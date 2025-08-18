import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from config import system_prompt

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    args = sys.argv

    try:
        user_prompt = args[1]

    except IndexError:
        print("No prompt was provided")
        exit(1)


    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(model="gemini-2.0-flash-001",
                                              contents= messages,
                                              config=types.GenerateContentConfig(system_instruction=system_prompt))
    if len(args) == 3:
        print(f"User prompt: {user_prompt}")
        print(response.text)
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
              f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        print(response.text)

if __name__ == "__main__":
    main()


