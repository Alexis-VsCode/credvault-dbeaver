# Backend: API FastAPI de CredVault (modo demo por defecto en contenedor).
FROM python:3.12-slim AS base

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CREDVAULT_DEMO=1

COPY backend/pyproject.toml backend/README.md* ./
COPY backend/src ./src

RUN pip install --no-cache-dir -e .

EXPOSE 8000

# Nota: dentro de un contenedor no hay DBeaver local; por eso corre en modo demo.
# Para uso real, ejecuta el backend directamente en tu máquina (ver README).
CMD ["uvicorn", "credvault.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
