import argparse
import os

from google import genai
from google.genai import types

from dotenv import load_dotenv
from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(
        prog="ai-agent",
        description="An AI Code Assistant"
    )
    parser.add_argument("user_prompt", type=str, help="What prompt to send to Google Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    model = os.environ.get("MODEL")
    if not api_key:
        raise RuntimeError("No GEMINI_API_KEY enviroment variable found.")
    if not model:
        raise RuntimeError("No MODEL enviroment variable found.")

    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, model, args.verbose)


def generate_content(client, messages, ai_model, verbose):
    response = client.models.generate_content(
        model=ai_model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")
    if verbose:
        print(f"Prompt tokens: {
            response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")
    if not response.function_calls:
        print("Response:")
        print(response.text)
        return

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    if not function_responses:
        raise Exception("no function response generated, exiting.")


if __name__ == "__main__":
    main()
