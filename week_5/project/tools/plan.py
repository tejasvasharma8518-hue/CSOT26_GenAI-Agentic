import json
from pathlib import Path

TODO_FILE = ".agent/todos.json"

VALID_STATUSES = {
    "pending",
    "in_progress",
    "blocked",
    "failed",
    "completed"
}

Path(".agent").mkdir(
    parents=True,
    exist_ok=True
)


def load_todos():

    if Path(TODO_FILE).exists():

        return json.loads(
            Path(TODO_FILE).read_text()
        )

    return []


def save_todos(todos):

    Path(TODO_FILE).write_text(
        json.dumps(
            todos,
            indent=2
        )
    )


def add_todos(todos):

    current = load_todos()

    current.extend(todos)

    save_todos(current)

    return {
        "success": True,
        "count": len(current)
    }


def get_todos(status=None):

    todos = load_todos()

    if status:

        todos = [
            t for t in todos
            if t["status"] == status
        ]

    return {
        "todos": todos
    }


def mark_todo(
    title,
    status,
    evidence=None
):

    todos = load_todos()

    if status not in VALID_STATUSES:

        return {
            "error": f"Invalid status: {status}"
        }

    for todo in todos:

        if todo["title"] == title:

            if (
                status == "completed"
                and not evidence
            ):
                return {
                    "error":
                    "Evidence required to complete todo"
                }

            todo["status"] = status

            if evidence:
                todo["evidence"] = evidence

            save_todos(todos)

            return {
                "success": True
            }

    return {
        "error": "Todo not found"
    }
def verify_todo(
    verification_command
):

    from tools.exec import run_command

    result = run_command(
        verification_command
    )

    return (
        result.get(
            "exit_code"
        ) == 0
    )


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_todos",
            "description":
                "Add one or more todos. Every todo must contain a title, description, verification method and status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "todos": {
                        "type": "array"
                    }
                },
                "required": ["todos"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_todos",
            "description":
                "Get current todo list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mark_todo",
            "description":
                "Update a todo status. Completing a todo requires evidence.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string"
                    },
                    "status": {
                        "type": "string"
                    },
                    "evidence": {
                        "type": "string"
                    }
                },
                "required": [
                    "title",
                    "status"
                ]
            }
        }
    }
]


__all__ = [
    "add_todos",
    "get_todos",
    "mark_todo",
    "verify_todo"
]