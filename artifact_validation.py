from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import validate


def _event_values(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "events":
                yield from child
            else:
                yield from _event_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from _event_values(child)


def validate_artifact(artifact: dict, schema_path: Path, known_events: set[str]) -> None:
    schema = json.loads(schema_path.read_text())
    validate(instance=artifact, schema=schema)
    unknown = sorted(set(_event_values(artifact)) - known_events)
    if unknown:
        raise ValueError(f"unknown transcript events: {', '.join(unknown)}")
