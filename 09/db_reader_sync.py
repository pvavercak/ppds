#!/usr/bin/env python3
import sqlite3
import queue

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

        result = db_connection.execute(query)
        row = result.fetchone()
        print(f"{task_name}: {country} - {row[0]}")
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
        while not done:
            for task in tasks:
                try:
                    next(task)
                except StopIteration:
                    tasks.remove(task)
                if len(tasks) == 0:
                    done = True


if __name__ == "__main__":
    main()
