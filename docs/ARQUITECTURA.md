# Arquitectura

## Hexagonal (puertos y adaptadores)

El objetivo es que la **lógica de negocio** no dependa de detalles técnicos (AES, filesystem,
HTTP, React). Esos detalles son **adaptadores** enchufados a **puertos**.

```
            ENTRADA (driving)                      SALIDA (driven)
         ┌──────────────────┐                 ┌──────────────────────┐
         │  FastAPI / CLI    │                 │ FilesystemFinder      │
         │  (adaptadores in) │                 │ AesDecryptor          │
         └────────┬─────────┘                 │ JsonDataSourcesReader │
                  │                            └──────────┬───────────┘
                  ▼                                       ▲
        ┌───────────────────────── APPLICATION ──────────┴───────────┐
        │  Casos de uso: ScanInstallations, RecoverCredentials        │
        │  Puertos: InstallationFinderPort, CredentialDecryptorPort,  │
        │           MetadataReaderPort                                │
        └───────────────────────────┬────────────────────────────────┘
                                     ▼
                          ┌──────── DOMAIN ────────┐
                          │ Installation, Connection│
                          │ Credential, LogEntry,   │
                          │ RecoveryReport, errores │
                          └─────────────────────────┘
```

- **Dominio**: dataclasses puras, sin imports de framework. Es el centro.
- **Aplicación**: casos de uso que orquestan puertos (interfaces abstractas).
- **Infraestructura**: implementaciones concretas + *composition root* (`deps.py`).

El mismo patrón se replica en el frontend: `domain` (tipos) → `application` (puerto `ApiClient`
+ hook `useRecovery`) → `infrastructure` (`HttpApiClient` / `DemoApiClient`) → `ui`.

## Principios SOLID — dónde se ven

| Principio | Dónde |
|-----------|-------|
| **S**RP | Cada adaptador hace una cosa: `AesCredentialDecryptor` solo descifra; `JsonDataSourcesReader` solo lee metadatos; cada caso de uso una operación. |
| **O**CP | Añadir un descifrador con contraseña maestra = nueva clase que implementa `CredentialDecryptorPort`, sin tocar el caso de uso. |
| **L**SP | `DemoDecryptor` y `AesCredentialDecryptor` son intercambiables donde se espera el puerto; los tests lo demuestran con fakes. |
| **I**SP | Tres puertos chicos y separados (finder / decryptor / metadata) en vez de una interfaz gorda. |
| **D**IP | Los casos de uso reciben los puertos por constructor; nunca importan infraestructura. El *composition root* arma el grafo. |

## Flujo de una recuperación

1. `RecoverCredentials.execute()` pide instalaciones al `InstallationFinderPort`.
2. Por cada instalación, descifra con `CredentialDecryptorPort` (maneja master-password).
3. Lee metadatos con `MetadataReaderPort` (best-effort) y los **une** por `connection_id`.
4. Construye el agregado `RecoveryReport` con conexiones + log observable.
5. El adaptador de entrada (API/CLI) traduce el reporte a su formato.
