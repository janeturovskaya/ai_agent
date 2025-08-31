import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from config import system_prompt
from call_functions import call_function, available_functions


def generate_content(client, messages, verbose):

    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents=messages,
                                              config=types.GenerateContentConfig(
                                                  tools=[available_functions],
                                                  system_instruction=system_prompt
                                              ))
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
              f"Response tokens: {response.usage_metadata.candidates_token_count}")

    for candidate in response.candidates:
        messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    for fc in response.function_calls:
        function_call_result = call_function(fc, verbose)

        messages.append(function_call_result.types.Content(role='user'))

        if not function_call_result.parts[0].function_response.response:
            raise Exception("Fatal error")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")


def main():

    load_dotenv()
    args = sys.argv
    verbose = "--verbose" in args

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = args[1]

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    while True:
        response = client.models.generate_content(model="gemini-2.0-flash-001",
                                                  contents=messages,
                                                  config=types.GenerateContentConfig(
                                                      tools=[available_functions],
                                                      system_instruction=system_prompt
                                                  ))

        messages.append({"role": "assistant", "text": response.text})
        messages.append({"role": "tool", "text": get_updated_description(response)})




if __name__ == "__main__":
    main()


