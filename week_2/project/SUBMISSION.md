# Week 2 Submission

# What I Built

For this week's project, I built a terminal-based research assistant that can search the web, read webpages, and generate answers based on the information it finds. The project combines the concepts covered throughout the week, including tool calling, agent loops, web search, web fetching, and Textual-based terminal interfaces.

I first completed the three builds for the week. Build 1 helped me understand how tool calling works internally by manually parsing tool calls and dispatching them to Python functions. Build 2 used the OpenAI SDK's built-in tool calling support, which made the implementation much cleaner. Build 3 involved converting my Week 1 chatbot into a full-screen Textual application with conversation history, keyboard shortcuts, and background workers to keep the interface responsive during API calls.

For the project itself, I implemented web search using the Serper API and webpage fetching using Requests and Trafilatura. The agent first searches for relevant results, selects a result, fetches the page content, and then sends the gathered information to the language model to generate a final answer. The interface runs inside the terminal and allows users to interact with the agent in a more user-friendly way than a standard command-line script.

# How the Agent Loop Works

The overall flow of my implementation is:

1. Accept a research question from the user.
2. Perform a web search using Serper.
3. Select a search result and fetch the page content.
4. Clean and truncate the webpage text before sending it to the model.
5. Generate a response using the retrieved information.
6. Display the answer to the user.

The project follows the same general agent pattern discussed in the lessons, where tools are used to gather information before producing a final answer.

# Design Decision

One design decision I made was limiting the amount of webpage content sent to the model. Raw webpages can be extremely large and contain a lot of unnecessary information such as navigation menus, advertisements, and page metadata. I used Trafilatura to extract the main content and truncated the result before sending it to the model.

This reduced token usage and made the responses faster while still preserving the most relevant information from the page.

# Features Implemented

- Web search using Serper API
- Web page extraction using Trafilatura
- AlphaXiv MCP integration
- Research workflow combining web search and research papers
- Textual TUI interface
- Multi-turn conversation support
- Non-blocking UI using Textual workers
- Conversation history management

# Something That Surprised Me

The most surprising part of this week's work was MCP authentication. Initially, I assumed that connecting to the AlphaXiv MCP server would only require the server URL. However, I kept receiving 401 Unauthorized errors even though the URL was correct.

After investigating further and discussing the issue with other students, I discovered that AlphaXiv uses OAuth authentication. Once I implemented the OAuth flow and logged in through the browser, the connection worked correctly and I was able to access the AlphaXiv tools and retrieve research papers.

Another issue I encountered was with keyboard shortcuts in the Textual application. Ctrl+L and Ctrl+K worked correctly, but Ctrl+Q conflicted with terminal and editor shortcuts in some environments, which made testing slightly confusing.

# Improvements With More Time

If I had more time, I would extend the agent so that it can repeatedly search, fetch multiple sources, compare information across pages, and automatically decide when it has enough information to answer. I would also integrate the AlphaXiv MCP tools directly into the research workflow so that the agent can combine academic papers and web results in the same response.

Another improvement would be adding streaming responses and a dedicated panel showing which tools are being called in real time. This would make it easier to understand the agent's reasoning process while it is working.

Overall, this project helped me understand how agents actually work behind the scenes rather than treating tool calling as a black box. Building the loop manually and then using the SDK made the differences very clear and gave me a much better understanding of agent-based systems.
