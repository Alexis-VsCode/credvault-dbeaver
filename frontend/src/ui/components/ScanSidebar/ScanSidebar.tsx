import type { Installation, LogEntry } from "@/domain/models";
import { LogPanel } from "@/ui/components/LogPanel/LogPanel";
import "./ScanSidebar.css";

interface ScanSidebarProps {
  installations: Installation[];
  log: LogEntry[];
}

export function ScanSidebar({ installations, log }: ScanSidebarProps) {
  return (
    <aside className="sidebar">
      <div className="sidebar__label">Instalaciones detectadas</div>
      {installations.length === 0 && <div className="sidebar__empty">Sin escanear.</div>}
      {installations.map((inst) => (
        <div key={inst.workspace_path} className="sidebar__item">
          <span className="sidebar__check" aria-hidden="true">
            ✓
          </span>
          <span>
            {inst.name} · {inst.kind}
          </span>
        </div>
      ))}

      <div className="sidebar__label sidebar__label--log">Log</div>
      <LogPanel entries={log} />
    </aside>
  );
}
