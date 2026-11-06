// Selección del adaptador según el entorno (Composition Root del front).
// VITE_DEMO=1 → DemoApiClient (sin backend). Por defecto → HttpApiClient.

import type { ApiClient } from "@/application/ApiClient";
import { HttpApiClient } from "@/infrastructure/HttpApiClient";
import { DemoApiClient } from "@/infrastructure/DemoApiClient";

export function createApiClient(): ApiClient {
  const demo = import.meta.env.VITE_DEMO === "1";
  return demo ? new DemoApiClient() : new HttpApiClient();
}
