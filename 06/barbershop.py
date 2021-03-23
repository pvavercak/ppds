from fei.ppds import print, Thread, Semaphore, Mutex
from time import sleep
from random import randint


class Shared():
    def __init__(self, N):
        self.N = N
        self.customers = 0
        self.mutex = Mutex()

        self.barber = Semaphore(0)
        self.customer = Semaphore(0)

        self.barberDone = Semaphore(0)
        self.customerDone = Semaphore(0)


def cut_hair():
    sleep(randint(0,2)/10 + 0.5)


def get_haircut():
    sleep(randint(0, 3)/10 + 0.7)


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
