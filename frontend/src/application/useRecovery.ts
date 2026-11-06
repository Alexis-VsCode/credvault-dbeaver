// Caso de uso de la UI: orquesta el escaneo y expone estado observable.
// Recibe el puerto ApiClient por parámetro (DIP): en prod llega HttpApiClient,
// en demo DemoApiClient, en tests un fake. El hook no sabe cuál es.

import { useCallback, useState } from "react";
import type { ApiClient } from "@/application/ApiClient";
import type { RecoveryReport } from "@/domain/models";

export type ScanStatus = "idle" | "scanning" | "done" | "error";

export interface RecoveryState {
  status: ScanStatus;
  report: RecoveryReport | null;
  error: string | null;
  scan: () => Promise<void>;
}

export function useRecovery(api: ApiClient): RecoveryState {
  const [status, setStatus] = useState<ScanStatus>("idle");
  const [report, setReport] = useState<RecoveryReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  const scan = useCallback(async () => {
    setStatus("scanning");
    setError(null);
    try {
      const result = await api.recover();
      setReport(result);
      setStatus("done");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Error desconocido durante el escaneo.");
      setStatus("error");
    }
  }, [api]);

  return { status, report, error, scan };
}
