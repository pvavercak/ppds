import time
import queue


def task(name, work_queue):
    if work_queue.empty():
        print(f"Task {name} nothing to do")
    else:
        while not work_queue.empty():
            count = work_queue.get()
            total = 0
            print(f"Task {name} running")
            for i in range(count):
                total += 1
            print(f"Task {name} total: {total}")


def main():
    work_queue = queue.Queue()

    for i in [1,5,7,9]:
        work_queue.put(i)
    
    tasks = [
        (task, "First_Task", work_queue),
        (task, "Second_Task", work_queue),
    ]

    for t, n, q in tasks:
        t(n, q)


if __name__ == '__main__':
    main()
