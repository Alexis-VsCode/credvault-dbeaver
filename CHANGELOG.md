# Changelog

Todas las novedades relevantes de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el versionado
[SemVer](https://semver.org/lang/es/).

## [1.0.0] - 2026-11-06

### Añadido
- Núcleo de dominio (DDD): `Installation`, `Connection`, `Credential`, `RecoveryReport`, errores.
- Casos de uso `ScanInstallations` y `RecoverCredentials` sobre puertos (arquitectura hexagonal).
- Adaptadores: descifrado AES-128-CBC, buscador de instalaciones en filesystem, lector de
  `data-sources.json`, modo demo con datos ficticios.
- API REST con FastAPI (`/api/health`, `/api/installations`, `/api/recover`) y CLI.
- Frontend React + TypeScript con capas `domain / application / infrastructure / ui`, consola de
  escaneo con revelar/copiar y paleta corporativa.
- Suite de pruebas (dominio, cripto con fixtures cifrados reales, casos de uso, integración y API).
- Integración continua (GitHub Actions) y despliegue con Docker.
- Documentación: arquitectura, patrones, metodología, manual de usuario y manual técnico.

### Seguridad
- Detección de almacenes protegidos con contraseña maestra (no se fuerza, se informa).
- Sin credenciales, hosts ni IPs reales en el repositorio.
