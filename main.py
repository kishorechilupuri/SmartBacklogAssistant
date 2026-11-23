"""
Smart Backlog Assistant — run with:
  python main.py                                 # interactive mode
  python main.py --file input/sample_meeting_notes.md
  python main.py --demo                          # uses input/sample_meeting_notes.md

Prerequisites: Ollama running at http://localhost:11434 with `ollama pull llama3.1:8b`
"""
import sys
import time
import logging
import argparse
from datetime import datetime

from agents.extraction_agent import extract_requirements
from agents.story_agent import generate_all_stories
from agents.prioritization_agent import prioritize_stories

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("backlog_assistant")

DEMO_FILE = "input/sample_meeting_notes.md"


def format_backlog(stories: list, summary: str) -> str:
    """Format the final backlog as readable Markdown."""
    lines = [
        "# Smart Backlog Assistant — Output",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "", "## Summary", summary, "", "## Backlog", "",
    ]
    sprint_labels = {
        "sprint_1": "Sprint 1 — Critical / Now",
        "sprint_2": "Sprint 2 — High Value",
        "backlog": "Backlog — Defer / Low Priority",
    }
    for key, label in sprint_labels.items():
        group = [s for s in stories if s.get("sprint_suggestion", "backlog") == key]
        if not group:
            continue
        lines += [f"### {label}", ""]
        for s in group:
            lines.append(f"#### [{s.get('story_points', '?')}pt] [{str(s.get('priority', '?')).upper()}] "
                         f"[{s.get('category', 'other')}] {s.get('story', 'N/A')}")
            lines += ["", "**Acceptance Criteria:**"]
            lines += [f"- {ac}" for ac in s.get("acceptance_criteria", [])]
            lines.append("")
    return "\n".join(lines)


def run_pipeline(input_text: str = "", filepath: str = "") -> str:
    """input -> extract -> stories -> prioritize -> format"""
    t0 = time.time()
    log.info("Starting Smart Backlog Assistant pipeline...")

    if filepath:
        extraction = extract_requirements(filepath, is_filepath=True)
    else:
        extraction = extract_requirements(input_text)

    stories = generate_all_stories(extraction["requirements"])
    prioritized = prioritize_stories(stories)
    output = format_backlog(prioritized, extraction["summary"])

    log.info(f"Pipeline complete in {time.time() - t0:.1f}s — {len(stories)} stories generated")
    return output


def main():
    parser = argparse.ArgumentParser(description="Smart Backlog Assistant")
    parser.add_argument("--file", help="Path to meeting notes file (.txt or .md)")
    parser.add_argument("--demo", action="store_true", help="Run with input/sample_meeting_notes.md")
    args = parser.parse_args()

    if args.demo:
        print(f"Running demo with {DEMO_FILE}...\n")
        result = run_pipeline(filepath=DEMO_FILE)
    elif args.file:
        print(f"Processing file: {args.file}\n")
        result = run_pipeline(filepath=args.file)
    else:
        print("Smart Backlog Assistant")
        print("Paste your meeting notes below. Press Enter twice when done.\n")
        lines, empty_count = [], 0
        while empty_count < 2:
            line = input()
            empty_count = empty_count + 1 if line == "" else 0
            lines.append(line)
        text = "\n".join(lines).strip()
        if not text:
            print("No input provided. Use --demo to run with sample data.")
            sys.exit(1)
        result = run_pipeline(input_text=text)

    print("\n" + "=" * 60)
    print(result)
    print("=" * 60)

    output_file = f"output/backlog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(result)
    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
