import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key=os.environ["OPENROUTER_API_KEY"])

PROMPT = "Explain AI Agent in 2 lines"
start = time.perf_counter()

resp = client.chat.completions.create(
    model="openrouter/free",
    messages=[{"role": "user", "content": PROMPT}]
    )
latency = time.perf_counter()-start

print('Model:', resp.model)
print('Answer :', resp.choices[0].message.content)
print('Latency:', latency)

usage = resp.usage
if usage is not None:
    print("Tokens in  :", usage.prompt_tokens)
    print("Tokens out :", usage.completion_tokens)
    print(resp.usage)   # look for completion_tokens_details → reasoning_tokens
else:
    print("Tokens     : provider did not report usage")