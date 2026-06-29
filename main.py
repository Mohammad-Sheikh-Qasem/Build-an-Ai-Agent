from google.genai import types
import argparse
import os
from dotenv import load_dotenv
from google import genai

parser = argparse.ArgumentParser(description="Chatbot")

parser.add_argument('user_prompt', help = "return a text for the prompt", type = str)
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages
)

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if args.verbose:
      print(f"User prompt: {args.user_prompt}")
    #print(f"Prompt tokens: {prompt_tokens}.")

#print(f"Response tokens: {response.text}.")
      print(f"Prompt tokens: {prompt_tokens}")
#print(response.text)

      print(f"Response tokens: {response_tokens}")
print(response.text)
#def main():
#    print("Hello from build-an-ai-agent!")


#if __name__ == "__main__":
#    main()

