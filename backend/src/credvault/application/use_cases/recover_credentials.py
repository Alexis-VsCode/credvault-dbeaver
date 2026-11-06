"""Caso de uso: recuperar credenciales de todas las instalaciones.

Orquesta tres puertos (finder, decryptor, metadata) y produce un
RecoveryReport (agregado). No conoce AES, rutas ni JSON concretos: todo
llega por inyección de dependencias (DIP / hexagonal).
"""
from __future__ import annotations

from credvault.application.ports import (
    CredentialDecryptorPort,
    InstallationFinderPort,
    MetadataReaderPort,
)
from credvault.domain.errors import (
    CorruptCredentialsFile,
    CredentialsDecryptionError,
    MasterPasswordProtected,
)
from credvault.domain.models import (
    Connection,
    Credential,
    Installation,
    LogLevel,
    RecoveryReport,
)


class RecoverCredentials:
    def __init__(
        self,
        finder: InstallationFinderPort,
        decryptor: CredentialDecryptorPort,
        metadata_reader: MetadataReaderPort,
    ) -> None:
        self._finder = finder
        self._decryptor = decryptor
        self._metadata = metadata_reader

    def execute(self) -> RecoveryReport:
        report = RecoveryReport()
        report.installations = self._finder.find()

        if not report.installations:
            report.add_log(LogLevel.WARN, "No se encontraron instalaciones de DBeaver.")
            return report

        for inst in report.installations:
            report.add_log(LogLevel.OK, f"Detectada: {inst.name} ({inst.kind.value})")
            self._recover_installation(inst, report)

        report.add_log(
            LogLevel.INFO,
            f"{report.connections_count} conexiones · {report.with_password_count} con contraseña.",
        )
        return report

    def _recover_installation(self, inst: Installation, report: RecoveryReport) -> None:
        try:
            raw = self._decryptor.decrypt(inst.credentials_file)
        except MasterPasswordProtected:
            report.add_log(
                LogLevel.WARN,
                f"{inst.name}: protegido con contraseña maestra, se omite.",
            )
            return
        except (CredentialsDecryptionError, CorruptCredentialsFile) as exc:
            report.add_log(LogLevel.ERROR, f"{inst.name}: {exc}")
            return

        metadata: dict = {}
        if inst.has_data_sources:
            # Los metadatos son best-effort: si el archivo falta o está corrupto, la
            # recuperación de usuario/contraseña continúa igual.
            try:
                metadata = self._metadata.read(inst.data_sources_file)  # type: ignore[arg-type]
            except (OSError, ValueError):
                report.add_log(LogLevel.INFO, f"{inst.name}: sin metadatos de conexión legibles.")

        for conn_id, node in raw.items():
            report.connections.append(self._build_connection(conn_id, node, metadata, inst))

    @staticmethod
    def _build_connection(
        conn_id: str, node: dict, metadata: dict, inst: Installation
    ) -> Connection:
        conn_creds = node.get("#connection", node) if isinstance(node, dict) else {}
        credential = Credential(
            user=str(conn_creds.get("user", "")),
            password=str(conn_creds.get("password", "")),
        )
        meta = metadata.get(conn_id, {})
        return Connection(
            id=conn_id,
            name=meta.get("name", conn_id),
            installation_name=inst.name,
            driver=meta.get("driver", ""),
            host=meta.get("host", ""),
            port=str(meta.get("port", "")),
            database=meta.get("database", ""),
            credential=credential,
        )
