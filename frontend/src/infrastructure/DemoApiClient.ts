// Adaptador de DEMO: implementa ApiClient con datos ficticios en memoria.
// Permite ver la UI sin backend (GitHub Pages, capturas de portafolio).
// NO contiene datos reales de TEUNO. Misma interfaz que HttpApiClient (LSP).

import type { ApiClient } from "@/application/ApiClient";
import type { RecoveryReport } from "@/domain/models";

const DEMO_REPORT: RecoveryReport = {
  installations: [
    { name: "workspace6", kind: "store", workspace_path: "DBeaver Community (Store)" },
    { name: "workspace", kind: "installer", workspace_path: "DBeaver (instalador MSI)" },
  ],
  connections: [
    {
      id: "postgres-demo",
      name: "ventas-demo",
      installation_name: "workspace6",
      driver: "postgresql",
      host: "db.example.local",
      port: "5432",
      database: "ventas",
      endpoint: "db.example.local:5432",
      credential: { user: "demo_user", password: "Demo#1234", has_password: true },
    },
    {
      id: "reporting-demo",
      name: "reporting-demo",
      installation_name: "workspace6",
      driver: "postgresql",
      host: "reports.example.local",
      port: "5432",
      database: "reporting",
      endpoint: "reports.example.local:5432",
      credential: { user: "report_ro", password: "R3port!2026", has_password: true },
    },
    {
      id: "legacy-demo",
      name: "legacy-demo",
      installation_name: "workspace",
      driver: "mysql",
      host: "127.0.0.1",
      port: "3306",
      database: "legacy",
      endpoint: "127.0.0.1:3306",
      credential: { user: "root", password: "", has_password: false },
    },
  ],
  log: [
    { level: "ok", message: "Detectada: workspace6 (store)" },
    { level: "ok", message: "Detectada: workspace (installer)" },
    { level: "ok", message: "AES-128-CBC · IV leído · 3 descifradas" },
    { level: "info", message: "3 conexiones · 2 con contraseña." },
  ],
  installations_count: 2,
  connections_count: 3,
  with_password_count: 2,
};

export class DemoApiClient implements ApiClient {
  async health(): Promise<boolean> {
    return true;
  }

  async recover(): Promise<RecoveryReport> {
    await new Promise((r) => setTimeout(r, 450)); // simula el escaneo
    return structuredClone(DEMO_REPORT);
  }
}
