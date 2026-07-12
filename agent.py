import os, json
from groq import Groq

client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --- 1. The executor (real Python function) ---
def read_file(path: str) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {e}"

# --- 2. The schema (what the LLM sees) ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return the full text contents of a file on the local disk.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file, e.g. 'agent.py'"}
                },
                "required": ["path"],
            },
        },
    }
]

# --- 3. Map each tool NAME to its real Python executor ---
# When the model says "run read_file", we look it up here.
TOOL_FUNCTIONS = {
    "read_file": read_file,
}

MODEL = "openai/gpt-oss-20b"

# --- 4. The reusable agent loop ---
# Takes the ongoing conversation (a list of messages), lets the model think
# and call tools until it produces a final text answer. The `messages` list is
# mutated in place so the caller keeps the full history (the agent's "memory").
# Returns: (final_text, tool_events) where tool_events is a list of (name, args)
# describing every tool the agent ran this turn — handy for showing in a UI.
def run_agent_turn(messages: list) -> tuple[str, list]:
    tool_events = []

    while True:
        # (a) Ask the model what to do next, given the conversation so far.
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
        )
        msg = response.choices[0].message

        # (b) Record the model's reply (text and/or tool requests) in history.
        messages.append(msg)

        # (c) No tool calls => the model gave its final answer. We're done.
        if not msg.tool_calls:
            return msg.content, tool_events

        # (d) Otherwise, run every tool the model asked for...
        for call in msg.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments)  # arguments arrive as a JSON string
            tool_events.append((name, args))

            func = TOOL_FUNCTIONS.get(name)
            result = func(**args) if func else f"ERROR: unknown tool '{name}'"

            # (e) ...and feed each result back, tagged with the call id.
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result),
            })
        # (f) Loop again so the model can read the results and continue.


# CLI helper: one-shot question, prints tool activity + final answer.
def run_agent(user_message: str):
    messages = [{"role": "user", "content": user_message}]
    answer, tool_events = run_agent_turn(messages)
    for name, args in tool_events:
        print(f"[tool] {name}({args})")
    print("\nAGENT:", answer)
    return answer


if __name__ == "__main__":
    run_agent("What's the first line of agent.py?")