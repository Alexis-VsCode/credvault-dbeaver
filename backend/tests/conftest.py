"""Fixtures de test (TDD).

`encrypted_credentials_file` genera un credentials-config.json CIFRADO real
con la clave pública de DBeaver y datos FICTICIOS, para validar el descifrado
de extremo a extremo sin depender de un DBeaver instalado.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

_KEY = bytes.fromhex("babb4a9f774ab853c96c2d653dfe544a")

_DEMO_CREDS = {
    "postgres-demo": {"#connection": {"user": "demo_user", "password": "Demo#1234"}},
}
_DEMO_DATASOURCES = {
    "connections": {
        "postgres-demo": {
            "name": "ventas-demo",
            "driver": "postgresql",
            "configuration": {"host": "db.example.local", "port": "5432", "database": "ventas"},
        }
    }
}


def _encrypt(payload: dict) -> bytes:
    """Replica el formato de DBeaver: IV(16) + AES-CBC(16 bytes random + JSON + padding)."""
    iv = os.urandom(16)
    plaintext = os.urandom(16) + json.dumps(payload).encode("utf-8")
    pad = 16 - (len(plaintext) % 16)
    plaintext += bytes([pad]) * pad  # PKCS7
    enc = Cipher(algorithms.AES(_KEY), modes.CBC(iv)).encryptor()
    return iv + enc.update(plaintext) + enc.finalize()


@pytest.fixture
def encrypted_credentials_file(tmp_path: Path) -> Path:
    f = tmp_path / "credentials-config.json"
    f.write_bytes(_encrypt(_DEMO_CREDS))
    return f


@pytest.fixture
def data_sources_file(tmp_path: Path) -> Path:
    f = tmp_path / "data-sources.json"
    f.write_text(json.dumps(_DEMO_DATASOURCES), encoding="utf-8")
    return f


@pytest.fixture
def fake_workspace(tmp_path: Path) -> Path:
    """Árbol .../workspace6/General/.dbeaver/ con ambos archivos, para el finder."""
    dbeaver = tmp_path / "workspace6" / "General" / ".dbeaver"
    dbeaver.mkdir(parents=True)
    (dbeaver / "credentials-config.json").write_bytes(_encrypt(_DEMO_CREDS))
    (dbeaver / "data-sources.json").write_text(json.dumps(_DEMO_DATASOURCES), encoding="utf-8")
    return tmp_path
