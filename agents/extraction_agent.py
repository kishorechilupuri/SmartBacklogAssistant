"""Step 2: Extract requirements from raw text or a file."""
import json
import logging
import llm_client
from prompts.prompts import EXTRACTION_SYSTEM
from tools.file_tools import run_tool_loop

log = logging.getLogger("backlog_assistant")


def clean_json(raw: str) -> str:
    """Strip markdown fences if present."""
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return raw


def extract_requirements(input_text: str, is_filepath: bool = False) -> dict:
    """If is_filepath=True, the model uses the read_file tool automatically."""
    log.info("Step 1: Extracting requirements...")

    if is_filepath:
        messages = [{"role": "user", "content": f"Please read the file at '{input_text}' and extract all requirements."}]
        raw = run_tool_loop(messages, system=EXTRACTION_SYSTEM)
    else:
        messages = [{"role": "user", "content": f"Extract requirements from:\n\n{input_text}"}]
        raw = llm_client.chat(messages, system=EXTRACTION_SYSTEM, json_mode=True)["content"]

    data = json.loads(clean_json(raw))
    log.info(f"Extracted {len(data['requirements'])} requirements")
    return data
