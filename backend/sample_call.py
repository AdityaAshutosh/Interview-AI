import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY= os.getenv("API_KEY")
claude= anthropic.Anthropic(api_key=API_KEY)

print(claude.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "I am Optimus Prime"}
    ]
))

