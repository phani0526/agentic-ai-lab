import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
or_client = OpenAI(
    base_url=os.environ.get("OPENROUTER_BASE_URL"), api_key=os.environ["OPENROUTER_API_KEY"]
)
ol_client = OpenAI(base_url=os.environ.get("OLLAMA_BASE_URL"), api_key="ollama")

PROMPT = "Explain AI Agent in 2 lines"

start = time.perf_counter()
or_resp = or_client.chat.completions.create(
    model="nvidia/nemotron-3.5-lightning:free", messages=[{"role": "user", "content": PROMPT}]
)
latency = time.perf_counter() - start

print("Model:", or_resp.model)
print("Answer :", or_resp.choices[0].message.content)
print("Latency:", latency)
print(or_resp.usage)

#start = time.perf_counter()
#ol_resp = ol_client.chat.completions.create(
    #model="qwen3:0.6b", messages=[{"role": "user", "content": PROMPT}]
#)

#latency = time.perf_counter() - start

#print("Model:", ol_resp.model)
#print("Answer :", ol_resp.choices[0].message.content)
#print("Latency:", latency)
#print(ol_resp.usage)

for label, prompt in [("think", PROMPT), ("no_think", PROMPT + " /no_think")]:
    start = time.perf_counter()
    resp = ol_client.chat.completions.create(
        model="qwen3:0.6b",
        messages=[{"role": "user", "content": prompt}],
    )
    latency = time.perf_counter() - start
    print(f"{label:<9} {latency:>6.2f}s  tokens={resp.usage.completion_tokens if resp.usage else 'n/a'}")
    print("   ", resp.choices[0].message.content)