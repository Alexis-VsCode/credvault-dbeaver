# Manual técnico

## Requisitos

- Python 3.10+
- Node.js 18+ (probado con 22) y npm
- Windows 10/11 para uso real; Linux/macOS para desarrollo y tests.

## Estructura del repositorio

```
teuno-credvault-dbeaver/
├── backend/
│   ├── pyproject.toml
│   ├── src/credvault/
│   │   ├── domain/            models.py, errors.py
│   │   ├── application/       ports.py, use_cases/
│   │   └── infrastructure/    crypto/, finders/, metadata/, api/, cli/, demo.py
│   └── tests/                 conftest.py, test_*.py
├── frontend/
│   ├── package.json, vite.config.ts, tsconfig.json
│   └── src/
│       ├── domain/            models.ts
│       ├── application/       ApiClient.ts, useRecovery.ts
│       ├── infrastructure/    HttpApiClient.ts, DemoApiClient.ts, config.ts
│       └── ui/                components/<Comp>/, pages/ConsoleView/, theme.css
└── docs/
```

## Backend

### Instalar y correr

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # opcional
pip install -e ".[dev]"
uvicorn credvault.infrastructure.api.main:app --reload --port 8000
```

### Variables de entorno

| Variable | Efecto |
|----------|--------|
| `CREDVAULT_DEMO=1` | Usa adaptadores de demo (sin DBeaver, datos ficticios). |
| `CREDVAULT_BASE_PATH=/ruta` | Fuerza la raíz donde buscar workspaces (útil en tests/manual). |

### Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/health` | Chequeo de vida. |
| GET | `/api/installations` | Instalaciones detectadas. |
| POST | `/api/recover` | Recupera credenciales y devuelve el `RecoveryReport`. |

### Tests y tipado

```bash
pytest                 # unit + integración + API
mypy src/credvault
ruff check src tests   # si instalas ruff
```

## Frontend

```bash
cd frontend
npm install
npm run dev            # dev server :5173 con proxy /api → :8000
npm run build          # build de producción en dist/
npm run typecheck      # tsc --noEmit
```

En producción sirve `frontend/dist/` detrás del mismo origen que la API, o deja el proxy.
Para una demo estática (p. ej. GitHub Pages) compila con `VITE_DEMO=1` y usa `DemoApiClient`.

## Cómo extenderlo

- **Soportar contraseña maestra**: nueva clase que implemente `CredentialDecryptorPort` pidiendo
  la clave; se registra en `deps.py`. El caso de uso no cambia (OCP).
- **Otro gestor (no DBeaver)**: nuevo `InstallationFinderPort` + `CredentialDecryptorPort`.
- **Exportar a CSV/KeePass**: nuevo adaptador de salida que consuma el `RecoveryReport`.

## Detalle del cifrado

- Algoritmo: **AES-128-CBC**, clave fija pública de DBeaver (`babb4a9f...544a`).
- Formato del archivo: `IV (16 bytes) + ciphertext`. Tras descifrar, DBeaver antepone 16 bytes
  aleatorios y añade padding; el JSON va de la primera `{` a la última `}`.
- Detección de master-password: ciphertext no alineado a 16 bytes, o descifrado sin JSON válido.
