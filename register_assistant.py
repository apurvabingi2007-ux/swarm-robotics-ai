
import openai
import os
from tools import tool_definitions
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

def main():
    try:
        assistant = openai.beta.assistants.create(
            name="Vision-Controlled Robot Assistant",
            instructions="You capture image, detect robot and object, and control movement to complete the user's task.",
            tools=tool_definitions,
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT")
        )
        with open("assistant.id", "w") as f:
            f.write(assistant.id)
        print(f"Assistant created with ID: {assistant.id}")
    except Exception as e:
        print(f"❌ Failed to create assistant: {e}")

if __name__ == "__main__":
    main()


