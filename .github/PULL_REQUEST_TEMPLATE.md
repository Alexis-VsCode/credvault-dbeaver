## Qué cambia

Describe brevemente el cambio y el porqué.

## Tipo

- [ ] `feat` — nueva funcionalidad
- [ ] `fix` — corrección de bug
- [ ] `refactor` — mejora interna sin cambio de comportamiento
- [ ] `docs` — documentación
- [ ] `test` — pruebas
- [ ] `chore` — build / tooling

## Checklist

- [ ] Los tests pasan (`pytest -q`) y agregué/actualicé los que corresponden.
- [ ] `mypy` y `ruff` sin errores.
- [ ] Si toqué el frontend, `npm run typecheck` y `npm run build` pasan.
- [ ] Respeté la arquitectura hexagonal (dominio sin dependencias; lo nuevo es un adaptador).
- [ ] No incluí credenciales, hosts ni IPs reales.
- [ ] Actualicé el `CHANGELOG.md` si aplica.

## Cómo probarlo

Pasos para verificar el cambio.
