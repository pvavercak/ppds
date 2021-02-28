from fei.ppds import Thread, Mutex, Semaphore, print, Event
from time import sleep
from random import randint


def calculate_fibonacci_simple(mutex, fibonacci, thread_id):
    while True:
        sleep(randint(1,10)/10)
        mutex.lock()
        index = thread_id + 2
        mutex.unlock()
        if index == len(fibonacci):
            fibonacci.append(fibonacci[index-2] + fibonacci[index - 1])
            break


def test_simple_fibonacci(N):
    threads = list()
    fibonacci = [0, 1]
    mtx = Mutex()
    for thread_num in range(N):    
        threads.append(Thread(calculate_fibonacci_simple, mtx, fibonacci, thread_num))

    for t in threads:
        t.join()


def calculate_fibonacci(semaphores, fibonacci, thread_id):
    sleep(randint(1, 10)/10)
    if thread_id > 0:
        semaphores[thread_id - 1].wait()
    fibonacci.append(fibonacci[thread_id] + fibonacci[thread_id + 1])
    semaphores[thread_id].signal()


def test_fibonacci(N):
    threads = list()
    sync = list()
    fibonacci = [0, 1]
    for _ in range(N):
        sync.append(Event())
    # Implementacia moze byt aj pomocou Semaphore objektu:
    # for _ in range(N):
    #     sync.append(Semaphore(0))
    for thread_id in range(N):
        threads.append(Thread(calculate_fibonacci, sync, fibonacci, thread_id))

    for t in threads:
        t.join()


test_simple_fibonacci(5)
test_fibonacci(200)
