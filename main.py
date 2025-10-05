import os 
from dotenv import load_dotenv
from google import genai
import sys

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001",
        contents = sys.argv[1]
    )
except:
    print("No Input Detected")
    raise Exception("Code 1")

print(response.text)

print("Prompt Tokens: ", response.usage_metadata.prompt_token_count)
print("Response Tokens: ", response.usage_metadata.candidates_token_count)