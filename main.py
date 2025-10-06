import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types  # type: ignore
from functions.get_files_info import schema_get_files_info, get_files_info
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

system_prompt = (
    system_prompt
) = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
except:
    print("No Input Detected")
    raise Exception("Code 1")

print(response.text)

if response.function_calls:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
else:
    print("No function calls found in response.")

print("Prompt Tokens: ", response.usage_metadata.prompt_token_count)
print("Response Tokens: ", response.usage_metadata.candidates_token_count)
