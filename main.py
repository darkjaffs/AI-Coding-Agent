import os
from dotenv import load_dotenv  # type: ignore
from google import genai
import sys
from google.genai import types  # type: ignore

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=sys.argv[1]
    )
except:
    print("No Input Detected")
    raise Exception("Code 1")

print(response.text)

print("Prompt Tokens: ", response.usage_metadata.prompt_token_count)
print("Response Tokens: ", response.usage_metadata.candidates_token_count)
