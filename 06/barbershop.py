from fei.ppds import print, Thread, Semaphore, Mutex
from time import sleep
from random import randint


class Shared():
    def __init__(self, customer_capacity):
        self.N = customer_capacity
        self.customers = 0
        self.mutex = Mutex()

        self.barber = Semaphore(0)
        self.customer = Semaphore(0)

        self.barber_done = Semaphore(0)
        self.customer_done = Semaphore(0)


def cut_hair():
    sleep(randint(0,2)/10 + 0.5)


def get_haircut():
    sleep(randint(0, 3)/10 + 0.7)


def customer(shared):
    pass


def barber(shared):
    while True:
        shared.customer.wait()
        shared.barber.signal()

        cut_hair(shared)

        shared.customer_done.wait()
        shared.barber_done.signal()


def run_threads():
    N_CUSTOMERS = 3
    CAP = 2
    barbershop = Shared(CAP)

    threads = [Thread(customer, id + 1, barbershop)
               for id in range(N_CUSTOMERS)]
    threads.append(Thread(barber, barbershop))

    [th.join() for th in threads]


run_threads()
