"""Adaptador: lee metadatos de conexión desde data-sources.json (texto plano).

DBeaver guarda el nombre, driver, host, puerto y base de cada conexión en
`data-sources.json`, indexado por el mismo connection_id que usa el archivo
de credenciales. Unir ambos da la foto completa: nombre + host + user + pass.

Implementa MetadataReaderPort.
"""
from __future__ import annotations

import json

from credvault.application.ports import MetadataReaderPort


class JsonDataSourcesReader(MetadataReaderPort):
    def read(self, data_sources_file: str) -> dict:
        with open(data_sources_file, "r", encoding="utf-8") as fh:
            raw = json.load(fh)

        connections = raw.get("connections", {}) if isinstance(raw, dict) else {}
        result: dict[str, dict] = {}
        for conn_id, node in connections.items():
            cfg = node.get("configuration", {}) if isinstance(node, dict) else {}
            result[conn_id] = {
                "name": node.get("name", conn_id),
                "driver": node.get("driver", ""),
                "host": cfg.get("host", ""),
                "port": cfg.get("port", ""),
                "database": cfg.get("database", ""),
            }
        return result
