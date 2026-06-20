import json
import os
import uuid
from datetime import datetime, timezone

SESSIONS_DIR = ".agent/sessions"
AGENTS_PATHS = ("AGENTS.md", ".agent/AGENTS.md")

BASE_PROMPT = "You are Research Desk, a helpful research assistant."


def create_session() -> str:
    """Return a new 8-char hex session ID."""
    os.makedirs(SESSIONS_DIR, exist_ok=True)

    session_id = uuid.uuid4().hex[:8]

    return session_id


def save_session(session_id: str, messages: list, title: str = "Untitled") -> None:
    """Write session JSON to .agent/sessions/{id}.json"""

    os.makedirs(SESSIONS_DIR, exist_ok=True)

    session_data = {
        "id": session_id,
        "title": title,
        "messages": messages,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    filepath = os.path.join(
        SESSIONS_DIR,
        f"{session_id}.json"
    )

    with open(filepath, "w") as f:
        json.dump(
            session_data,
            f,
            indent=2
        )


def load_session(session_id: str) -> dict:
    """Load and return session dict including messages list."""

    filepath = os.path.join(
        SESSIONS_DIR,
        f"{session_id}.json"
    )

    with open(filepath, "r") as f:
        return json.load(f)


def list_sessions() -> list[dict]:
    """Return sessions sorted by updated_at descending."""

    if not os.path.exists(SESSIONS_DIR):
        return []

    sessions = []

    for filename in os.listdir(SESSIONS_DIR):

        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(
            SESSIONS_DIR,
            filename
        )

        with open(filepath, "r") as f:
            data = json.load(f)

            sessions.append(
                {
                    "id": data["id"],
                    "title": data["title"],
                    "updated_at": data["updated_at"],
                }
            )

    sessions.sort(
        key=lambda x: x["updated_at"],
        reverse=True
    )

    return sessions


def build_system_prompt() -> str:
    """Base prompt + AGENTS.md if it exists."""

    prompt = BASE_PROMPT

    for path in AGENTS_PATHS:

        if os.path.exists(path):

            with open(path, "r") as f:
                agents_text = f.read()

            prompt += "\n\nAGENTS.md Rules:\n"
            prompt += agents_text

            break

    return prompt


if __name__ == "__main__":

    sid = create_session()

    messages = [
        {
            "role": "system",
            "content": build_system_prompt()
        },
        {
            "role": "user",
            "content": "What is a surface code?"
        },
        {
            "role": "assistant",
            "content": "A surface code is a type of quantum error correcting code."
        },
    ]

    save_session(
        sid,
        messages,
        title="Quantum error correction"
    )

    print(f"Saved session: {sid}")

    print("\nAll Sessions:")
    print(list_sessions())

    print("\nLoaded Session:")
    print(load_session(sid))