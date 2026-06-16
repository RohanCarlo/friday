import json
import os
from datetime import date

_MEMORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "memory.json")


def _load() -> list[dict]:
    if not os.path.exists(_MEMORY_FILE):
        return []
    with open(_MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(memories: list[dict]):
    with open(_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=2, ensure_ascii=False)


def remember(key: str, value: str) -> str:
    memories = _load()
    key_lower = key.lower().strip()
    for m in memories:
        if m["key"].lower() == key_lower:
            m["value"] = value
            m["updated_at"] = str(date.today())
            _save(memories)
            return f"Updated: '{key}' is now '{value}'."
    memories.append({"key": key.strip(), "value": value, "saved_at": str(date.today())})
    _save(memories)
    return f"Got it. I'll remember that {key}: {value}."


def recall(query: str = "") -> str:
    memories = _load()
    if not memories:
        return "I don't have any memories stored yet."
    if query:
        q = query.lower()
        matches = [m for m in memories if q in m["key"].lower() or q in m["value"].lower()]
        if not matches:
            return f"Nothing stored about '{query}'."
        return ". ".join(f"{m['key']}: {m['value']}" for m in matches)
    return ". ".join(f"{m['key']}: {m['value']}" for m in memories)


def forget(key: str) -> str:
    memories = _load()
    before = len(memories)
    memories = [m for m in memories if m["key"].lower() != key.lower().strip()]
    if len(memories) == before:
        return f"Nothing stored under '{key}'."
    _save(memories)
    return f"Done. Forgotten '{key}'."


def get_memory_context() -> str:
    """Compact summary injected into the system prompt on every request."""
    memories = _load()
    if not memories:
        return ""
    lines = [f"- {m['key']}: {m['value']}" for m in memories]
    return "What you know about the user (long-term memory):\n" + "\n".join(lines)
