from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, field
from typing import List

import orjson
import pandas as pd

from outputs.schema import SkoolItem

@dataclass
class Exporter:
    out_dir: str
    jsonl_name: str = "items.ndjson"
    json_name: str = "items.json"
    csv_name: str = "items.csv"
    _buffer: List[SkoolItem] = field(default_factory=list)

    def _path(self, name: str) -> str:
        return os.path.join(self.out_dir, name)

    def write(self, item: SkoolItem) -> None:
        # Stream NDJSON for large runs
        with open(self._path(self.jsonl_name), "ab") as f:
            f.write(orjson.dumps(item.model_dump()) + b"\n")
        self._buffer.append(item)

    def finalize(self) -> None:
        # Write JSON array
        with open(self._path(self.json_name), "wb") as f:
            f.write(orjson.dumps([i.model_dump() for i in self._buffer], option=orjson.OPT_INDENT_2))

        # Minimal CSV for a quick view
        rows = []
        for i in self._buffer:
            rows.append(
                {
                    "type": i.type.value,
                    "id": i.id,
                    "title": i.title or i.postTitle,
                    "url": i.url,
                    "createdAt": i.createdAt or "",
                    "commentsCount": i.metadata.get("comments", 0),
                    "upvotes": i.metadata.get("upvotes", 0),
                }
            )
        df = pd.DataFrame(rows)
        df.to_csv(self._path(self.csv_name), index=False)