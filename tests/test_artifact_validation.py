import json
from pathlib import Path

from artifact_validation import validate_artifact


ROOT = Path(__file__).parents[1]


def test_structured_schema_accepts_atomic_sourced_claim() -> None:
    artifact = {
        "sections": [
            {"name": "Objective", "claims": [{"text": "A claim", "events": ["event-9"]}]}
        ]
    }
    validate_artifact(artifact, ROOT / "schemas/structured-handoff.schema.json", {"event-9"})


def test_unknown_event_is_rejected() -> None:
    artifact = {
        "sections": [
            {"name": "Objective", "claims": [{"text": "A claim", "events": ["event-999"]}]}
        ]
    }
    try:
        validate_artifact(artifact, ROOT / "schemas/structured-handoff.schema.json", {"event-9"})
    except ValueError as error:
        assert "event-999" in str(error)
    else:
        raise AssertionError("unknown event was accepted")
