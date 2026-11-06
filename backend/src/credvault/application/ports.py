"""Puertos (interfaces) de la capa de aplicación — arquitectura hexagonal.

Los casos de uso dependen SOLO de estas abstracciones (DIP). Las
implementaciones concretas (filesystem, AES, lectura de JSON) viven en
`infrastructure` y se inyectan por constructor.

ISP: puertos pequeños y enfocados, uno por responsabilidad.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from credvault.domain.models import Installation


class InstallationFinderPort(ABC):
    """Puerto de salida: descubre instalaciones de DBeaver en el sistema."""

    @abstractmethod
    def find(self) -> list[Installation]:
        """Devuelve las instalaciones detectadas (vacío si no hay)."""
        raise NotImplementedError


class CredentialDecryptorPort(ABC):
    """Puerto de salida: descifra el archivo credentials-config.json.

    Devuelve el mapa crudo { connection_id: {"#connection": {user, password}, ...} }.
    Lanza MasterPasswordProtected / CredentialsDecryptionError según el caso.
    """

    @abstractmethod
    def decrypt(self, credentials_file: str) -> dict:
        raise NotImplementedError


class MetadataReaderPort(ABC):
    """Puerto de salida: lee metadatos de conexión desde data-sources.json.

    Devuelve { connection_id: {name, driver, host, port, database} }.
    Es opcional: si no hay archivo, el caso de uso igual recupera user/pass.
    """

    @abstractmethod
    def read(self, data_sources_file: str) -> dict:
        raise NotImplementedError
