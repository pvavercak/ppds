import queue
import time


def task(name, work_queue):
    while not work_queue.empty():
        delay = work_queue.get()
        print(f"Task {name} running")
        start = time.perf_counter()
        time.sleep(delay)
        diff = time.perf_counter() - start
        print(f"Task {name} elapsed: {diff:.1f}s")
        yield


def main():
    work_queue = queue.Queue()

    for i in [3, 4, 2, 1]:
        work_queue.put(i)

    tasks = [
        task("One", work_queue),
        task("Two", work_queue)
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
    print(f"Application Finished in {diff:.1f}s")


if __name__ == '__main__':
    main()
