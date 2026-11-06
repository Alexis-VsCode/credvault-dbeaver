# Manual de usuario

CredVault te ayuda a **recuperar las contraseñas de tus conexiones de DBeaver** cuando las
olvidaste. Funciona sobre tu propia máquina.

> Antes de empezar: **cierra DBeaver** para que el archivo de credenciales no esté en uso.

---

## Opción A — Consola web (recomendada)

1. Abre una terminal y levanta el backend:
   ```bash
   cd backend
   pip install -e .
   uvicorn credvault.infrastructure.api.main:app --port 8000
   ```
2. En otra terminal, levanta la interfaz:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Abre tu navegador en **http://localhost:5173**.
4. Pulsa **Escanear**. Verás:
   - a la izquierda, las instalaciones de DBeaver detectadas y el *log* del proceso;
   - a la derecha, cada conexión con su usuario y la contraseña enmascarada.
5. En cada fila:
   - 👁 **revela** u oculta la contraseña;
   - ⧉ **copia** la contraseña al portapapeles.

### ¿Solo quieres ver cómo se ve, sin DBeaver?

Levanta todo en **modo demo** (datos de ejemplo, ninguna credencial real):

```bash
# backend
CREDVAULT_DEMO=1 uvicorn credvault.infrastructure.api.main:app --port 8000
# frontend (alternativa sin backend)
VITE_DEMO=1 npm run dev
```

---

## Opción B — Línea de comandos

```bash
cd backend
pip install -e .
credvault           # muestra las contraseñas enmascaradas
credvault --show    # muestra las contraseñas en claro
```

---

## Preguntas frecuentes

**No aparece ninguna instalación.**
Revisa que DBeaver esté instalado para tu usuario. Las rutas típicas en Windows 11 son:
`%APPDATA%\DBeaverData\...` (instalador) y
`%LOCALAPPDATA%\Packages\DBeaverCorp.DBeaverCE_*\...` (Microsoft Store).

**Dice que un workspace tiene "contraseña maestra".**
Ese almacén está cifrado con una clave que tú definiste en DBeaver; la clave pública no sirve y
CredVault no puede leerlo. Tendrías que recordarla desde DBeaver.

**¿Es seguro?**
La herramienta solo lee archivos locales a los que tu usuario ya tiene acceso y no envía nada a
ningún servidor. Aun así, úsala solo en equipos tuyos o con permiso.
