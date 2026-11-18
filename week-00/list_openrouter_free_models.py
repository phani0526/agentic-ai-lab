import httpx

resp = httpx.get('https://openrouter.ai/api/v1/models', timeout=10)
resp.raise_for_status()
free = [m for m in resp.json()['data'] if m['id'].endswith('free')]
for m in sorted(free, key=lambda m: -m.get("context_length", 0)):
    print(f'{m["id"]:<55} ctx={m.get("context_length")}')