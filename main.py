import os
from dotenv import load_dotenv
from google import genai
from google.genai import types  # type: ignore
import sys
from google.genai import types  # type: ignore
from functions.call_function import call_function, available_functions
from functions.prompts import system_prompt


def main():

    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []

    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content_loop(client, messages, verbose)


def generate_content_loop(client, messages, verbose, max_iterations=20):

    for iteration in range(max_iterations):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            messages.append(response.candidates[0].content)

            if verbose:
                print("Prompt Tokens: ", response.usage_metadata.prompt_token_count)
                print(
                    "Response Tokens: ", response.usage_metadata.candidates_token_count
                )

            for candidate in response.candidates:
                messages.append(candidate.content)

            if not response.function_calls and response.text:
                print("\n Final Response:")
                print(response.text)
                break

            function_call_responses = []

            if response.function_calls:
                for function_call in response.function_calls:

                    print(
                        f"Calling function: {function_call.name}({function_call.args})"
                    )

                    function_call_result = call_function(function_call, verbose)

                    if not function_call_result.parts or not hasattr(
                        function_call_result.parts[0], "function_response"
                    ):
                        raise RuntimeError(
                            f"Fatal exception: call_function for {function_call.name} "
                            "did not return a valid function_response."
                        )
                    if verbose:
                        print(
                            f"-> {function_call_result.parts[0].function_response.response}"
                        )
                    function_call_responses.append(function_call_result.parts[0])

            if function_call_responses:
                messages.append(
                    types.Content(role="user", parts=function_call_responses)
                )
            elif not response.text:
                print(
                    "Error: Model did not provide a text response or a valid function call."
                )
                break

        except Exception as e:
            print(f"Error: {e}")
            break

    else:
        print(
            f"Reached maximum iterations ({max_iterations}). Agent may not have completed the task."
        )


if __name__ == "__main__":

    main()
