"""Adaptador de entrada (driving): CLI.

Mismo caso de uso que la API, otra entrada (ODD / outside-in: el caso de uso
es el centro, las entradas son intercambiables). Imprime una tabla y el log.
"""
from __future__ import annotations

import argparse

from credvault.infrastructure.api.deps import build_recover_use_case


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="credvault",
        description="Recupera credenciales de DBeaver guardadas en tu propia máquina.",
    )
    parser.add_argument("--show", action="store_true", help="Muestra las contraseñas en claro.")
    args = parser.parse_args(argv)

    report = build_recover_use_case().execute()

    print(f"\nInstalaciones: {report.installations_count}  |  "
          f"Conexiones: {report.connections_count}  |  "
          f"Con contraseña: {report.with_password_count}\n")

    for c in report.connections:
        pwd = c.credential.password if args.show else "•" * len(c.credential.password)
        print(f"  [{c.installation_name}] {c.name}")
        print(f"      {c.endpoint}  user={c.credential.user}  pass={pwd}")

    print("\nLog:")
    for e in report.log:
        print(f"  {e.level.value:5} {e.message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
