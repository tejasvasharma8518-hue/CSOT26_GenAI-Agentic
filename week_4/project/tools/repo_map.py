import os
from tools.search import list_definitions


def build_repo_map(root):

    repo_map = {}

    for dirpath, _, filenames in os.walk(root):

        for filename in filenames:

            if filename.endswith(".py"):

                path = os.path.join(
                    dirpath,
                    filename
                )

                result = list_definitions(
                    path
                )

                if (
                    "definitions"
                    in result
                ):

                    repo_map[path] = [
                        item["name"]
                        for item in result[
                            "definitions"
                        ]
                    ]

    return repo_map