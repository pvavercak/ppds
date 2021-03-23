from fei.ppds import print, Thread, Semaphore, Mutex
from time import sleep
from random import randint


class Shared():
    def __init__(self, N):
        pass


def customer(shared):
    pass


def barber(shared):
    pass


def run_threads():
    N_CUSTOMERS = 5
    barbershop = Shared(N_CUSTOMERS)

    threads = [Thread(customer, barbershop) for _ in range(N_CUSTOMERS)]
    threads.append(Thread(barber, barbershop))

    [th.join() for th in threads]


run_threads()
