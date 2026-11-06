"""Adaptador de entrada (driving): rutas HTTP de FastAPI.

Fino a propósito: traduce HTTP ↔ caso de uso y no contiene lógica de negocio.
"""
from __future__ import annotations

from fastapi import APIRouter

from credvault.infrastructure.api.deps import build_recover_use_case, build_scan_use_case
from credvault.infrastructure.api.schemas import InstallationDTO, RecoveryReportDTO

router = APIRouter(prefix="/api", tags=["credvault"])


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/installations", response_model=list[InstallationDTO])
def list_installations() -> list[InstallationDTO]:
    installations, _ = build_scan_use_case().execute()
    return [
        InstallationDTO(name=i.name, kind=i.kind.value, workspace_path=i.workspace_path)
        for i in installations
    ]


@router.post("/recover", response_model=RecoveryReportDTO)
def recover() -> RecoveryReportDTO:
    report = build_recover_use_case().execute()
    return RecoveryReportDTO.from_domain(report)
