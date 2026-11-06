"""Modelos del dominio (DDD - lenguaje ubicuo).

Capa de dominio PURA: sin dependencias de framework, I/O ni cripto.
Todo lo que entra aquí es vocabulario del negocio:

- Installation     : una instalación de DBeaver detectada en la máquina.
- Credential       : value object inmutable (usuario + contraseña).
- Connection       : una conexión a base de datos con su credencial recuperada.
- LogEntry         : evento observable del proceso (ODD / observability).
- RecoveryReport   : agregado raíz con el resultado completo de una recuperación.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class InstallationKind(str, Enum):
    """Origen de la instalación de DBeaver."""

    STORE = "store"        # Microsoft Store (AppData\Local\Packages\...)
    INSTALLER = "installer"  # Instalador MSI/EXE (AppData\Roaming\DBeaverData)
    PORTABLE = "portable"    # Versión portable (workspace junto al ejecutable)
    UNKNOWN = "unknown"


class LogLevel(str, Enum):
    OK = "ok"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


@dataclass(frozen=True)
class Installation:
    """Entidad: una instalación de DBeaver con su workspace y archivo de credenciales."""

    name: str
    kind: InstallationKind
    workspace_path: str
    credentials_file: str
    data_sources_file: str | None = None

    @property
    def has_data_sources(self) -> bool:
        return bool(self.data_sources_file)


@dataclass(frozen=True)
class Credential:
    """Value object inmutable. La contraseña nunca se registra en logs."""

    user: str = ""
    password: str = ""

    @property
    def has_password(self) -> bool:
        return bool(self.password)

    def masked(self) -> Credential:
        """Devuelve una copia con la contraseña enmascarada (para logs/telemetría)."""
        return Credential(user=self.user, password="•" * len(self.password) if self.password else "")


@dataclass(frozen=True)
class Connection:
    """Entidad: conexión a BD con metadatos y credencial recuperada."""

    id: str
    name: str
    installation_name: str
    driver: str = ""
    host: str = ""
    port: str = ""
    database: str = ""
    credential: Credential = field(default_factory=Credential)

    @property
    def endpoint(self) -> str:
        if self.host and self.port:
            return f"{self.host}:{self.port}"
        return self.host or ""


@dataclass(frozen=True)
class LogEntry:
    """Evento observable del proceso de recuperación (ODD)."""

    level: LogLevel
    message: str


@dataclass
class RecoveryReport:
    """Agregado raíz: resultado de un escaneo + recuperación.

    Reúne instalaciones, conexiones recuperadas y la traza observable.
    """

    installations: list[Installation] = field(default_factory=list)
    connections: list[Connection] = field(default_factory=list)
    log: list[LogEntry] = field(default_factory=list)

    def add_log(self, level: LogLevel, message: str) -> None:
        self.log.append(LogEntry(level=level, message=message))

    @property
    def installations_count(self) -> int:
        return len(self.installations)

    @property
    def connections_count(self) -> int:
        return len(self.connections)

    @property
    def with_password_count(self) -> int:
        return sum(1 for c in self.connections if c.credential.has_password)
