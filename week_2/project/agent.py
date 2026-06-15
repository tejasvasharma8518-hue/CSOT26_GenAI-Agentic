import os
import requests
import trafilatura
from openai import OpenAI
from dotenv import load_dotenv

import asyncio
import httpx

from mcp import ClientSession
from mcp.client.auth import OAuthClientProvider
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.auth import OAuthClientMetadata
from mcp_test import (
    ALPHAXIV_MCP_URL,
    REDIRECT_URI,
    FileTokenStorage,
    open_browser,
    wait_for_callback,
)

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

SERPER_API_KEY = os.environ["SERPER_API_KEY"]

MODEL = "openai/gpt-oss-120b:free"



async def get_paper_research(query):
    storage = FileTokenStorage()

    auth = OAuthClientProvider(
        server_url=ALPHAXIV_MCP_URL,
        client_metadata=OAuthClientMetadata(
            client_name="Research Agent",
            redirect_uris=[REDIRECT_URI],
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
            scope="read",
        ),
        storage=storage,
        redirect_handler=open_browser,
        callback_handler=wait_for_callback,
    )

    async with httpx.AsyncClient(
        auth=auth,
        follow_redirects=True,
        timeout=60,
    ) as http:

        async with streamable_http_client(
            ALPHAXIV_MCP_URL,
            http_client=http,
        ) as (read, write, _):

            async with ClientSession(read, write) as session:

                await session.initialize()

                discover_result = await session.call_tool(
                    "discover_papers",
                    {
                        "question": query,
                        "keywords": query.split()[:3],
                        "difficulty": 5,
                    }
                )

                return str(discover_result)

               


def web_search(query, num_results=5):
    response = requests.post(
        "https://google.serper.dev/search",
        headers={
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json",
        },
        json={
            "q": query,
            "num": num_results,
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get("organic", []):
        results.append(
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
            }
        )

    return results


def web_fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    text = trafilatura.extract(response.text)

    if not text:
        return "Could not extract content."

    return text[:8000]


def ask_llm(question, context):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research assistant. "
                    "Answer using the provided sources."
                ),
            },
            {
                "role": "user",
                "content": f"""
Question:
{question}

Source Content:
{context}

Provide a concise answer.
""",
            },
        ],
    )

    return response.choices[0].message.content


def main():
    question = input("Research Question: ")

    answer = asyncio.run(
        research_question(question)
    )

    print("=" * 60)
    print(answer)
    print("=" * 60)


async def research_question(question):
    results = web_search(question)

    if not results:
        return "No search results found."

    top_result = results[0]

    content = web_fetch(top_result["link"])

    paper_content = await get_paper_research(question)

    combined_context = f"""
WEB SOURCE:

{content}

PAPER SOURCE:

 {paper_content}
"""

    answer = ask_llm(
        question,
        combined_context
    )

    return answer

if __name__ == "__main__":
    main()