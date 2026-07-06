import json
from pathlib import Path


CONFIG_FILE = "config/mcp.json"


def list_mcps():

    try:

        config = json.loads(
            Path(CONFIG_FILE).read_text()
        )

        return {
            "servers":
            config["servers"]
        }

    except Exception as e:

        return {
            "error": str(e)
        }


def get_mcp_status():

    try:

        config = json.loads(
            Path(CONFIG_FILE).read_text()
        )

        status = []

        for server in config["servers"]:

            status.append(
                {
                    "name":
                    server["name"],
                    "enabled":
                    server["enabled"]
                }
            )

        return {
            "status": status
        }

    except Exception as e:

        return {
            "error": str(e)
        }


__all__ = [
    "list_mcps",
    "get_mcp_status"
]