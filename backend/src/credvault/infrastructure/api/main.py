"""Punto de entrada de la API FastAPI."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from credvault.infrastructure.api.routes import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="TEUNO · CredVault DBeaver",
        description="Recuperador local de credenciales de DBeaver (uso en tu propia máquina).",
        version="1.0.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


app = create_app()
