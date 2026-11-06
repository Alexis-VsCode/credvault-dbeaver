import { createApiClient } from "@/infrastructure/config";
import { ConsoleView } from "@/ui/pages/ConsoleView/ConsoleView";

// Composition Root de la UI: elige el adaptador una sola vez y lo inyecta.
const api = createApiClient();

export function App() {
  return <ConsoleView api={api} />;
}
