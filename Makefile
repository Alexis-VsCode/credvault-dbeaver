.PHONY: install test typecheck api cli front front-build

install:
	cd backend && pip install -e ".[dev]"
	cd frontend && npm install

test:
	cd backend && pytest -q

typecheck:
	cd backend && mypy src/credvault
	cd frontend && npm run typecheck

api:            ## API real (lee tu DBeaver local)
	cd backend && uvicorn credvault.infrastructure.api.main:app --reload --port 8000

api-demo:       ## API en modo demo (sin DBeaver)
	cd backend && CREDVAULT_DEMO=1 uvicorn credvault.infrastructure.api.main:app --port 8000

cli:
	cd backend && CREDVAULT_DEMO=1 credvault --show

front:
	cd frontend && npm run dev

front-build:
	cd frontend && npm run build
