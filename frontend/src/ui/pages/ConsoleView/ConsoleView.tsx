import type { ApiClient } from "@/application/ApiClient";
import { useRecovery } from "@/application/useRecovery";
import { Navbar } from "@/ui/components/Navbar/Navbar";
import { ScanSidebar } from "@/ui/components/ScanSidebar/ScanSidebar";
import { ResultsPanel } from "@/ui/components/ResultsPanel/ResultsPanel";
import "./ConsoleView.css";

interface ConsoleViewProps {
  api: ApiClient;
}

export function ConsoleView({ api }: ConsoleViewProps) {
  const { status, report, error, scan } = useRecovery(api);

  return (
    <div className="console">
      <Navbar onScan={scan} scanning={status === "scanning"} />
      <div className="console__body">
        <ScanSidebar installations={report?.installations ?? []} log={report?.log ?? []} />
        <main className="console__main">
          <ResultsPanel report={report} error={error} />
        </main>
      </div>
    </div>
  );
}
