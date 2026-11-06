import type { RecoveryReport } from "@/domain/models";
import { CredentialRow } from "@/ui/components/CredentialRow/CredentialRow";
import "./ResultsPanel.css";

interface ResultsPanelProps {
  report: RecoveryReport | null;
  error: string | null;
}

export function ResultsPanel({ report, error }: ResultsPanelProps) {
  if (error) {
    return <div className="results results__error">⚠ {error}</div>;
  }
  if (!report) {
    return (
      <div className="results results__empty">
        Presiona <strong>Escanear</strong> para recuperar las credenciales de DBeaver.
      </div>
    );
  }
  return (
    <div className="results">
      <div className="results__stats">
        <Stat label="Instalaciones" value={report.installations_count} />
        <Stat label="Conexiones" value={report.connections_count} />
        <Stat label="Con contraseña" value={report.with_password_count} accent />
      </div>
      <div className="results__label">Credenciales recuperadas · {report.connections_count}</div>
      <div className="results__list">
        {report.connections.map((c) => (
          <CredentialRow key={`${c.installation_name}-${c.id}`} connection={c} />
        ))}
      </div>
    </div>
  );
}

function Stat({ label, value, accent }: { label: string; value: number; accent?: boolean }) {
  return (
    <div className="stat">
      <div className="stat__label">{label}</div>
      <div className={`stat__value ${accent ? "stat__value--accent" : ""}`}>{value}</div>
    </div>
  );
}
