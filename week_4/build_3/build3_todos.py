import json
from pathlib import Path

TODO_FILE = ".agent/todos.json"

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


if __name__ == "__main__":

    add_todos(
        [
            {
                "title":
                    "Fix login bug",
                "description":
                    "Investigate login failure",
                "verification":
                    "pytest tests/test_login.py",
                "status":
                    "pending"
            },
            {
                "title":
                    "Run tests",
                "description":
                    "Run project tests",
                "verification":
                    "pytest",
                "status":
                    "pending"
            }
        ]
    )

    print(get_todos())

    print(
        mark_todo(
            "Fix login bug",
            "in_progress"
        )
    )

    print(
        mark_todo(
            "Fix login bug",
            "completed"
        )
    )

    print(
        mark_todo(
            "Fix login bug",
            "completed",
            evidence="pytest passed"
        )
    )

    print(get_todos())