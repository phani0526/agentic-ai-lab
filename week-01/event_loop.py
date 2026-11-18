import asyncio
import time


async def fake_llm_call(name: str, seconds: float) -> str:
    """Pretend to call an LLM: the sleep stands in for waiting on the network."""
    print(f"{time.perf_counter() - T0:5.2f}s  start {name}")
    await asyncio.sleep(seconds)  # pause here → loop runs other tasks
    print(f"{time.perf_counter() - T0:5.2f}s  done  {name}")
    return f"answer from {name}"


async def sequential() -> None:
    for name, secs in [("nemotron", 2), ("qwen3", 3), ("gemma", 1)]:
        await fake_llm_call(name, secs)  # wait for each before starting the next


async def concurrent() -> None:
    results = await asyncio.gather(  # start all three, wait for all
        fake_llm_call("nemotron", 2),
        fake_llm_call("qwen3", 3),
        fake_llm_call("gemma", 1),
    )
    print(results)  # results come back in the order you passed them


T0 = time.perf_counter()
asyncio.run(sequential())
print("---")
T0 = time.perf_counter()
asyncio.run(concurrent())
