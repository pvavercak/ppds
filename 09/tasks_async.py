import queue
import time


def task(name, work_queue):
    while not work_queue.empty():
        start = time.perf_counter()
        count = work_queue.get()
        total = 0
        print(f"Task {name} running")
        for i in range(count):
            total += 1
            yield
        diff = time.perf_counter() - start
        print(f"Task {name} total: {total} time elapsed: {diff:.10f}s")


def main():
    work_queue = queue.Queue()

    for i in [15, 50, 100, 150]:
        work_queue.put(i)

    tasks = [
        task("First_Task", work_queue),
        task("Second_Task", work_queue)
    ]

    done = False
    start = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)
            if len(tasks) == 0:
                done = True
    diff = time.perf_counter() - start
    print(f"Application Finished in {diff:.10f}s")


if __name__ == '__main__':
    main()
