import time
import queue
import urllib.request


URLS = [
    'http://stuba.sk',
    'http://facebook.com',
    'http://uim.fei.stuba.sk',
    'http://google.com'
]


def task(name, work_queue):
    while not work_queue.empty():
        url = work_queue.get()
        print(f"Task {name} getting URL: {url}")
        start = time.perf_counter()
        urllib.request.urlopen(url)
        diff = time.perf_counter() - start
        print(f"Task {name} elapsed: {diff:.1f}s")
        yield


def main():
    work_queue = queue.Queue()

    for url in URLS:
        work_queue.put(url)

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
