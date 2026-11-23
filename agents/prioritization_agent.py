"""Step 4: Prioritize stories and suggest a sprint.

Done in plain Python: an 8B model is unreliable at re-ordering a long JSON array,
and this is simple arithmetic. Rule: high=3, medium=2, low=1; ties -> fewer points first.
"""
import logging

log = logging.getLogger("backlog_assistant")

SCORE = {"high": 3, "medium": 2, "low": 1}


def prioritize_stories(stories: list) -> list:
    log.info("Step 3: Prioritizing stories...")
    ordered = sorted(
        stories,
        key=lambda s: (-SCORE.get(str(s.get("priority")).lower(), 1), int(s.get("story_points", 99))),
    )
    for s in ordered:
        prio, pts = str(s.get("priority")).lower(), int(s.get("story_points", 99))
        if prio == "high":
            s["sprint_suggestion"] = "sprint_1"
        elif prio == "medium" and pts <= 5:
            s["sprint_suggestion"] = "sprint_2"
        else:
            s["sprint_suggestion"] = "backlog"
    return ordered
