import os
import sys
import json
import uuid
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = "openai/gpt-oss-120b:free"

SESSIONS_DIR = ".agent/sessions"

os.makedirs(SESSIONS_DIR, exist_ok=True)


def resolve_path(path: str) -> str:
    return os.path.abspath(path)


def read_file(path: str, start_line: int = 1, read_lines: int = 200):
    try:
        with open(resolve_path(path), "r") as f:
            lines = f.readlines()

        end_line = start_line + read_lines

        return {
            "content": "".join(lines[start_line - 1:end_line - 1]),
            "has_more": end_line <= len(lines)
        }

    except Exception as e:
        return {"error": str(e)}


def write_file(path: str, content: str):
    try:
        with open(resolve_path(path), "w") as f:
            f.write(content)

        return {"status": "success"}

    except Exception as e:
        return {"error": str(e)}


def edit_file(
    path,
    operation,
    start_line,
    end_line=None,
    content=None,
):
    try:
        with open(resolve_path(path), "r") as f:
            lines = f.readlines()

        if operation == "append":
            lines.append(content + "\n")

        elif operation == "replace":
            lines[start_line - 1:end_line] = [content + "\n"]

        elif operation == "delete":
            del lines[start_line - 1:end_line]

        with open(resolve_path(path), "w") as f:
            f.writelines(lines)

        return {"status": "success"}

    except Exception as e:
        return {"error": str(e)}


def list_files(path=".", pattern="*"):
    try:
        files = os.listdir(resolve_path(path))
        return {"files": files}

    except Exception as e:
        return {"error": str(e)}


class Agent:

    def __init__(self):
        self.session_id = str(uuid.uuid4())[:8]

        self.messages = [
            {
                "role": "system",
                "content": build_system_prompt()
            }
        ]

    def save_session(self):
        with open(
            f"{SESSIONS_DIR}/{self.session_id}.json",
            "w"
        ) as f:
            json.dump(
                self.messages,
                f,
                indent=2
            )

    def chat(self, user_message):

        self.messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=self.messages
        )

        answer = response.choices[0].message.content

        self.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        self.save_session()

        return answer

    def run_once(self, prompt):
        return self.chat(prompt)

    def _emit(self, event, **data):
        pass


class REPLAgent(Agent):

    def run(self):

        print(
            f"Research Desk [{self.session_id}]"
        )

        while True:

            question = input("> ")

            if question.lower() in [
                "/quit",
                "/exit"
            ]:
                break

            print(
                self.chat(question)
            )


def build_system_prompt():

    prompt = (
        "You are Research Desk, a helpful research assistant."
    )

    if os.path.exists("AGENTS.md"):
        with open(
            "AGENTS.md",
            "r"
        ) as f:
            prompt += "\n\n" + f.read()

    return prompt


def main():

    agent = REPLAgent()

    if len(sys.argv) > 1:

        print(
            agent.run_once(
                " ".join(sys.argv[1:])
            )
        )

        return

    agent.run()


if __name__ == "__main__":
    main()