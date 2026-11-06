@echo off
REM Arranque rapido en modo DEMO (sin DBeaver) para Windows.
REM Abre dos ventanas: backend (API) y frontend (Vite).

start "CredVault API (demo)" cmd /k "cd backend && pip install -e . && set CREDVAULT_DEMO=1 && uvicorn credvault.infrastructure.api.main:app --port 8000"
start "CredVault Front" cmd /k "cd frontend && npm install && npm run dev"
echo Abre http://localhost:5173 cuando ambas ventanas esten listas.
