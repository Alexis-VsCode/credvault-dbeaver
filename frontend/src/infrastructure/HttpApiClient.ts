// Adaptador de infraestructura: implementa ApiClient con fetch real al backend.

import type { ApiClient } from "@/application/ApiClient";
import type { RecoveryReport } from "@/domain/models";

export class HttpApiClient implements ApiClient {
  constructor(private readonly baseUrl: string = "/api") {}

  async health(): Promise<boolean> {
    try {
      const res = await fetch(`${this.baseUrl}/health`);
      return res.ok;
    } catch {
      return false;
    }
  }

  async recover(): Promise<RecoveryReport> {
    const res = await fetch(`${this.baseUrl}/recover`, { method: "POST" });
    if (!res.ok) {
      throw new Error(`El backend respondió ${res.status}. ¿Está corriendo en el puerto 8000?`);
    }
    return (await res.json()) as RecoveryReport;
  }
}
