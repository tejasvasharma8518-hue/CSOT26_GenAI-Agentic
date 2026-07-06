import os
from openai import OpenAI
from dotenv import load_dotenv
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Input, RichLog

from agent import REPLAgent

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = "openai/gpt-oss-120b:free"
MAX_HISTORY_TURNS = 20


def trim_history(messages: list[dict], max_turns: int) -> list[dict]:

    if len(messages) <= 1:
        return messages

    system_message = messages[0]

    history = messages[1:]

    max_entries = max_turns * 2

    history = history[-max_entries:]

    return [system_message] + history


class ChatApp(App):

    TITLE = "Research Desk TUI"

    CSS = """
    Screen {
        layout: vertical;
    }

    RichLog {
        height: 1fr;
        border: solid $primary;
        padding: 0 1;
    }

    Input {
        dock: bottom;
        height: 3;
    }
    """

    BINDINGS = [
        Binding("ctrl+l", "clear_display", "Clear display"),
        Binding("ctrl+k", "clear_history", "Clear history"),
        Binding("ctrl+q", "quit_app", "Quit"),
    ]

    def __init__(self):
        super().__init__()

        self.agent = REPLAgent()

        self.messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ]

    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)

        yield RichLog(
            id="log",
            wrap=True
        )

        yield Input(
            placeholder="Ask a research question..."
        )

        yield Footer()

    def on_mount(self) -> None:

        log = self.query_one(
            "#log",
            RichLog
        )

        log.write(
            "Research Desk Ready\n"
            "Ctrl+L = Clear Display | "
            "Ctrl+K = Clear History | "
            "Ctrl+Q = Quit\n"
        )

        self.query_one(Input).focus()

    def on_input_submitted(
        self,
        event: Input.Submitted
    ) -> None:

        user_text = event.value.strip()

        if user_text.lower() in [
            "quit",
            "exit"
        ]:
            self.exit()
            return

        if not user_text:
            return

        event.input.clear()

        log = self.query_one(
            "#log",
            RichLog
        )

        log.write(
            f"[You] {user_text}\n"
        )

        self.messages.append(
            {
                "role": "user",
                "content": user_text
            }
        )

        self.messages = trim_history(
            self.messages,
            MAX_HISTORY_TURNS
        )

        self.run_worker(
            self._get_response(),
            thread=True
        )

    async def _get_response(self) -> None:

        log = self.query_one(
            "#log",
            RichLog
        )

        try:

            latest_question = self.messages[-1]["content"]

            reply = self.agent.chat(
                latest_question
            )

            self.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

            self.messages = trim_history(
                self.messages,
                MAX_HISTORY_TURNS
            )

            self.call_from_thread(
                log.write,
                f"[Agent] {reply}\n"
            )

        except Exception as e:

            self.call_from_thread(
                log.write,
                f"[Error] {e}\n"
            )

    def action_clear_display(self) -> None:

        log = self.query_one(
            "#log",
            RichLog
        )

        log.clear()

    def action_clear_history(self) -> None:

        self.messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ]

        log = self.query_one(
            "#log",
            RichLog
        )

        log.clear()

        log.write(
            "History cleared.\n"
        )

    def action_quit_app(self) -> None:

        self.exit()


if __name__ == "__main__":

    ChatApp().run()