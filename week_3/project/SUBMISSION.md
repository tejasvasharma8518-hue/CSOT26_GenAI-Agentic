# Week 3 Submission

## Overview

For Week 3, I converted my Week 2 research assistant into a research agent with memory, persistent sessions, paper search capabilities, file tools, and a Textual UI.

The main objective this week was to make the agent capable of remembering previous conversations and continuing research across multiple sessions instead of starting from scratch every time.

## What I Implemented

### 1. Persistent Sessions

I implemented session storage using JSON files inside `.agent/sessions`.

Whenever the user interacts with the agent, the conversation history is saved automatically. On startup, the latest session is loaded so the agent can continue previous discussions.

I also added:

* `/sessions` command to list saved sessions
* `/resume <session_name>` command to load a previous session

This allows conversations to be resumed even after closing the terminal.

---

### 2. AGENTS.md Support

The agent reads instructions from `AGENTS.md` during startup and adds them to the system prompt.

This separates agent behaviour from the code and makes it easier to modify instructions without editing Python files.

---

### 3. Paper Search Tools

I implemented paper tools using the Hugging Face Papers API.

Functions added:

* `paper_search(query)`
* `read_paper(arxiv_id)`

The agent now searches both the web and academic papers before generating a response.

For academic questions, paper information is included alongside web results to produce better answers.

---

### 4. File Tools

I implemented:

* `list_files()`
* `read_file()`
* `write_file()`
* `edit_file()`

The read tool supports line-based reading and indicates whether more content exists.

The edit tool supports:

* append
* replace
* delete

and returns a simple diff preview after modifications.

---

### 5. Research Notes

Whenever the agent generates a response, it automatically saves the answer inside the `notes/` directory.

This creates a small research archive that can be revisited later without rerunning searches.

---

### 6. Agent Class Architecture

I separated the project into an Agent-based structure.

The base `Agent` class handles:

* session management
* paper tools
* web tools
* memory
* note generation

The REPL and TUI act as interfaces on top of the same core agent logic.

This made the code cleaner and easier to maintain.

---

### 7. Multiple Ways to Run

The project supports:

#### REPL Mode

```bash
python agent.py
```

#### One-Shot Mode

```bash
python agent.py "What is Q-learning?"
```

#### Textual UI

```bash
python agent.py --tui
```

All three use the same agent backend.

---

## Challenges Faced

Most of the time spent this week was debugging.

Some issues I encountered:

* Accidentally created the Week 3 folder inside Week 2 and had to reorganize the project structure.
* Faced multiple Python import path issues while moving files.
* Had a duplicate `edit_file()` definition which silently overrode the intended implementation.
* Encountered OpenRouter model availability issues and had to switch models.
* Session filenames initially contained special characters which caused problems while resuming sessions.

Debugging these issues took more time than implementing the actual features.

---

## What I Learned

This week helped me understand that an AI agent is much more than just an LLM call.

The important parts are:

* memory
* tool usage
* file management
* persistence
* retrieval of external information

Building these components gave me a much better understanding of how agent systems work in practice.

I also got more comfortable working with APIs, JSON storage, file operations, and organizing a larger Python project.

---

## Bonus Features

I implemented:

* `/sessions` command
* `/resume <session_name>` command

for managing and resuming previous conversations.

---

## Final Thoughts

Compared to my Week 2 project, this version feels much closer to a real research assistant.

The agent can search the web, search papers, save notes, remember previous conversations, and continue research across sessions. The addition of memory and persistence made the biggest difference in usability.

Overall, this week gave me practical experience with how modern AI agents are structured and how different components work together beyond the language model itself.
