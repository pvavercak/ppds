import time
import asyncio


async def task(name, work_queue):
    while not work_queue.empty():
        delay = await work_queue.get()
        print(f"Task {name} running")
        start = time.perf_counter()
        await asyncio.sleep(delay)
        diff = time.perf_counter() - start
        print(f"Task {name} elapsed: {diff:.1f}s")


async def main():
    work_queue = asyncio.Queue()

    for i in [3, 4, 2, 1]:
        await work_queue.put(i)

    tasks = [
        task("One", work_queue),
        task("Two", work_queue)
    ]

    start = time.perf_counter()
    await asyncio.gather(*tasks)
    diff = time.perf_counter() - start
    print(f"Application Finished in {diff:.1f}s")


if __name__ == '__main__':
    asyncio.run(main())
