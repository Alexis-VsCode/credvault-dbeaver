// Capa de APLICACIÓN: el PUERTO que la UI consume.
// La UI depende de esta interfaz, no de fetch ni del backend (DIP).
// Implementaciones concretas viven en infrastructure/.

import type { RecoveryReport } from "@/domain/models";

export interface ApiClient {
  health(): Promise<boolean>;
  recover(): Promise<RecoveryReport>;
}
