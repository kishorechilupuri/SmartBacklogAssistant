"""Step 3: Generate user stories (few-shot + structured output)."""
import json
import logging
import llm_client
from prompts.prompts import STORY_SYSTEM, STORY_EXAMPLES
from agents.extraction_agent import clean_json

log = logging.getLogger("backlog_assistant")


def generate_user_story(requirement: dict) -> dict:
    messages = STORY_EXAMPLES + [
        {"role": "user", "content": f"Requirement ({requirement['type']}): {requirement['text']}"}
    ]
    raw = llm_client.chat(messages, system=STORY_SYSTEM, json_mode=True)["content"]
    story = json.loads(clean_json(raw))
    story["requirement_id"] = requirement["id"]
    return story


def generate_all_stories(requirements: list) -> list:
    log.info(f"Step 2: Generating {len(requirements)} user stories...")
    stories = []
    for i, req in enumerate(requirements, 1):
        log.info(f"  Generating story {i}/{len(requirements)} for {req['id']}...")
        stories.append(generate_user_story(req))
    return stories
