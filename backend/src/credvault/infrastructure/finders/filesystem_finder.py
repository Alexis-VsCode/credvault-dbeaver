"""Adaptador: descubre instalaciones de DBeaver recorriendo el filesystem.

Implementa InstallationFinderPort. Busca el archivo
`.dbeaver/credentials-config.json` en las ubicaciones conocidas de Windows
(Store, instalador MSI, portable) y en Linux/macOS para desarrollo/tests.

Las rutas base son inyectables → testeable sin un DBeaver real (DIP).
"""
from __future__ import annotations

import os
from pathlib import Path

from credvault.application.ports import InstallationFinderPort
from credvault.domain.models import Installation, InstallationKind

_CREDENTIALS_NAME = "credentials-config.json"
_DATA_SOURCES_NAME = "data-sources.json"


def _default_base_paths() -> list[Path]:
    """Rutas raíz donde DBeaver suele guardar sus workspaces, por SO."""
    home = Path.home()
    bases: list[Path] = []

    local = os.environ.get("LOCALAPPDATA")
    roaming = os.environ.get("APPDATA")
    if roaming:  # Windows - instalador MSI/EXE
        bases.append(Path(roaming) / "DBeaverData")
    if local:  # Windows - Microsoft Store (bajo Packages\DBeaverCorp...)
        bases.append(Path(local) / "Packages")
        bases.append(Path(local) / "DBeaverData")

    # Linux / macOS (desarrollo) y portable bajo el home.
    bases.append(home / ".local" / "share" / "DBeaverData")
    bases.append(home / "Library" / "DBeaverData")
    bases.append(home / "DBeaverData")
    return [b for b in bases if b.exists()]


def _classify(workspace: Path) -> InstallationKind:
    text = str(workspace).lower()
    if "packages" in text and "dbeavercorp" in text:
        return InstallationKind.STORE
    if "roaming" in text or "dbeaverdata" in text:
        return InstallationKind.INSTALLER
    return InstallationKind.UNKNOWN


class FilesystemInstallationFinder(InstallationFinderPort):
    def __init__(self, base_paths: list[Path] | None = None) -> None:
        self._base_paths = base_paths if base_paths is not None else _default_base_paths()

    def find(self) -> list[Installation]:
        found: list[Installation] = []
        seen: set[str] = set()
        for base in self._base_paths:
            for cred_file in base.rglob(_CREDENTIALS_NAME):
                key = str(cred_file.resolve())
                if key in seen:
                    continue
                seen.add(key)
                found.append(self._to_installation(cred_file))
        return found

    @staticmethod
    def _to_installation(cred_file: Path) -> Installation:
        dbeaver_dir = cred_file.parent          # .../General/.dbeaver
        general_dir = dbeaver_dir.parent         # .../General
        workspace = general_dir.parent           # .../workspace6
        data_sources = dbeaver_dir / _DATA_SOURCES_NAME
        return Installation(
            name=workspace.name or "workspace",
            kind=_classify(workspace),
            workspace_path=str(workspace),
            credentials_file=str(cred_file),
            data_sources_file=str(data_sources) if data_sources.exists() else None,
        )
