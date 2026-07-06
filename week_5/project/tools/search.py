import ast
import os
import re

WORKSPACE_ROOT = os.path.abspath(
    os.environ.get(
        "WORKSPACE_ROOT",
        "."
    )
)

MAX_GREP_RESULTS = 50

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build"
}


def resolve_path(path: str) -> str | None:

    abs_path = os.path.abspath(
        os.path.join(
            WORKSPACE_ROOT,
            path
        )
    )

    if not abs_path.startswith(
        WORKSPACE_ROOT
    ):
        return None

    return abs_path


def grep(
    pattern: str,
    path: str = ".",
    case_sensitive: bool = False,
    max_results: int = MAX_GREP_RESULTS,
) -> dict:

    root = resolve_path(path)

    if not root:
        return {
            "error": "Path escapes workspace"
        }

    flags = 0

    if not case_sensitive:
        flags = re.IGNORECASE

    matches = []
    total_matches = 0

    try:

        for dirpath, dirnames, filenames in os.walk(root):

            dirnames[:] = [
                d for d in dirnames
                if d not in EXCLUDE_DIRS
            ]

            for filename in filenames:

                file_path = os.path.join(
                    dirpath,
                    filename
                )

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        for line_no, line in enumerate(
                            f,
                            start=1
                        ):

                            if re.search(
                                pattern,
                                line,
                                flags
                            ):

                                total_matches += 1

                                if len(matches) < max_results:

                                    matches.append(
                                        {
                                            "file": os.path.relpath(
                                                file_path,
                                                WORKSPACE_ROOT
                                            ),
                                            "line": line_no,
                                            "text": line.strip()
                                        }
                                    )

                except Exception:
                    continue

        return {
            "matches": matches,
            "truncated":
                total_matches > max_results,
            "total_matches":
                total_matches
        }

    except Exception as e:

        return {
            "error": str(e)
        }


def list_definitions(path: str) -> dict:

    file_path = resolve_path(path)

    if not file_path:
        return {
            "error": "Path escapes workspace"
        }

    if not os.path.exists(file_path):
        return {
            "error": "File not found"
        }

    try:

        source = open(
            file_path,
            "r",
            encoding="utf-8"
        ).read()

        tree = ast.parse(source)

        definitions = []

        for node in tree.body:

            if isinstance(
                node,
                ast.FunctionDef
            ):

                definitions.append(
                    {
                        "kind": "function",
                        "name": node.name,
                        "line": node.lineno,
                        "end_line":
                            getattr(
                                node,
                                "end_lineno",
                                node.lineno
                            )
                    }
                )

            elif isinstance(
                node,
                ast.AsyncFunctionDef
            ):

                definitions.append(
                    {
                        "kind": "async function",
                        "name": node.name,
                        "line": node.lineno,
                        "end_line":
                            getattr(
                                node,
                                "end_lineno",
                                node.lineno
                            )
                    }
                )

            elif isinstance(
                node,
                ast.ClassDef
            ):

                definitions.append(
                    {
                        "kind": "class",
                        "name": node.name,
                        "line": node.lineno,
                        "end_line":
                            getattr(
                                node,
                                "end_lineno",
                                node.lineno
                            )
                    }
                )

                for child in node.body:

                    if isinstance(
                        child,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef
                        )
                    ):

                        definitions.append(
                            {
                                "kind": "method",
                                "name": child.name,
                                "line": child.lineno,
                                "end_line":
                                    getattr(
                                        child,
                                        "end_lineno",
                                        child.lineno
                                    )
                            }
                        )

        return {
            "definitions":
                definitions
        }

    except SyntaxError as e:

        return {
            "error":
                f"SyntaxError: {e}"
        }

    except Exception as e:

        return {
            "error": str(e)
        }


__all__ = [
    "grep",
    "list_definitions"
]