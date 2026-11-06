"""Caso de uso: escanear instalaciones de DBeaver.

Outside-in (ODD): el caso de uso define el contrato; la infraestructura
lo satisface. Emite LogEntry observables en cada paso.
"""
from __future__ import annotations

from credvault.application.ports import InstallationFinderPort
from credvault.domain.models import Installation, LogEntry, LogLevel


class ScanInstallations:
    """Descubre instalaciones. Depende del puerto, no de la implementación (DIP)."""

    def __init__(self, finder: InstallationFinderPort) -> None:
        self._finder = finder

    def execute(self) -> tuple[list[Installation], list[LogEntry]]:
        log: list[LogEntry] = []
        installations = self._finder.find()
        if not installations:
            log.append(LogEntry(LogLevel.WARN, "No se encontraron instalaciones de DBeaver."))
            return [], log
        for inst in installations:
            log.append(LogEntry(LogLevel.OK, f"Detectada: {inst.name} ({inst.kind.value})"))
        return installations, log
