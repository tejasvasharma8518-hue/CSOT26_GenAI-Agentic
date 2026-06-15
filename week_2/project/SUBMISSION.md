# Week 2 Submission

## What I Built

For Week 2, I built a research assistant that can search the web, retrieve information from webpages, discover relevant research papers, and generate answers based on the information it collects. I also integrated everything into a Textual-based terminal interface so the agent can be used through a full-screen TUI instead of a simple command-line script.

I started by completing all three builds for the week.

### Build 1

In Build 1, I implemented tool calling manually. The model generated tool requests, and I had to parse them and call the correct Python functions myself. This helped me understand what actually happens behind the scenes when a model decides to use a tool.

### Build 2

In Build 2, I used the OpenAI SDK's built-in tool calling functionality. Compared to Build 1, the code became much cleaner because the SDK handled most of the tool execution workflow automatically.

### Build 3

In Build 3, I converted my Week 1 chatbot into a Textual-based terminal UI. The application supports:

* Multi-turn conversations
* Scrollable chat history
* Keyboard shortcuts
* Conversation memory
* Background workers to prevent the UI from freezing while waiting for API responses

This gave me a much better user experience than interacting with the chatbot through a normal terminal.

### Final Project

For the final project, I built a research assistant that combines several different components:

* Web search using the Serper API
* Webpage retrieval using Requests
* Content extraction using Trafilatura
* AlphaXiv MCP integration
* OpenRouter for answer generation
* Textual for the user interface

The goal was to create a system that can gather information before generating an answer instead of relying entirely on the model's internal knowledge.

---

## How the Research Workflow Works

The workflow of my project is:

1. The user enters a research question.
2. The agent performs a web search using Serper.
3. The most relevant search result is selected.
4. The webpage content is downloaded and cleaned using Trafilatura.
5. The AlphaXiv MCP server is queried to discover relevant research papers.
6. The retrieved information is combined into a context.
7. The language model generates a final answer.
8. The answer is displayed to the user in the terminal interface.

This allows the agent to use external information sources before producing a response.

---

## MCP Integration

One of the most interesting parts of the project was integrating the AlphaXiv MCP server.

After connecting successfully, I was able to access tools such as:

* discover_papers
* get_paper_content
* answer_pdf_queries
* read_files_from_github_repository

I mainly used AlphaXiv to retrieve research paper information related to the user's query. This allowed the project to go beyond simple web search and incorporate academic research into the workflow.

Working with MCP was completely new for me, so getting it working felt like one of the biggest achievements of the assignment.

---

## Design Decisions

### Reducing Webpage Noise

Most webpages contain a lot of unnecessary content such as navigation bars, advertisements, footers, and menus.

To avoid sending all of this to the model, I used Trafilatura to extract only the main article content before passing it to the LLM. This reduced token usage and improved response quality.

### Keeping the UI Responsive

Since web searches and API calls can take several seconds, I used Textual workers so that the interface would remain responsive while the agent was working.

Without this, the UI would freeze every time a request was made.

### Separating Logic and Interface

I kept the research workflow separate from the TUI code. The TUI handles user interaction, while the research functions handle searching, fetching, paper discovery, and answer generation.

This made debugging and testing much easier.

---

## Challenges Faced

This project definitely involved more debugging than I expected.

### MCP Authentication

The biggest challenge was getting AlphaXiv MCP authentication working.

At first I kept receiving 401 Unauthorized errors and assumed that I had configured the server URL incorrectly. After spending a lot of time debugging, I discovered that AlphaXiv uses OAuth authentication and requires a browser-based login flow.

Once I implemented the OAuth process and token storage correctly, everything started working.

### Async Issues in the TUI

After connecting the research workflow to the Textual interface, I started running into asynchronous programming issues.

One of the more frustrating errors was related to trying to start an event loop inside another event loop. Since Textual already runs asynchronously, I had to restructure parts of the code so that async functions were called correctly.

This ended up teaching me a lot about how asynchronous Python actually works.

### Git Problems

Towards the end of the assignment, I also ran into Git issues while trying to push my final changes.

My local branch and remote branch had diverged, which caused push failures and merge conflicts. Fixing this required inspecting commit history and carefully updating the repository without losing work.

It was stressful to deal with close to the deadline, but I eventually got everything synced correctly.

### Understanding MCP Tools

Another challenge was figuring out the exact arguments expected by MCP tools.

Several calls failed initially because I was passing incorrect parameters. I ended up creating small test scripts to inspect available tools and experiment with their inputs before integrating them into the project.

---

## Features Implemented

* Serper web search integration
* Requests-based webpage retrieval
* Content extraction using Trafilatura
* AlphaXiv MCP integration
* Research paper discovery
* OpenRouter LLM integration
* Textual TUI interface
* Multi-turn conversation support
* Conversation history management
* Keyboard shortcuts
* Non-blocking UI using workers
* OAuth authentication flow
* Persistent token storage

---

## What Surprised Me

Before starting the project, I assumed that most of the work would involve prompting the language model.

In reality, the model integration was one of the easier parts.

Most of my time was spent getting different systems to work together: authentication, APIs, MCP tools, asynchronous programming, web retrieval, debugging, and Git.

The project made me realize that building AI applications involves much more engineering than simply calling a model API.

Another thing that surprised me was how useful MCP can be once it's configured properly. Being able to access external tools through a common interface felt much more powerful than hardcoding everything directly into the application.

---

## Improvements With More Time

If I had more time, there are several things I would like to improve.

First, I would make the agent more autonomous. Currently the workflow follows a fixed sequence of steps. A future version could allow the model to decide when to search again, which sources to fetch, and when enough information has been collected.

I would also like to fetch multiple webpages and compare information from different sources before generating an answer.

Another improvement would be adding streaming responses so that users can see the answer being generated in real time.

Finally, I would add a dedicated panel showing which tools are being called so that users can better understand what the agent is doing behind the scenes.

---

## Final Reflection

This was probably the most challenging assignment I have worked on in the course so far, but it was also one of the most rewarding.

I started the week thinking that AI agents were mostly about prompting models. After building the project, I now understand that a large part of agent development involves integrating tools, managing data flow, handling authentication, debugging APIs, and designing a good user experience.

The MCP integration was particularly interesting because it was my first time connecting an external tool server to an AI workflow. Seeing the agent retrieve research papers and use them as part of its responses made the project feel much more realistic than a standard chatbot.

Overall, the project gave me a much better understanding of how modern AI systems are built and how different components work together to create useful applications.
