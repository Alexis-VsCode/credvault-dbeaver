"""Tests del adaptador AES (TDD, outside-in sobre el puerto de descifrado)."""
from __future__ import annotations

from pathlib import Path

import pytest

from credvault.domain.errors import CorruptCredentialsFile, MasterPasswordProtected
from credvault.infrastructure.crypto.aes_decryptor import AesCredentialDecryptor


def test_descifra_credenciales_validas(encrypted_credentials_file: Path) -> None:
    result = AesCredentialDecryptor().decrypt(str(encrypted_credentials_file))
    assert "postgres-demo" in result
    conn = result["postgres-demo"]["#connection"]
    assert conn["user"] == "demo_user"
    assert conn["password"] == "Demo#1234"


def test_archivo_truncado_es_corrupto(tmp_path: Path) -> None:
    f = tmp_path / "credentials-config.json"
    f.write_bytes(b"\x00\x01\x02")  # menos de 16 bytes
    with pytest.raises(CorruptCredentialsFile):
        AesCredentialDecryptor().decrypt(str(f))


def test_bloque_no_alineado_sugiere_master_password(tmp_path: Path) -> None:
    f = tmp_path / "credentials-config.json"
    f.write_bytes(b"\x00" * 16 + b"\x00" * 17)  # ciphertext no múltiplo de 16
    with pytest.raises(MasterPasswordProtected):
        AesCredentialDecryptor().decrypt(str(f))


def test_clave_incorrecta_se_detecta_como_master_password(tmp_path: Path) -> None:
    # Cifrado con clave distinta → al descifrar no aparece JSON → MasterPasswordProtected.
    import os

    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    other_key = bytes.fromhex("00112233445566778899aabbccddeeff")
    iv = os.urandom(16)
    enc = Cipher(algorithms.AES(other_key), modes.CBC(iv)).encryptor()
    body = enc.update(b"\x11" * 48) + enc.finalize()
    f = tmp_path / "credentials-config.json"
    f.write_bytes(iv + body)
    with pytest.raises(MasterPasswordProtected):
        AesCredentialDecryptor().decrypt(str(f))
