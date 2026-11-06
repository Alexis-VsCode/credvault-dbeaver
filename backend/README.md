# CredVault · Backend

API y CLI de recuperación de credenciales de DBeaver, en **arquitectura hexagonal**.

Capas: `domain` (modelos puros) → `application` (puertos + casos de uso) → `infrastructure`
(adaptadores: AES, filesystem, metadata, API FastAPI, CLI).

```bash
pip install -e ".[dev]"
pytest -q
uvicorn credvault.infrastructure.api.main:app --port 8000   # real
CREDVAULT_DEMO=1 uvicorn credvault.infrastructure.api.main:app --port 8000   # demo
```

Ver la documentación completa en [`../docs`](../docs) y el [README raíz](../README.md).
