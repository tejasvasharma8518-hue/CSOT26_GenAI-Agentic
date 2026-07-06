# Week 4 Submission – Research Desk Agent

## Overview

For Week 4, I extended my Week 3 Research Desk agent into a more capable research and coding assistant. The agent can maintain todos, explore repositories, inspect code structure, execute commands safely, save notes, resume sessions, and verify work before marking tasks complete.

The project combines research tools, repository exploration tools, planning tools, session memory, and safety mechanisms into a single agent workflow.

---

# Build 1 – Command Execution

Implemented:

- paths_within_sandbox
- classify_command
- run_command

Features:

- Read-only commands execute immediately.
- Destructive commands require human approval.
- Commands are restricted to the workspace sandbox.
- Output is captured and returned safely.
- Timeouts are enforced.
- Exit codes are returned for verification.

Examples:

- git status
- git log
- pytest
- grep
- ls

Safety:

- Commands that may modify files require explicit approval.
- Commands attempting to escape the workspace are blocked.

---

# Build 2 – Repository Exploration

Implemented:

- resolve_path
- grep
- list_definitions

Features:

- Search repository contents for patterns.
- Skip excluded directories.
- AST-based inspection of Python files.
- Function, method, and class discovery with line numbers.
- Structural understanding of repositories without reading entire files.

Repository used for testing:

- Flask (https://github.com/pallets/flask)

Examples:

- Searched for Flask route definitions.
- Located Flask application methods.
- Inspected flask/app.py structure using AST.
- Explored repository contents using grep before reading files.

---

# Build 3 – Todo System

Implemented:

- add_todos
- get_todos
- mark_todo
- verify_todo

Features:

- Persistent storage using `.agent/todos.json`
- Verification evidence required before completion
- Todo state survives restarts
- Status tracking

Supported statuses:

- pending
- in_progress
- blocked
- failed
- completed

Verification:

A todo cannot be completed without verification evidence.

Example workflow:

1. Create todo.
2. Execute verification command.
3. Collect evidence.
4. Mark todo completed.

---

# Project Features

The final agent integrates:

- Web search
- Academic paper search
- Session persistence
- Resume previous sessions
- Note generation
- Repository search
- Command execution
- Todo tracking
- Verification workflow
- Repository exploration

The agent automatically:

1. Creates todos.
2. Searches repositories.
3. Executes verification commands.
4. Stores notes.
5. Saves conversation history.
6. Marks tasks completed with evidence.

---

# Safety Features

Implemented:

### Approval-Gated Commands

Potentially destructive commands require explicit human approval before execution.

Examples:

- rm
- mv
- git push
- git commit
- pip install

### Approval-Gated File Operations

File modifications require explicit approval.

Examples:

- write_file
- edit_file

### Sandbox Protection

Commands attempting to access files outside the workspace are rejected.

---

# Memory Features

Implemented:

### Session Persistence

Conversations are automatically saved to:

```
.agent/sessions
```

### Session Resume

Users can resume previous sessions using:

```
/resume <session_name>
```

### Notes

Generated research notes are automatically stored in:

```
notes/
```

---

# Repository Used

Flask

https://github.com/pallets/flask

The Flask repository was used to test:

- grep
- list_definitions
- repository exploration
- command execution
- repository mapping

---

# Bonus Features

## 1. Prompt Injection Protection

Implemented a basic repository-content sanitization layer.

The agent checks repository text for potentially malicious instructions such as:

- ignore previous instructions
- reveal system prompt
- delete all files
- ignore system message

Suspicious content is removed before being passed to the model.

This helps separate repository content from agent instructions.

---

## 2. Extended Todo States

Added support for additional states:

- blocked
- failed

in addition to:

- pending
- in_progress
- completed

This more closely matches real-world task management systems used by autonomous agents.

---

## 3. Repository Map

Implemented a repository mapping utility.

The repository map:

- Scans Python files.
- Uses AST analysis.
- Extracts classes, methods, and functions.
- Produces a high-level structural overview of a repository.

This was inspired by the repository mapping ideas discussed in the Week 4 material.

---

## 4. Automatic Verification

Implemented executable verification commands.

Instead of simply storing verification information, the agent can execute verification commands and use the result to determine whether a task should be marked completed.

Example:

- git status
- pytest

Verification results are converted into completion evidence.

---

# Lessons Learned

The most important lesson from Week 4 was understanding the difference between a chatbot and an agent.

A chatbot mainly answers questions, while an agent can:

- plan work
- maintain memory
- use tools
- inspect repositories
- verify results
- interact safely with external systems

I also learned how repository exploration, todo tracking, verification, and approval mechanisms work together to make AI systems more reliable and trustworthy.

The repository exploration tools and verification workflow were particularly useful because they encouraged evidence-based task completion instead of simply trusting generated responses.