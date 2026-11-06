"""Tests de casos de uso con dobles de prueba (TDD + hexagonal).

Los puertos se sustituyen por fakes en memoria: se prueba la LÓGICA de
orquestación sin filesystem ni cripto. Verifica DIP (todo inyectado) y LSP
(los fakes encajan donde van los adaptadores reales).
"""
from __future__ import annotations

from credvault.application.ports import (
    CredentialDecryptorPort,
    InstallationFinderPort,
    MetadataReaderPort,
)
from credvault.application.use_cases.recover_credentials import RecoverCredentials
from credvault.application.use_cases.scan_installations import ScanInstallations
from credvault.domain.errors import MasterPasswordProtected
from credvault.domain.models import Installation, InstallationKind, LogLevel


class FakeFinder(InstallationFinderPort):
    def __init__(self, installations: list[Installation]) -> None:
        self._installations = installations

    def find(self) -> list[Installation]:
        return self._installations


class FakeDecryptor(CredentialDecryptorPort):
    def __init__(self, data: dict, raises: Exception | None = None) -> None:
        self._data = data
        self._raises = raises

    def decrypt(self, credentials_file: str) -> dict:
        if self._raises:
            raise self._raises
        return self._data


class FakeMetadata(MetadataReaderPort):
    def __init__(self, data: dict) -> None:
        self._data = data

    def read(self, data_sources_file: str) -> dict:
        return self._data


def _installation() -> Installation:
    return Installation(
        name="workspace6",
        kind=InstallationKind.STORE,
        workspace_path="demo://ws",
        credentials_file="demo://cred",
        data_sources_file="demo://data",
    )


def test_scan_reporta_instalaciones() -> None:
    uc = ScanInstallations(FakeFinder([_installation()]))
    installations, log = uc.execute()
    assert len(installations) == 1
    assert any(e.level == LogLevel.OK for e in log)


def test_scan_sin_instalaciones_avisa() -> None:
    installations, log = ScanInstallations(FakeFinder([])).execute()
    assert installations == []
    assert any(e.level == LogLevel.WARN for e in log)


def test_recover_une_credencial_con_metadatos() -> None:
    uc = RecoverCredentials(
        FakeFinder([_installation()]),
        FakeDecryptor({"c1": {"#connection": {"user": "u", "password": "p"}}}),
        FakeMetadata({"c1": {"name": "ventas", "host": "db.example.local", "port": "5432"}}),
    )
    report = uc.execute()
    assert report.connections_count == 1
    conn = report.connections[0]
    assert conn.name == "ventas"
    assert conn.endpoint == "db.example.local:5432"
    assert conn.credential.user == "u"
    assert report.with_password_count == 1


def test_recover_omite_workspace_con_master_password() -> None:
    uc = RecoverCredentials(
        FakeFinder([_installation()]),
        FakeDecryptor({}, raises=MasterPasswordProtected("demo://cred")),
        FakeMetadata({}),
    )
    report = uc.execute()
    assert report.connections_count == 0
    assert any(e.level == LogLevel.WARN and "maestra" in e.message for e in report.log)


def test_recover_sin_instalaciones() -> None:
    report = RecoverCredentials(FakeFinder([]), FakeDecryptor({}), FakeMetadata({})).execute()
    assert report.installations_count == 0
    assert any(e.level == LogLevel.WARN for e in report.log)
