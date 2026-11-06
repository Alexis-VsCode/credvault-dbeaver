"""Tests de integración: finder + decryptor + metadata reales sobre un
workspace de disco (ficticio), y la API FastAPI de punta a punta.
"""
from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from credvault.application.use_cases.recover_credentials import RecoverCredentials
from credvault.infrastructure.crypto.aes_decryptor import AesCredentialDecryptor
from credvault.infrastructure.finders.filesystem_finder import FilesystemInstallationFinder
from credvault.infrastructure.metadata.datasources_reader import JsonDataSourcesReader


def test_pipeline_real_sobre_workspace_ficticio(fake_workspace: Path) -> None:
    uc = RecoverCredentials(
        FilesystemInstallationFinder(base_paths=[fake_workspace]),
        AesCredentialDecryptor(),
        JsonDataSourcesReader(),
    )
    report = uc.execute()
    assert report.installations_count == 1
    assert report.connections_count == 1
    conn = report.connections[0]
    assert conn.name == "ventas-demo"
    assert conn.host == "db.example.local"
    assert conn.credential.password == "Demo#1234"


def test_api_demo_mode(monkeypatch) -> None:
    monkeypatch.setenv("CREDVAULT_DEMO", "1")
    from credvault.infrastructure.api.main import create_app

    client = TestClient(create_app())

    assert client.get("/api/health").json() == {"status": "ok"}

    resp = client.post("/api/recover")
    assert resp.status_code == 200
    body = resp.json()
    assert body["connections_count"] == 2
    assert body["with_password_count"] == 2
    names = {c["name"] for c in body["connections"]}
    assert "ventas-demo" in names
