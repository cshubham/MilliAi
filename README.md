# 🌸 MilliAI

A minimal "Cursor-style" coding agent built from scratch in Python — an LLM that can actually **use tools** (like reading your files) to answer questions, wrapped in a cherry-blossom themed chat UI.

Built as a learning project to understand how AI coding agents really work under the hood: it's just an **LLM + tools + a loop**.

<img width="1171" height="748" alt="MilliAI screenshot" src="https://github.com/user-attachments/assets/ff7ee5bf-e5fd-43e5-90fe-b27eec41cf3c" />

## What it does

- Chat with an LLM through a clean, pink cherry-blossom UI.
- The agent can **call tools** — currently `read_file`, so it can open and reason about files on disk.
- Remembers the conversation across turns (multi-turn memory).
- Runs locally as a real coding agent, or hosted as a shareable demo.

## How it works

The whole "agent" is a simple loop:

1. Send the LLM the conversation **+ a list of tools it can use**.
2. The LLM replies with either a normal answer **or** a request to run a tool (e.g. `read_file("agent.py")`).
3. If it's a tool request, the code runs the tool locally and feeds the result back.
4. Loop until the LLM produces a final answer.

| File | Role |
|------|------|
| `agent.py` | The **engine** — tool definitions + the agent loop (`run_agent_turn`) |
| `app.py` | The **UI** — a Streamlit chat interface that calls the engine |
| `agentGrok.py` | The first "hello LLM" test script |
| `requirements.txt` | Dependencies (`streamlit`, `groq`) |
| `.streamlit/config.toml` | Pink theme config |

**Model:** `openai/gpt-oss-20b` served free/fast via [Groq](https://groq.com).

## Setup (run locally)

**1. Clone and enter the project**

```bash
git clone https://github.com/cshubham/MilliAi.git
cd MilliAi
```

**2. Create a virtual environment and install dependencies**

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
pip install -r requirements.txt
```

**3. Get a free Groq API key**

Create one at [console.groq.com/keys](https://console.groq.com/keys), then set it as an environment variable:

```bash
export GROQ_API_KEY="your_key_here"
```

**4. Run it**

Chat UI (recommended):

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

Or the command-line version:

```bash
python agent.py
```

## Deploy (Streamlit Community Cloud)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **Create app** → select this repo → main file `app.py`.
3. In **Settings → Secrets**, add your key:

   ```toml
   GROQ_API_KEY = "your_key_here"
   ```

4. Deploy — you get a public `https://<name>.streamlit.app` link.

> **Note:** When hosted, the agent's tools run on the *server*, so `read_file` reads the server's files, not yours — great as a demo, but the true "codes on my machine" experience is running it locally.

## Roadmap

- [ ] More tools: `list_files`, `write_file`, `run_command`
- [ ] Safety confirmation before writing/running
- [ ] Streaming responses
- [ ] System prompt tuning
