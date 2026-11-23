# Smart Backlog Assistant

Turns raw meeting notes into a prioritized, sprint-ready backlog of user stories. Runs **fully
locally** on **Llama 3.1 8B** via **Ollama** (`http://localhost:11434`) — no cloud, no API key.

## 1. Objective & Problem Statement

**Problem.** After planning meetings, teams spend hours hand-converting unstructured notes into
well-formed backlog items; stories end up inconsistent, requirements get lost, and sending internal
notes to a cloud LLM is often not permitted.

**Objective.** Automate notes → requirements → user stories → prioritized sprint plan using a local LLM.

## 2. Key Features

- Reads notes from a file (the LLM calls a `read_file` tool itself), pasted text, or a demo file
- Extracts requirements / bugs / non-functional constraints
- Generates user stories with acceptance criteria, Fibonacci points, priority and category (few-shot prompt)
- Prioritizes and assigns Sprint 1 / Sprint 2 / Backlog
- Saves a Markdown backlog to `output/`

## 3. LLMs, Tools, Frameworks

| Item | Used |
|---|---|
| Model | Llama 3.1 8B (`llama3.1:8b`) |
| Runtime | Ollama REST API (`/api/chat`) via Python `requests` |
| Techniques | System prompts, few-shot prompting, JSON output mode, tool calling |
| Tool | `read_file` |

## 4. Agentic Architecture

```
 notes (file / text)
        │
        ▼
 ┌──────────────────┐   tool call    ┌───────────┐
 │ Extraction Agent │ ─────────────► │ read_file │
 └────────┬─────────┘ ◄───────────── └───────────┘
          │ requirements (JSON)
          ▼
 ┌──────────────────┐
 │   Story Agent    │  (few-shot, one story per requirement)
 └────────┬─────────┘
          │ stories (JSON)
          ▼
 ┌──────────────────┐
 │ Prioritization   │  (sort + sprint tag, plain Python)
 └────────┬─────────┘
          ▼
   Markdown formatter ──► output/backlog_*.md

 Extraction + Story agents ◄──► llm_client.py ◄──► Ollama (llama3.1:8b @ localhost:11434)
```

## 5. End-to-End Data Flow

1. `main.py` receives a file path, pasted text, or `--demo`.
2. **Extraction**: Llama calls `read_file`, then returns `{requirements, summary}` as JSON.
3. **Stories**: for each requirement, Llama returns `{story, acceptance_criteria, story_points, priority, category}`.
4. **Prioritization**: sorted by priority (high > medium > low), then fewer points first; sprint tag added.
5. **Output**: formatted Markdown is printed and saved in `output/`.

## 6. Project Structure

```
SmartBacklogAsistant/
├── main.py                       # entry point: CLI + pipeline + formatter
├── llm_client.py                 # Ollama client (host + model)
├── agents/
│   ├── extraction_agent.py       # notes -> requirements
│   ├── story_agent.py            # requirement -> user story
│   └── prioritization_agent.py   # ordering + sprint suggestion
├── tools/file_tools.py           # read_file, tool schema, registry, tool loop
├── prompts/prompts.py            # system prompts + few-shot example
├── input/sample_meeting_notes.md
├── output/                       # generated backlogs
├── requirements.txt
└── smart_backlog_assistant.py    # original single-file Claude version (reference only)
```

## 7. Setup & Execution

```powershell
ollama pull llama3.1:8b        # one-time; Ollama must be running
pip install -r requirements.txt

python main.py --demo          # run on input/sample_meeting_notes.md
python main.py --file input/sample_meeting_notes.md
python main.py                 # paste notes, press Enter twice
```

To change the model or host, edit `HOST` / `MODEL` in `llm_client.py`.

**Notes.** A full run makes ~7 sequential LLM calls; on CPU it can take a few minutes.
Prioritization is plain Python because an 8B model is unreliable at re-ordering long JSON.
