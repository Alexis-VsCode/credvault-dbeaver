# Cómo contribuir

¡Gracias por tu interés! Este proyecto es abierto (MIT) y las contribuciones son bienvenidas.

## Antes de empezar

- Lee el [DISCLAIMER](DISCLAIMER.md): la herramienta es para recuperar **credenciales propias**.
- Revisa la [arquitectura](docs/ARQUITECTURA.md) y los [patrones](docs/PATRONES.md). El proyecto es
  **hexagonal**: si agregas una fuente de datos o un formato de salida, hazlo como **adaptador**
  implementando el puerto correspondiente, sin tocar el dominio ni los casos de uso.

## Entorno de desarrollo

```bash
# Backend
cd backend
pip install -e ".[dev]"
pytest -q
mypy src/credvault
ruff check src tests

# Frontend
cd frontend
npm install
npm run typecheck
npm run build
```

## Flujo de trabajo

1. Haz un fork y crea una rama: `feat/mi-mejora` o `fix/mi-arreglo`.
2. Escribe o actualiza los **tests** (TDD): ningún PR entra con los tests en rojo.
3. Mantén el estilo: `ruff` para Python, `tsc` estricto para TypeScript.
4. Commits en formato [Conventional Commits](https://www.conventionalcommits.org/):
   `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`.
5. Abre el Pull Request contra `develop` y completa la plantilla.

## Reglas de diseño (clean code, sin sobreingeniería)

- Una clase, una responsabilidad. Nombres del dominio, no técnicos.
- Depende de **puertos** (interfaces), no de implementaciones.
- No agregues capas, carpetas ni patrones que el problema no pida.
- Todo lo observable se registra como `LogEntry`, no como `print` suelto.

## Reporte de bugs y seguridad

- Bugs funcionales: abre un *issue* con la plantilla.
- Vulnerabilidades: sigue la [política de seguridad](SECURITY.md) (no las publiques como issue).
