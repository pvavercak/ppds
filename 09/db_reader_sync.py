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
    pass


def main():
    countries = queue.Queue()
    for country in COUNTRIES:
        countries.put(country)

    with sqlite3.connect("capitals.db") as db_connection:
        get_capital("One", countries, db_connection)


if __name__ == "__main__":
    main()
