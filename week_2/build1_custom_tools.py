"""
Build 1: Custom Tool Call Parser
=================================
Before modern SDKs handled tool calls natively, developers used custom text formats
that the model was prompted to emit. This build has you implement that pattern from
scratch: prompt the model to emit tool calls in a structured format, parse them, run
the corresponding Python function, and feed the result back.

This is NOT the production way to do it (Build 2 is). But doing it manually first
makes the mechanics obvious. The SDK is doing exactly this, just more robustly.

The format we'll use:
    The model emits tool calls wrapped in <tool_call> tags, like:

        I need to read the file first.

        <tool_call>
        {"name": "read_file", "arguments": {"path": "notes.txt"}}
        </tool_call>

    Your code finds the tag, parses the JSON, runs the function, and injects
    the result back as a <tool_response> in the next message.

Tasks:
  1. Complete `parse_tool_call` to extract name + arguments from a model response
  2. Complete `dispatch` to route a tool call to the right Python function
  3. Complete `run_agent` to implement the back-and-forth loop

Tools to implement:
  - read_file(path: str) -> dict    reads a file from disk and returns its content
  - write_file(path: str, content: str) -> dict    writes content to a file on disk

Before running, create a file called `sample.txt` with some text in it.
"""

import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = "openai/gpt-oss-120b:free"

SYSTEM_PROMPT = """You are a helpful file assistant with access to the following tools:

- read_file(path: str): reads a file from disk and returns its content
- write_file(path: str, content: str): writes content to a file on disk

When you need to use a tool, emit EXACTLY this format and nothing else after it:

<tool_call>
{"name": "TOOL_NAME", "arguments": {"arg1": "value1"}}
</tool_call>

After you receive the tool result in a <tool_response> block, continue your response
normally. Do not emit a tool_call and prose in the same turn. Pick one or the other.
"""

# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def read_file(path: str) -> dict:
    try:
        with open(path, "r") as f:
            content = f.read()

        return {
            "content": content,
            "path": path
        }

    except Exception as e:
        return {
            "error": str(e)
        }


def write_file(path: str, content: str) -> dict:
    try:
        with open(path, "w") as f:
            bytes_written = f.write(content)

        return {
            "success": True,
            "path": path,
            "bytes_written": bytes_written
        }

    except Exception as e:
        return {
            "error": str(e)
        }


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def parse_tool_call(response_text: str) -> dict | None:
    match = re.search(
        r"<tool_call>(.*?)</tool_call>",
        response_text,
        re.DOTALL
    )

    if not match:
        return None

    try:
        return json.loads(match.group(1).strip())

    except json.JSONDecodeError:
        return None


def strip_tool_call(response_text: str) -> str:
    return re.sub(
        r"<tool_call>.*?</tool_call>",
        "",
        response_text,
        flags=re.DOTALL
    ).strip()


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

TOOL_REGISTRY = {
    "read_file": read_file,
    "write_file": write_file,
}

def dispatch(name: str, arguments: dict) -> str:
    tool = TOOL_REGISTRY.get(name)

    if tool is None:
        return json.dumps({
            "error": f"Unknown tool: {name}"
        })

    try:
        result = tool(**arguments)
        return json.dumps(result)

    except Exception as e:
        return json.dumps({
            "error": str(e)
        })


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

MAX_ITERATIONS = 6

def run_agent(user_message: str) -> str:
    """
    Run the tool-calling agent loop for a single user message.

    Steps:
      1. Build the initial messages list with SYSTEM_PROMPT + user message.
      2. Call the model.
      3. Parse the response for a <tool_call>.
      4. If found: run the tool, inject a <tool_response> block into messages, go to 2.
      5. If not found: return the model's text (the final answer).
      6. If MAX_ITERATIONS reached: return an error string.

    The <tool_response> you inject back should look like:
        <tool_response>
        {"content": "Hello, world!", "path": "sample.txt"}
        </tool_response>

    Wrap it in a user message so the model sees it as a continuation:
        {"role": "user", "content": "<tool_response>\n...\n</tool_response>"}

    Print a line to stderr each time a tool is called so you can follow the loop.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for iteration in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        response_text = response.choices[0].message.content

        tool_call = parse_tool_call(response_text)

        if tool_call is None:
            return strip_tool_call(response_text)

        name = tool_call["name"]
        arguments = tool_call["arguments"]

        print(
            f"[Tool Call] {name} {arguments}",
            file=os.sys.stderr
        )

        tool_result = dispatch(
            name,
            arguments
        )

        messages.append(
            {
            "role": "assistant",
            "content": response_text
            }
        )

        messages.append(
            {
                "role": "user",
                "content":
                    f"<tool_response>\n"
                    f"{tool_result}\n"
                    f"</tool_response>"
            }
        )

    return f"[Agent stopped after {MAX_ITERATIONS} iterations]"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Create a sample file for the agent to work with
    with open("sample.txt", "w") as f:
        f.write("IIT Delhi was established in 1961. It is one of the premier engineering institutions in India.\n")
        f.write("The campus spans 325 acres in Hauz Khas, New Delhi.\n")

    test_queries = [
        "Read sample.txt and summarise what it says.",
        "Read sample.txt and write a one-sentence version of its content to summary.txt.",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        result = run_agent(query)
        print(f"Answer: {result}")