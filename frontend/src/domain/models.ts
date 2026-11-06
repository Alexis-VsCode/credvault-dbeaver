// Capa de DOMINIO del frontend: tipos puros, sin React ni fetch.
// Reflejan el mismo lenguaje ubicuo que el backend (DDD).

export type LogLevel = "ok" | "info" | "warn" | "error";
export type InstallationKind = "store" | "installer" | "portable" | "unknown";

export interface Credential {
  user: string;
  password: string;
  has_password: boolean;
}

export interface Connection {
  id: string;
  name: string;
  installation_name: string;
  driver: string;
  host: string;
  port: string;
  database: string;
  endpoint: string;
  credential: Credential;
}

export interface Installation {
  name: string;
  kind: InstallationKind;
  workspace_path: string;
}

export interface LogEntry {
  level: LogLevel;
  message: string;
}

export interface RecoveryReport {
  installations: Installation[];
  connections: Connection[];
  log: LogEntry[];
  installations_count: number;
  connections_count: number;
  with_password_count: number;
}
