import { useState } from "react";
import type { Connection } from "@/domain/models";
import "./CredentialRow.css";

interface CredentialRowProps {
  connection: Connection;
}

export function CredentialRow({ connection }: CredentialRowProps) {
  const [revealed, setRevealed] = useState(false);
  const [copied, setCopied] = useState(false);
  const { credential } = connection;

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(credential.password);
      setCopied(true);
      setTimeout(() => setCopied(false), 1200);
    } catch {
      /* clipboard puede fallar fuera de https; se ignora silenciosamente */
    }
  };

  const shown = credential.has_password
    ? revealed
      ? credential.password
      : "•".repeat(Math.max(credential.password.length, 7))
    : "(sin contraseña)";

  return (
    <div className="cred-row">
      <div className="cred-row__meta">
        <div className="cred-row__name">{connection.name}</div>
        <div className="cred-row__sub">
          {credential.user} @ {connection.endpoint || "—"} · {connection.installation_name}
        </div>
      </div>
      <div className="cred-row__secret">
        <span className={`cred-row__pwd ${revealed ? "cred-row__pwd--open" : ""}`}>{shown}</span>
        {credential.has_password && (
          <>
            <button
              className="cred-row__icon"
              onClick={() => setRevealed((v) => !v)}
              aria-label={revealed ? "Ocultar contraseña" : "Revelar contraseña"}
            >
              {revealed ? "🙈" : "👁"}
            </button>
            <button className="cred-row__icon" onClick={copy} aria-label="Copiar contraseña">
              {copied ? "✓" : "⧉"}
            </button>
          </>
        )}
      </div>
    </div>
  );
}
