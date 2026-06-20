from pathlib import Path


def list_files(path="."):

    try:

        files = [
            str(p)
            for p in Path(path).glob("*")
        ]

        return {
            "content": files
        }

    except Exception as e:

        return {
            "error": str(e)
        }


def write_file(path, content):

    try:

        Path(path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        Path(path).write_text(content)

        return {
            "content": f"Wrote {path}"
        }

    except Exception as e:

        return {
            "error": str(e)
        }


def read_file(
    path,
    start_line=1,
    read_lines=50
):

    try:

        lines = Path(path).read_text().splitlines()

        start_index = max(
            start_line - 1,
            0
        )

        end_index = start_index + read_lines

        selected = lines[
            start_index:end_index
        ]

        numbered = []

        for i, line in enumerate(
            selected,
            start=start_line
        ):
            numbered.append(
                f"{i}: {line}"
            )

        return {
            "content": "\n".join(numbered),
            "has_more": end_index < len(lines)
        }

    except Exception as e:

        return {
            "error": str(e)
        }


def edit_file(
    path,
    operation,
    content="",
    start_line=None,
    end_line=None
):

    try:

        file_path = Path(path)

        if not file_path.exists():

            return {
                "error": "File not found"
            }

        lines = file_path.read_text().splitlines()

        if operation == "append":

            lines.append(content)

            diff = f"+ {content}"

        elif operation == "replace":

            if start_line is None:
                return {
                    "error": "start_line required"
                }

            index = start_line - 1

            if index >= len(lines):
                return {
                    "error": "Line out of range"
                }

            old_line = lines[index]

            lines[index] = content

            diff = (
                f"- {old_line}\n"
                f"+ {content}"
            )

        elif operation == "delete":

            if start_line is None:
                return {
                    "error": "start_line required"
                }

            if end_line is None:
                end_line = start_line

            deleted = lines[
                start_line - 1:end_line
            ]

            del lines[
                start_line - 1:end_line
            ]

            diff = "\n".join(
                f"- {x}"
                for x in deleted
            )

        else:

            return {
                "error": "Invalid operation"
            }

        file_path.write_text(
            "\n".join(lines)
        )

        return {
            "content": "File updated",
            "diff": diff
        }

    except Exception as e:

        return {
            "error": str(e)
        }