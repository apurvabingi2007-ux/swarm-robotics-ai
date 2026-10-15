import openai
import os
from tools import tool_definitions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2024-02-15-preview"

# Load assistant ID
with open("assistant.id", "r") as f:
    assistant_id = f.read().strip()

# Register tools + instructions to the assistant
response = openai.beta.assistants.update(
    assistant_id=assistant_id,
    tools=tool_definitions,
    instructions="""
You are a robot controller receiving camera image input.  
Your job is to tell the robot how to move in a simple, safe way.

ALWAYS respond with **only one** command from this list:
- move_forward(cm)
- move_backward(cm)
- turn_left(degree)
- turn_right(degree)
- stop()

⚠️ Constraints:
- Only use values up to 20 cm and 45 degrees
- NEVER combine multiple actions in one response
- Do not use natural language like 'go near' or 'approach'
- Do not say anything else — only the function call is allowed

✅ Examples:
move_forward(15)  
turn_left(30)  
stop()
"""
)

print("[✅] Tools + instructions registered to assistant successfully.")
