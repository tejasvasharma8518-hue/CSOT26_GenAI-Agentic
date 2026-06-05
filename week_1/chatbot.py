import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

def run_chatbot():
    """
    A terminal chatbot that holds a coherent multi-turn conversation.

    Your implementation should:
    - Start with a system message that sets the assistant's behaviour.
    - Maintain a `messages` list with alternating user/assistant turns.
    - Append the assistant's reply to `messages` after each call.
    - Resend the full history on every API call.
    - Allow the user to type 'exit' or 'quit' to end the session.

    Stretch:
    - Add a '/reset' command that clears history so you can feel context loss live.
    - Add a '/tokens' command that prints response.usage after the last call.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    last_usage = None
    

    print("Chat started. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input == "/tokens":
            print(last_usage)
            continue

        if user_input == "/reset":
            messages = [
                {"role": "system", "content": "You are a helpful assistant."}
            ]
            print("Conversation history cleared.")
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        messages.append(
            {"role": "user", "content": user_input}
        )

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=messages
        )

        last_usage = response.usage

        assistant_reply = response.choices[0].message.content

        messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

        print(f"Bot: {assistant_reply}")        

if __name__ == "__main__":
    run_chatbot()
