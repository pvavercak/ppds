from fei.ppds import Event, Thread, Mutex, print, Semaphore
from time import sleep
from random import randint


class SimpleBarrier:
    def __init__(self, num_of_threads):
        self.N = num_of_threads
        self.cnt = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.N:
            self.cnt = 0
            for _ in range(self.N):
                self.turnstile.signal()
        self.mutex.unlock()
        self.turnstile.wait()


class SimpleBarrierEvent:
    def __init__(self, num_of_threads):
        self.N = num_of_threads
        self.C = num_of_threads
        self.mutex = Mutex()
        self.turnstile = Event()

    def wait(self):
        self.mutex.lock()
        if self.C == 0:
            self.turnstile.clear()
            self.C += 1
            if self.C == self.N:
                self.turnstile.set()
        self.mutex.unlock()
        self.turnstile.wait()


def simple_barrier_example(barrier, thread_id):
    sleep(randint(1,10)/10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


def test_simple_barrier(num_of_threads):
    sb = SimpleBarrier(num_of_threads)
    threads = list()
    for i in range(num_of_threads):
        t = Thread(simple_barrier_example, sb, i)
        threads.append(t)

    for t in threads:
        t.join()


def rendezvous(thread_name):
    sleep(randint(1,10)/10)
    print(f"rendezvous: {thread_name}")


def ko(thread_name):
    print(f"ko: {thread_name}")
    sleep(randint(1,10)/10)


def reusable_barrier_example(barrier1, barrier2, thread_name):
    while True:
        rendezvous(thread_name)
        barrier1.wait()
        ko(thread_name)
        barrier2.wait()


def test_reusable_barrier(num_of_threads):
    sb1 = SimpleBarrier(num_of_threads)
    sb2 = SimpleBarrier(num_of_threads)
    threads = list()
    for i in range(num_of_threads):
        t = Thread(reusable_barrier_example, sb1, sb2, f"Thread {i}")
        threads.append(t)

    for t in threads:
        t.join()


test_simple_barrier(5)
test_reusable_barrier(5)
