"""Tools (Step 1): file reading, tool definitions, registry, and the tool loop."""
import logging
import llm_client

log = logging.getLogger("backlog_assistant")


def read_file(filepath: str) -> str:
    """Read text content from a file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: File not found: {filepath}"
    except Exception as e:
        return f"ERROR: {e}"


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return the full contents of a text or markdown file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {"type": "string", "description": "Relative or absolute path to the file"}
                },
                "required": ["filepath"],
            },
        },
    }
]

TOOL_REGISTRY = {
    "read_file": lambda filepath: read_file(filepath),
}


def execute_tools(tool_calls: list) -> list:
    """Execute all tool calls and return tool result messages."""
    results = []
    for call in tool_calls:
        name = call["function"]["name"]
        args = call["function"]["arguments"]
        log.info(f"Tool call: {name}({args})")
        fn = TOOL_REGISTRY.get(name)
        result = fn(**args) if fn else f"Unknown tool: {name}"
        log.info(f"Tool result: {result[:100]}{'...' if len(result) > 100 else ''}")
        results.append({"role": "tool", "content": result})
    return results


def run_tool_loop(messages: list, system: str = "") -> str:
    """Run until the model stops calling tools. Returns the final text response."""
    while True:
        msg = llm_client.chat(messages, system=system, tools=TOOL_DEFINITIONS)
        messages.append(msg)
        if msg.get("tool_calls"):
            messages.extend(execute_tools(msg["tool_calls"]))
        else:
            return msg.get("content", "")
