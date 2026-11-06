"""Adaptador de descifrado AES para credentials-config.json de DBeaver.

DBeaver Community cifra el almacén con AES-128-CBC y una CLAVE FIJA pública
(no es un secreto: viene embebida en el propio DBeaver). El IV son los
primeros 16 bytes del archivo; el resto es el texto cifrado.

Implementa CredentialDecryptorPort → es sustituible por LSP (p. ej. un
descifrador con contraseña maestra en el futuro, sin tocar el caso de uso).
"""
from __future__ import annotations

import json

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from credvault.application.ports import CredentialDecryptorPort
from credvault.domain.errors import (
    CorruptCredentialsFile,
    CredentialsDecryptionError,
    MasterPasswordProtected,
)

# Clave pública fija de DBeaver Community (AES-128). No es información sensible.
_DBEAVER_LOCAL_KEY = bytes.fromhex("babb4a9f774ab853c96c2d653dfe544a")
_IV_SIZE = 16


class AesCredentialDecryptor(CredentialDecryptorPort):
    def __init__(self, key: bytes = _DBEAVER_LOCAL_KEY) -> None:
        self._key = key

    def decrypt(self, credentials_file: str) -> dict:
        with open(credentials_file, "rb") as fh:
            data = fh.read()

        if len(data) <= _IV_SIZE:
            raise CorruptCredentialsFile("El archivo de credenciales está vacío o truncado.")

        iv, ciphertext = data[:_IV_SIZE], data[_IV_SIZE:]
        if len(ciphertext) % _IV_SIZE != 0:
            # No es múltiplo de bloque → casi seguro cifrado con contraseña maestra.
            raise MasterPasswordProtected(credentials_file)

        try:
            decryptor = Cipher(algorithms.AES(self._key), modes.CBC(iv)).decryptor()
            plain = decryptor.update(ciphertext) + decryptor.finalize()
        except Exception as exc:
            raise CredentialsDecryptionError(str(exc)) from exc

        return self._parse_json(plain, credentials_file)

    @staticmethod
    def _parse_json(plain: bytes, source: str) -> dict:
        # DBeaver antepone 16 bytes aleatorios y añade padding: el JSON va
        # desde la primera '{' hasta la última '}'.
        start, end = plain.find(b"{"), plain.rfind(b"}")
        if start == -1 or end == -1 or end < start:
            # Descifró pero no hay JSON → la clave no corresponde (maestra).
            raise MasterPasswordProtected(source)
        try:
            parsed = json.loads(plain[start : end + 1])
        except json.JSONDecodeError as exc:
            raise CorruptCredentialsFile(f"JSON inválido tras descifrar: {exc}") from exc
        if not isinstance(parsed, dict):
            raise CorruptCredentialsFile("El contenido descifrado no es un objeto JSON.")
        return parsed
