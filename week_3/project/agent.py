
import os
import json
import sys
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)

MODEL = "openai/gpt-oss-120b:free"

from tools.web import web_search, web_fetch
from tools.papers import paper_search, read_paper
from tools.files import write_file

SESSION_DIR = ".agent/sessions"


class Agent:

    def __init__(self):

        self.messages = []

        Path(SESSION_DIR).mkdir(
            parents=True,
            exist_ok=True
        )

        self.load_agents_md()

    def load_agents_md(self):

        try:

            content = Path(
                "AGENTS.md"
            ).read_text()

            self.messages.append(
                {
                    "role": "system",
                    "content": content
                }
            )

        except FileNotFoundError:
            pass

    def save_session(self):

        title = "latest"

        try:

            for msg in self.messages:

                if msg["role"] == "user":

                    title = (
                        msg["content"][:20]
                        .replace(" ", "_")
                        .replace("/", "_")
                        .replace("?", "")
                        .replace(":", "")
                    )

                    break

        except:
            pass

        path = (
            Path(SESSION_DIR)
            / f"{title}.json"
        )

        path.write_text(
            json.dumps(
                self.messages,
                indent=2
            )
        )

        latest = (
            Path(SESSION_DIR)
            / "latest.json"
        )

        latest.write_text(
            json.dumps(
                self.messages,
                indent=2
            )
        )

    def load_session(self):

        path = (
            Path(SESSION_DIR)
            / "latest.json"
        )

        if path.exists():

            self.messages = json.loads(
                path.read_text()
            )
    def resume_session(self, session_name):

        if not session_name.endswith(".json"):

            session_name += ".json"

        path = (
            Path(SESSION_DIR)
            / session_name
        )

        if path.exists():

            self.messages = json.loads(
                path.read_text()
            )

            return True

        return False

    def chat(self, question):

        web_results = web_search(
            question
        )

        paper_results = paper_search(
            question
        )

        paper_content = ""

        try:

            if paper_results:

                paper_id = (
                    paper_results[0]["paper"]["id"]
                )

                paper_content = read_paper(
                    paper_id
                )

        except Exception:
            pass

        context = f"""
WEB RESULTS:

{str(web_results)[:3000]}

PAPER RESULTS:

{str(paper_results)[:3000]}

PAPER CONTENT:

{str(paper_content)[:3000]}
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                *self.messages,
                {
                    "role": "user",
                    "content": f"""
Question:
{question}

Research Information:

{context}

Using the web results and paper results above,
provide a clear research answer.
"""
                }
            ]
        )

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        safe_name = (
            question[:30]
            .replace(" ", "_")
            .replace("/", "_")
        )

        write_file(
            f"notes/{safe_name}.md",
            answer
        )

        self.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        self.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        self.save_session()

        return answer


class REPLAgent(Agent):

    def run(self):

        self.load_session()

        while True:

            question = input(
                "\nQuestion: "
            )

            if question.lower() in [
                "quit",
                "exit"
            ]:
                break

            if question == "/sessions":

                sessions = list(
                    Path(
                        ".agent/sessions"
                    ).glob("*.json")
                )

                print("\nSaved Sessions:\n")

                for session in sessions:
                    print(session.name)

                continue

            if question.startswith("/resume "):

                session_name = question.replace(
                        "/resume ",
                        ""
                )
                

                if self.resume_session(
                    session_name
                ):

                    print(
                        f"Resumed {session_name}"
                    )

                else:

                    print(
                        "Session not found"
                    )

                continue

            answer = self.chat(
                question
            )

            print(answer)


if __name__ == "__main__":

    if "--tui" in sys.argv:

        from tui import ChatApp

        ChatApp().run()

    else:

        agent = REPLAgent()

        if len(sys.argv) > 1:

            question = " ".join(
                arg
                for arg in sys.argv[1:]
                if arg != "--tui"
            )

            print(
                agent.chat(question)
            )

        else:

            agent.run()

