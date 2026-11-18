# print the Python version, confirm uv, ruff, pyright and pytest are installed, ping Ollama, make one hosted-model call using a key from .env
import asyncio
import importlib.util as iu
import sys
from pathlib import Path
from typing import Any

import httpx
from dotenv import dotenv_values

env_path = Path(__file__).resolve().parent.parent / ".env"
if not env_path.exists():
    raise FileNotFoundError(f".env not found: {env_path}")
env_values = dotenv_values(env_path)
ollama_local_url = env_values["OLLAMA_LOCAL_URL"]
ollama_remote_url = env_values["OLLAMA_REMOTE_URL"]
openrouter_api_key = env_values["OPENROUTER_API_KEY"]
openrouter_model = env_values["OPENROUTER_MODEL"]

modules_to_check = ["uv", "httpx", "ruff", "pyright", "pytest", "pydantic"]

print("Python Version:" + sys.version)


def check_modules(modules):
    for module in modules:
        spec = iu.find_spec(module)
        if spec is not None:
            print(spec)
        else:
            print(module + " Not installed")


async def ping_ollama(
    client: httpx.AsyncClient,
    ollama_remote_url: str | None,
) -> dict[str, Any]:

    try:
        if not ollama_remote_url:
            raise ValueError("OLLAMA_REMOTE_URL is missing in .env")

        response = await client.get(
            f"{ollama_remote_url.rstrip('/')}/api/version",
            timeout=3.0,
        )
        response.raise_for_status()

        return {
            "service": "ollama",
            "success": True,
            "status_code": response.status_code,
            "details": response.json(),
            "error": None,
        }

    except ValueError as exc:
        return {
            "service": "ollama",
            "success": False,
            "status_code": None,
            "details": None,
            "error": str(exc),
        }

    except httpx.HTTPError as exc:
        return {
            "service": "ollama",
            "success": False,
            "status_code": (
                exc.response.status_code if isinstance(exc, httpx.HTTPStatusError) else None
            ),
            "details": None,
            "error": str(exc),
        }


async def call_openrouter(
    client: httpx.AsyncClient,
    api_key: str,
) -> dict:

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": openrouter_model,
        "messages": [{"role": "user", "content": "Reply with: OpenRouter connection successful."}],
        "max_tokens": 50,
    }

    try:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

        return {
            "success": True,
            "status_code": response.status_code,
            "model": data.get("model"),
            "answer": data["choices"][0]["message"]["content"],
        }

    except httpx.HTTPStatusError as exc:
        # Get the actual error returned by OpenRouter
        try:
            error_details = exc.response.json()
        except ValueError:
            error_details = exc.response.text

        return {
            "success": False,
            "status_code": exc.response.status_code,
            "error": error_details,
        }

    except httpx.RequestError as exc:
        return {
            "success": False,
            "error": str(exc),
        }


# Run the async loop
# asyncio.run(ping_ollama())
check_modules(modules_to_check)


async def main():

    async with httpx.AsyncClient(timeout=10.0) as client:
        # ollama_result, openrouter_result = await asyncio.gather(
        #    ping_ollama(client, ollama_remote_url),
        #    call_openrouter(client, openrouter_api_key),
        # )
        tasks = [ping_ollama(client, ollama_remote_url)]

        if openrouter_api_key:
            tasks.append(call_openrouter(client, openrouter_api_key))

        results = await asyncio.gather(*tasks)

        ollama_result = results[0]
        openrouter_result = results[1] if len(results) > 1 else None

        print("Ollama:", ollama_result)
        print("OpenRouter:", openrouter_result)


asyncio.run(main())
