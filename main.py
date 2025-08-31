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
    return response


def get_tool_response(response, verbose):

    tool_response = []

    for fc in response.function_calls:
        function_call_result = call_function(fc, verbose)
        tool_response.append(function_call_result)

        if not function_call_result.parts[0].function_response.response:
            raise Exception("Tool: Fatal error")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    return tool_response


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

    iterations = 0
    while True:
        response = generate_content(client, messages, verbose)


        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
                      f"Response tokens: {response.usage_metadata.candidates_token_count}")

        content = response.candidates[0].content
        messages.append(content)

        if not response.function_calls:
            print(response.text)
            break

        tool_response = get_tool_response(response, verbose)
        for response in tool_response:
            messages.append(response)

        iterations += 1
        if iterations > 5:
            print("You've exceeded max iterations")
            break


if __name__ == "__main__":
    main()


