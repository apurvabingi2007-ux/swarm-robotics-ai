
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2024-02-15-preview"

# Create a new thread
thread = openai.beta.threads.create()

# Save the thread ID to file
with open("thread.id", "w") as f:
    f.write(thread.id)

print(f"Thread ID created and saved: {thread.id}")

