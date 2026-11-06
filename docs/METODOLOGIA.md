# Metodología: DDD + TDD + ODD

El proyecto combina tres enfoques de forma deliberada.

## DDD — Domain-Driven Design

- **Lenguaje ubicuo**: los nombres del código son los del negocio —
  `Installation`, `Connection`, `Credential`, `RecoveryReport`, `MasterPasswordProtected`.
- **Capa de dominio aislada**: `domain/` no importa FastAPI, `cryptography` ni `os`. Es
  modelable y testeable sola.
- **Value objects vs entidades**: `Credential` es un value object inmutable (frozen); `Connection`
  e `Installation` son entidades; `RecoveryReport` es el **agregado raíz** del resultado.
- **Errores del dominio**: expresan reglas (`MasterPasswordProtected`, `CorruptCredentialsFile`),
  no excepciones técnicas crudas.

## TDD — Test-Driven Development

- Ciclo **red → green → refactor**. Los puertos permiten escribir el test del caso de uso antes
  que el adaptador real, usando *fakes*.
- Cobertura por capas:
  - **dominio/aplicación**: `test_use_cases.py` con fakes en memoria.
  - **cripto**: `test_aes_decryptor.py` con fixtures **cifrados de verdad** (datos ficticios).
  - **integración**: `test_integration.py` arma un workspace de disco real y prueba el pipeline
    completo + la API con `TestClient`.
- Un fixture (`conftest.py`) genera el `credentials-config.json` cifrado con el mismo formato que
  DBeaver, así se valida el descifrado sin depender de una instalación real.

## ODD — Outside-in & Observability-Driven

- **Outside-in**: se parte del contrato del caso de uso (lo que la API/CLI necesita) y se avanza
  hacia adentro; los adaptadores existen para satisfacer ese contrato, no al revés.
- **Observabilidad**: cada paso del proceso emite un `LogEntry` tipado (`ok/info/warn/error`). Ese
  log es parte del modelo (no un `print` suelto) y viaja hasta la consola web, de modo que el
  comportamiento del sistema es **observable** de extremo a extremo. Encaja con un perfil de
  desarrollador orientado a observabilidad/DevOps.

## Por qué juntas

DDD da el **vocabulario y las fronteras**, TDD da la **red de seguridad y el diseño guiado por
pruebas**, y ODD mantiene el foco en el **contrato externo y en la trazabilidad**. La arquitectura
hexagonal es el esqueleto que permite que las tres convivan sin fricción.
