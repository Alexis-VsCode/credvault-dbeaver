# Patrones de diseño y clean code

Este documento explica **qué patrones se aplicaron, dónde y por qué** — y, igual de importante,
los que se decidió **no** usar para evitar sobreingeniería.

## Patrones aplicados

### Ports & Adapters (Hexagonal)
El corazón del proyecto. El dominio y los casos de uso definen **puertos** (interfaces) y la
infraestructura aporta **adaptadores** concretos.

- Puertos: `InstallationFinderPort`, `CredentialDecryptorPort`, `MetadataReaderPort`.
- Adaptadores: `FilesystemInstallationFinder`, `AesCredentialDecryptor`, `JsonDataSourcesReader`.
- **Beneficio**: el negocio se prueba sin filesystem ni cripto; cambiar una tecnología no toca el
  dominio.

### Dependency Injection + Composition Root
Las dependencias se construyen en un único lugar (`infrastructure/api/deps.py` en el backend,
`infrastructure/config.ts` en el frontend) y se inyectan por constructor.

- **Beneficio**: el grafo de dependencias es explícito y testeable; nada se instancia "a escondidas".

### Strategy
`CredentialDecryptorPort` es una estrategia de descifrado. Hoy hay dos implementaciones
intercambiables (`AesCredentialDecryptor`, `DemoDecryptor`); mañana podría sumarse una con
contraseña maestra **sin tocar** el caso de uso.

### DTO + Mapper (capa anticorrupción)
La API no expone el dominio: lo traduce a DTOs Pydantic (`schemas.py`, método `from_domain`). El
frontend tiene sus propios tipos en `domain/models.ts`.

- **Beneficio**: el formato del JSON de transporte puede cambiar sin arrastrar al dominio.

### Aggregate Root (DDD)
`RecoveryReport` agrupa instalaciones, conexiones y log, y es el único objeto que cruza la frontera
hacia la API/CLI. Centraliza los conteos derivados (`with_password_count`, etc.).

### Value Object
`Credential` es inmutable (`frozen=True`) y sabe enmascararse (`masked()`), así una contraseña no
se registra por accidente en un log.

## Clean code — decisiones concretas

- **Nombres del dominio, no técnicos**: `MasterPasswordProtected` en vez de una excepción genérica.
- **Funciones cortas y una responsabilidad** por clase/módulo.
- **Errores que son del negocio** viven en `domain/errors.py`, separados de las excepciones de
  librería (se traducen en el adaptador).
- **Observabilidad de primera clase**: cada paso emite un `LogEntry` tipado en vez de `print`.
- **Fronteras explícitas**: el dominio no importa FastAPI, `cryptography`, `os` ni React.

## Qué NO se hizo (y por qué)

Evitar sobreingeniería también es una decisión de diseño:

- **Sin base de datos ni ORM**: la herramienta lee archivos y responde; no hay estado que persistir.
- **Sin event bus ni CQRS**: el flujo es lineal (escanear → descifrar → unir → reportar).
- **Sin inyección por framework/contenedor DI**: un composition root a mano es suficiente y más
  legible para este tamaño.
- **Sin capa de repositorio genérica**: los puertos existentes ya son la abstracción justa; una capa
  extra solo agregaría indirección.
- **Sin microservicios**: un backend y un frontend bastan; separarlos más sería complejidad sin
  retorno.

La regla aplicada: **introducir un patrón solo cuando resuelve un problema real presente**, no por
anticipación.
