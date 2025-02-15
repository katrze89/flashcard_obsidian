import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env", ".env-chatgpt"))

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a haiku about recursion in programming."},
    ],
)

print(completion.choices[0].message)
