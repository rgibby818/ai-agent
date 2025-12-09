from os import environ
from sys import argv
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file


def main():
    load_dotenv()
    api_key = environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    env_model = environ.get("MODEL")

    if len(argv) < 2:
        print("Error: No prompt passed")
        print("Usage: python3 main.py <prompt>")
        exit(1)

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file],
    )
    user_prompt = argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    response = client.models.generate_content(
        model=env_model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt)
    )
    function_calls = response.function_calls
    if "--verbose" in argv:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {
            response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {
              response.usage_metadata.candidates_token_count}")

    print("----------------------Function Call------------------------------")
    print(f"Calling function: {function_calls[0].name}({function_calls[0].args})")
    print("-----------------------------------------------------------------")


if __name__ == "__main__":
    main()
