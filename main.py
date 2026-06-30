import argparse
import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str)
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

messages = [
    types.Content(
        role="user",
        parts=[types.Part(text=args.user_prompt)]
    )
]

function_results = []

for _ in range(20):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
            temperature=0,
        ),
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if response.function_calls:
        function_results = []

        for function_call in response.function_calls:
            result = call_function(function_call, verbose=args.verbose)

            tool_response = result.parts[0].function_response

            if not tool_response or not tool_response.response:
                raise Exception("Empty function response")

            function_results.append(result.parts[0])

        messages.append(
            types.Content(
                role="user",
                parts=function_results
            )
        )
        continue

    print(response.text)
    break

else:
    raise Exception("Agent did not finish in 20 iterations")
