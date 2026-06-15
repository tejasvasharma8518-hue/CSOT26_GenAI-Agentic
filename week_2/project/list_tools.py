import asyncio
import httpx

from mcp import ClientSession
from mcp.client.auth import OAuthClientProvider
from mcp.client.streamable_http import streamable_http_client
from mcp.shared.auth import OAuthClientMetadata

from mcp_test import (
    ALPHAXIV_MCP_URL,
    FileTokenStorage,
    open_browser,
    wait_for_callback,
    REDIRECT_URI,
)

async def main():
    storage = FileTokenStorage()

    auth = OAuthClientProvider(
        server_url=ALPHAXIV_MCP_URL,
        client_metadata=OAuthClientMetadata(
            client_name="Tool Lister",
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
        timeout=60
    ) as http:

        async with streamable_http_client(
            ALPHAXIV_MCP_URL,
            http_client=http
        ) as (read, write, _):

            async with ClientSession(read, write) as session:

                await session.initialize()

                tools = await session.list_tools()

                print("\nAVAILABLE TOOLS:\n")

                for tool in tools.tools:
                    print(tool.name)

asyncio.run(main())