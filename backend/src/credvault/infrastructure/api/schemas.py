"""DTOs de la API (Pydantic). Traducen el dominio a JSON de transporte.

Separados del dominio a propósito: el dominio no depende de Pydantic ni de
la forma del JSON que viaja al frontend (DIP / anticorrupción).
"""
from __future__ import annotations

from pydantic import BaseModel

from credvault.domain.models import Connection, LogEntry, RecoveryReport


class CredentialDTO(BaseModel):
    user: str
    password: str
    has_password: bool


class ConnectionDTO(BaseModel):
    id: str
    name: str
    installation_name: str
    driver: str
    host: str
    port: str
    database: str
    endpoint: str
    credential: CredentialDTO

    @classmethod
    def from_domain(cls, c: Connection) -> ConnectionDTO:
        return cls(
            id=c.id,
            name=c.name,
            installation_name=c.installation_name,
            driver=c.driver,
            host=c.host,
            port=c.port,
            database=c.database,
            endpoint=c.endpoint,
            credential=CredentialDTO(
                user=c.credential.user,
                password=c.credential.password,
                has_password=c.credential.has_password,
            ),
        )


class LogEntryDTO(BaseModel):
    level: str
    message: str

    @classmethod
    def from_domain(cls, e: LogEntry) -> LogEntryDTO:
        return cls(level=e.level.value, message=e.message)


class InstallationDTO(BaseModel):
    name: str
    kind: str
    workspace_path: str


class RecoveryReportDTO(BaseModel):
    installations: list[InstallationDTO]
    connections: list[ConnectionDTO]
    log: list[LogEntryDTO]
    installations_count: int
    connections_count: int
    with_password_count: int

    @classmethod
    def from_domain(cls, r: RecoveryReport) -> RecoveryReportDTO:
        return cls(
            installations=[
                InstallationDTO(name=i.name, kind=i.kind.value, workspace_path=i.workspace_path)
                for i in r.installations
            ],
            connections=[ConnectionDTO.from_domain(c) for c in r.connections],
            log=[LogEntryDTO.from_domain(e) for e in r.log],
            installations_count=r.installations_count,
            connections_count=r.connections_count,
            with_password_count=r.with_password_count,
        )
