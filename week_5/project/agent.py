

from tools.exec import run_command
from tools.search import grep, list_definitions
from tools.plan import (
    add_todos,
    get_todos,
    mark_todo,
    verify_todo
)
from tools.skills import (
    list_skills,
    load_skill
)
from tools.mcp import (
    list_mcps,
    get_mcp_status
)
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
TARGET_REPO = "target_repo"

def sanitize_repo_text(text):

    blocked_phrases = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "delete all files",
        "reveal system prompt",
        "show secrets",
        "ignore system message"
    ]

    lower = text.lower()

    for phrase in blocked_phrases:

        if phrase in lower:

            return (
                "[POTENTIAL PROMPT "
                "INJECTION REMOVED]"
            )

    return text


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
        
        todo_title = question[:50]
        active_skill = getattr(
            self,
            "active_skill",
            ""
        )

        add_todos([
            {
                "title": todo_title,
                "description": question,
                "verification": "git status",
                "status": "pending"
            }
        ])

        try:

            search_term = question.split()[0]

        except Exception:

            search_term = "def"

        repo_search = grep(
            search_term,
            path=TARGET_REPO,
            max_results=5
        )

        repo_status = run_command(
            "git status",
            cwd=TARGET_REPO
        )

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

        context = sanitize_repo_text(
            f"""
        WEB RESULTS:

        {str(web_results)[:3000]}

        PAPER RESULTS:

        {str(paper_results)[:3000]}

        PAPER CONTENT:

        {str(paper_content)[:3000]}

        REPOSITORY SEARCH:

        {str(repo_search)[:1500]}

        REPOSITORY STATUS:

        {str(repo_status)[:1000]}
        """
        )

        try:

            active_skill = ""
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    *self.messages,
                    {
                        "role": "user",
                        "content": f"""
        Question:
        {question}

        Active Skill:
        {active_skill}

        Research Information:

        {context}

        Using the web results and paper results above,
        provide a clear research answer.
        """
                    }
                ]
            )

        except Exception as e:

            return f"Model request failed: {e}"

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

        if verify_todo(
            "git status"
        ):

            mark_todo(
                todo_title,
                "completed",
                evidence="git status exit code 0"
            )

        else:

            mark_todo(
                todo_title,
                "failed"
            )
        pending = get_todos(
            status="pending"
        )

        if pending["todos"]:

            return (
                "Task not complete. "
                "Pending todos remain."
            )

        return answer


class REPLAgent(Agent):

    def run(self):

        self.load_session()
        self.active_skill = ""

        while True:

            question = input(
                "\nQuestion: "
            )

            if question.lower() in [
                "quit",
                "exit"
            ]:
                break

            # Skills

            if question == "/skills":

                print(
                    list_skills()
                )

                continue

            if question.startswith(
                "/load_skill "
            ):

                skill_name = (
                    question.replace(
                        "/load_skill ",
                        ""
                    )
                )

                result = load_skill(
                    skill_name
                )

                if "content" in result:

                    self.active_skill = (
                        result["content"]
                    )

                    print(
                        f"Loaded skill: {skill_name}"
                    )

                else:

                    print(result)

                continue

            # MCP

            if question == "/mcp":

                print(
                    get_mcp_status()
                )

                continue

            if question == "/mcp_list":

                print(
                    list_mcps()
                )

                continue

            # Sessions

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

