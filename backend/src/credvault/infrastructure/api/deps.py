"""Composición de dependencias (Composition Root).

Único lugar donde se instancian adaptadores concretos y se inyectan en los
casos de uso. Cambiar una implementación (p. ej. otro finder) se hace aquí,
sin tocar el dominio ni la aplicación (OCP).

En modo demo (CREDVAULT_DEMO=1) usa un finder y un descifrador en memoria
con datos ficticios: permite probar la app sin DBeaver instalado y sin
ninguna credencial real.
"""
from __future__ import annotations

import os
from pathlib import Path

from credvault.application.ports import (
    CredentialDecryptorPort,
    InstallationFinderPort,
    MetadataReaderPort,
)
from credvault.application.use_cases.recover_credentials import RecoverCredentials
from credvault.application.use_cases.scan_installations import ScanInstallations
from credvault.infrastructure.crypto.aes_decryptor import AesCredentialDecryptor
from credvault.infrastructure.finders.filesystem_finder import FilesystemInstallationFinder
from credvault.infrastructure.metadata.datasources_reader import JsonDataSourcesReader


def _is_demo() -> bool:
    return os.environ.get("CREDVAULT_DEMO", "").strip() in {"1", "true", "yes"}


def _build_adapters() -> tuple[
    InstallationFinderPort, CredentialDecryptorPort, MetadataReaderPort
]:
    if _is_demo():
        from credvault.infrastructure.demo import (  # import local para no cargar demo en prod
            DemoDecryptor,
            DemoFinder,
            DemoMetadataReader,
        )

        return DemoFinder(), DemoDecryptor(), DemoMetadataReader()

    base = os.environ.get("CREDVAULT_BASE_PATH")
    base_paths = [Path(base)] if base else None
    return (
        FilesystemInstallationFinder(base_paths=base_paths),
        AesCredentialDecryptor(),
        JsonDataSourcesReader(),
    )


def build_recover_use_case() -> RecoverCredentials:
    finder, decryptor, metadata = _build_adapters()
    return RecoverCredentials(finder, decryptor, metadata)


def build_scan_use_case() -> ScanInstallations:
    finder, _, _ = _build_adapters()
    return ScanInstallations(finder)
