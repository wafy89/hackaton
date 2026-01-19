#import wikipedia as wp
from openai import OpenAI
from dotenv import load_dotenv
import os
print("first")

load_dotenv()
print("2")

OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
print("3")

if not OPEN_AI_KEY:
    raise RuntimeError("OpenAI API key is required.")

print("4")

ai = OpenAI(
    api_key=OPEN_AI_KEY,
)
print("5")

response = ai.responses.create(
    model="gpt-5-nano",
    input="what is today's date",
)

print("start")
print(response.output_text)
print("DONE")

