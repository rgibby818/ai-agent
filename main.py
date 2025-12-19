import argparse
import os

from google import genai
from google.genai import types
from google.genai.errors import ClientError

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
        types.Content(role="user",
                      parts=[types.Part(text=args.user_prompt)])
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    max_iterations = 20
    for i in range(0, max_iterations):
        if generate_content(client, messages, model, args.verbose) is None:
            break


def generate_content(client: genai.Client, messages: list, ai_model: str, verbose: bool) -> None | bool:
    """
    Generate a model response using the Gemini API, handle tool/function calls,
    and update the converation state in-place.

    This function sends the provided messages to the specified AI model,
    prints usage metadata when verbosity is enabled, and process the model's reponse in one of three ways:
        1. Prints a final text reponse and ends the agent loop.
        2. Appends candidate model outputs to the message history.
        3. Executes any requested function calls, appends their results to the mesage history, and 
           signals that the agent should continue.

    Parameters
    --------
    client: genai.Client
        An initialized Gemini API client used to generate content.
    messages: list
        The converation history passed to the model; this list is modified in-place with new model outputs and function calls results.
    ai_model: str
        The name or identifiier of the AI model to use. Example("gemini-2.5-flash")
    verbose: bool
        If true, prints token usage information and function call outputs.

    Returns
    --------
    None or bool
        Return None when final text reponse is produced and the agent should stop. Returns True when additional steps
        are required and the agent should continue.

    Side Effects
    --------
    - Prints output to stdout
    - Mutates the 'messages' list by appending model responses and function call results.
    """
    try:
        response = client.models.generate_content(
            model=ai_model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
            ),
        )
    except ClientError as e:
        if e.code == 429 or 'RESOURCE_EXHAUSTED' in str(e):
            print("Quota exceeded / rate limit hit:")
            print(e)
            return None
        else:
            print("Response Error:")
            print(e)
            return None

    if not response.usage_metadata or response is None:
        raise RuntimeError("Gemini API response appears to be malformed")
    if verbose:
        print(f"Prompt tokens: {
            response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")

    if not response.function_calls and response.text:
        print("Final Response:")
        print(response.text)
        return None  # End agent call.

    if response.candidates:
        for candidate in response.candidates:
            if candidate is None or candidate.content is None:
                continue
            messages.append(candidate.content)

    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)

            if (
                not function_call_result.parts or not function_call_result.parts[0].function_response
            ):
                raise Exception("empty function call result")

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(function_call_result)
    return True  # Continue agent call.


if __name__ == "__main__":
    main()
