#!/usr/bin/env python3
import aiosqlite
import asyncio
import time

COUNTRIES = [
    "Slovakia",
    "China",
    "USA",
    "Czech Republic",
    "Poland",
    "Taiwan"
]

sum_times = 0


async def get_capital(task_name, work_queue, db_connection):
    global sum_times
    while not work_queue.empty():
        country = await work_queue.get()
        query = f"SELECT capital FROM CAPITALS WHERE country='{country}'"
        print(f"{task_name}: running")
        t = time.perf_counter_ns()

        async with db_connection.execute(query) as result:
            row = await result.fetchone()
            diff = time.perf_counter_ns() - t
            print(f"{task_name}: {country} - {row[0]},"
                  f" time elapsed {diff} [ns]")
            sum_times += diff


async def main():
    countries = asyncio.Queue()
    for country in COUNTRIES:
        await countries.put(country)

    async with aiosqlite.connect("capitals.db") as db_connection:
        tasks = [
            get_capital("One", countries, db_connection),
            get_capital("Two", countries, db_connection)]

        t = time.perf_counter_ns()
        await asyncio.gather(*tasks)
        diff = time.perf_counter_ns() - t
        print(f"{diff} [ns] vs {sum_times} [ns]"
              " (app runtime vs sum of partial times)")


if __name__ == "__main__":
    asyncio.run(main())
