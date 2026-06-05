# SUBMISSION


## Objective

The objective of Week 1 was to understand how LLM APIs work, how API keys are handled securely, and how conversation state can be maintained in a chatbot.

---

## Build 1: Single API Call

In build1.py, I created a simple program that sends a prompt to an LLM through OpenRouter and prints the response.

Example:

Input:

What is the capital of Australia?

Output:

Canberra

### Concepts Learned

- API requests and responses
- Chat completion APIs
- Response objects
- Token usage
- Extracting assistant messages

---

## Build 2: Multi-Turn Chatbot

In build2.py, I implemented a terminal chatbot capable of maintaining conversation history.

### Features

- System prompt support
- Multi-turn conversation
- Conversation memory
- Exit and quit commands
- /reset command
- /tokens command

Example:

You: My name is Tejasva

Bot: Nice to meet you, Tejasva!

You: What is my name?

Bot: Your name is Tejasva.

---

## Understanding LLMs

LLM stands for Large Language Model.

An LLM predicts the most likely next token based on the text provided to it.

Examples include GPT, Gemma, Claude and DeepSeek.

---

## Understanding APIs

API stands for Application Programming Interface.

In this project, the API acts as a bridge between my Python code and the language model hosted on OpenRouter.

Flow:

Python Program
→ OpenRouter API
→ LLM
→ Response
→ Python Program

---

## API Key Safety

The API key is stored inside a .env file.

The key is loaded using python-dotenv.

The .env file is excluded from Git tracking using .gitignore.

This prevents accidental exposure of credentials.

---

## Conversation State

LLMs are stateless.

To maintain memory, conversation history is stored inside a messages list and sent with every API request.

Example:

```python
messages = [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
]
```

This allows the chatbot to remember previous messages.

---

## Key Learnings

- How LLM APIs work
- How chat completions are created
- How to inspect API responses
- How token accounting works
- How environment variables are used
- How conversation memory is manually maintained
- Difference between system, user and assistant roles

---

## Reflection

Before this project, I had never worked with LLM APIs. Building both programs from scratch helped me understand how modern AI applications communicate with language models and maintain context during conversations.

## Challenges Faced

During development, I encountered several issues while setting up the project.

Initially, I used model names that were unavailable or temporarily rate-limited on OpenRouter, which resulted in 404 and 429 errors. Through debugging, I learned how to read API error messages and identify whether the issue was caused by an invalid model name or provider-side rate limiting.

I also learned how to inspect the response object returned by the API before extracting the assistant's message. This helped me understand the structure of chat completions, choices, messages, and usage statistics.

Another challenge was understanding how conversation memory works. At first, I assumed the model would remember previous messages automatically. After implementing the messages list and sending the full history with every request, I understood that LLM APIs are stateless and memory has to be maintained manually by the application.

These debugging steps helped me understand the API workflow much better than simply running a working example.
