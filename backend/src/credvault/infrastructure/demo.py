"""Adaptadores de DEMO con datos 100% ficticios.

NO contienen IPs ni credenciales reales. Sirven para probar la app sin
DBeaver instalado (modo CREDVAULT_DEMO=1) y para capturas del portafolio.

Implementan los mismos puertos que los adaptadores reales (LSP): el caso de
uso no nota la diferencia.
"""
from __future__ import annotations

from credvault.application.ports import (
    CredentialDecryptorPort,
    InstallationFinderPort,
    MetadataReaderPort,
)
from credvault.domain.models import Installation, InstallationKind

_DEMO_CRED_FILE = "demo://store/credentials-config.json"
_DEMO_DATA_FILE = "demo://store/data-sources.json"


class DemoFinder(InstallationFinderPort):
    def find(self) -> list[Installation]:
        return [
            Installation(
                name="workspace6",
                kind=InstallationKind.STORE,
                workspace_path="demo://DBeaver Community (Store)",
                credentials_file=_DEMO_CRED_FILE,
                data_sources_file=_DEMO_DATA_FILE,
            )
        ]


class DemoDecryptor(CredentialDecryptorPort):
    def decrypt(self, credentials_file: str) -> dict:
        return {
            "postgres-demo": {"#connection": {"user": "demo_user", "password": "Demo#1234"}},
            "reporting-demo": {"#connection": {"user": "report_ro", "password": "R3port!2026"}},
        }


class DemoMetadataReader(MetadataReaderPort):
    def read(self, data_sources_file: str) -> dict:
        return {
            "postgres-demo": {
                "name": "ventas-demo",
                "driver": "postgresql",
                "host": "db.example.local",
                "port": "5432",
                "database": "ventas",
            },
            "reporting-demo": {
                "name": "reporting-demo",
                "driver": "postgresql",
                "host": "reports.example.local",
                "port": "5432",
                "database": "reporting",
            },
        }
