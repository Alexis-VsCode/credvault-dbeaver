import type { LogEntry } from "@/domain/models";
import "./LogPanel.css";

interface LogPanelProps {
  entries: LogEntry[];
}

export function LogPanel({ entries }: LogPanelProps) {
  if (entries.length === 0) {
    return <div className="log log--empty">—</div>;
  }
  return (
    <div className="log">
      {entries.map((e, i) => (
        <div key={i} className="log__line">
          <span className={`log__tag log__tag--${e.level}`}>{e.level}</span>
          <span>{e.message}</span>
        </div>
      ))}
    </div>
  );
}
