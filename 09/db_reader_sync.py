#!/usr/bin/env python3
import sqlite3
import queue
import time

COUNTRIES = [
    "Slovakia",
    "China",
    "USA",
    "Czech Republic",
    "Poland",
    "Taiwan"
]


def get_capital(task_name, work_queue, db_connection):
    while not work_queue.empty():
        country = work_queue.get()
        query = f"SELECT capital FROM CAPITALS WHERE country='{country}'"
        print(f"{task_name}: running")
        t = time.perf_counter_ns()

        result = db_connection.execute(query)
        row = result.fetchone()

        diff = time.perf_counter_ns() - t
        print(f"{task_name}: {country} - {row[0]},"
              f" time elapsed {diff} [ns]")
        yield


def main():
    countries = queue.Queue()
    for country in COUNTRIES:
        countries.put(country)

    with sqlite3.connect("capitals.db") as db_connection:
        tasks = [
            get_capital("One", countries, db_connection),
            get_capital("Two", countries, db_connection)]

        done = False
        t = time.perf_counter_ns()
        diff = None

        while not done:
            for task in tasks:
                try:
                    next(task)
                except StopIteration:
                    tasks.remove(task)
                if len(tasks) == 0:
                    diff = time.perf_counter_ns() - t
                    done = True

        print(f"Application runtime {diff} [ns]")


if __name__ == "__main__":
    main()
