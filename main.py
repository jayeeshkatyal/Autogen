
import os
import json
import re
import sys
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager

# === Get directory from CLI ===
if len(sys.argv) < 2:
    print(" Usage: python main.py <project_directory>")
    sys.exit(1)

PROJECT_DIR = sys.argv[1]

# === LLM Config ===
llm_config = {
    "model": "llama3",
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama"
}

# === Agents ===
analyzer_agent = AssistantAgent(
    name="AnalyzerAgent",
    llm_config=llm_config,
    system_message="""
You are a semantic analyzer. Given code from any programming language, extract:
- Class names and methods/functions
- Method/function parameters
- Method/function calls
- CRUD operations (Create, Read, Update, Delete)
Return plain structured text. Do NOT return JSON.
"""
)

formatter_agent = AssistantAgent(
    name="FormatterAgent",
    llm_config=llm_config,
    system_message="""
You are a JSON formatter. Convert structured code analysis into this strict JSON format:
{
  "file": str,
  "classes": [ { "name": str, "methods": [ { "name": str, "parameters": [str] } ] } ],
  "functions": [ { "name": str, "parameters": [str] } ],
  "method_calls": [str],
  "crud_operations": [str]
}
Return ONLY valid JSON. No markdown, no explanation, no None values.
"""
)

user = UserProxyAgent(name="User", code_execution_config=False)

# === Utilities ===
def collect_files(root_dir):
    code_files = []
    for root, _, filenames in os.walk(root_dir):
        for fname in filenames:
            path = os.path.join(root, fname)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if content.strip():  # skip empty files
                        code_files.append((path, content))
            except Exception as e:
                print(f" Skipping unreadable file: {path}")
    return code_files

def extract_json(content):
    try:

        content = re.sub(r"```(?:json)?\s*", "", content).replace("```", "").strip()
        content = content.replace("None", "null")  # JSON-safe replacement
        return json.loads(content)
    except Exception as e:
        print(" Failed to parse JSON:", e)
        return None

# === Main ===
results = []

for path, code in collect_files(PROJECT_DIR):
    print(f" Analyzing {path}")
    try:
        group_chat = GroupChat(
            agents=[user, analyzer_agent, formatter_agent],
            messages=[],
            max_round=3
        )
        chat_manager = GroupChatManager(groupchat=group_chat, llm_config=llm_config)

        user.initiate_chat(
            chat_manager,
            message=f"""Please analyze the following source code and provide its structure and business logic as JSON.

File: {os.path.basename(path)}

```{code}```
"""
        )

        for msg in reversed(group_chat.messages):
            if msg.get("name") == "FormatterAgent":
                parsed = extract_json(msg.get("content", ""))
                if parsed:
                    parsed["file"] = path

                    # Fix: Ensure all parameters are lists
                    for cls in parsed.get("classes", []):
                        for method in cls.get("methods", []):
                            if not isinstance(method.get("parameters", []), list):
                                method["parameters"] = []

                    for func in parsed.get("functions", []):
                        if not isinstance(func.get("parameters", []), list):
                            func["parameters"] = []

                    results.append(parsed)
                    break
    except Exception as e:
        print(f"  Error analyzing {path}: {e}")
        continue

# === Save Results ===
with open("project_semantic_output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print(" Output saved to 'project_semantic_output.json'")