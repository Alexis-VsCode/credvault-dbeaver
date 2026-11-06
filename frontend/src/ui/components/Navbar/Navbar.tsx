import "./Navbar.css";

interface NavbarProps {
  onScan: () => void;
  scanning: boolean;
}

export function Navbar({ onScan, scanning }: NavbarProps) {
  return (
    <header className="navbar">
      <div className="navbar__brand">
        <span className="navbar__logo" aria-hidden="true">
          ◇
        </span>
        <span className="navbar__title">TEUNO · CredVault DBeaver</span>
      </div>
      <button className="btn-primary" onClick={onScan} disabled={scanning}>
        {scanning ? "Escaneando…" : "Escanear"}
      </button>
    </header>
  );
}
