from fei.ppds import print, Thread, Semaphore, Mutex
from time import sleep
from random import randint


TIME_OF_SERVICE = 1
TIME_DIVIDER = 10


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
    sleep(TIME_OF_SERVICE / TIME_DIVIDER)


def get_haircut():
    sleep(TIME_OF_SERVICE / TIME_DIVIDER)


def try_next_time():
    sleep(randint(2, 3) / TIME_DIVIDER)


def grow_hair():
    sleep(randint(2, 4) / TIME_DIVIDER)


def customer(shared):
    while True:
        shared.mutex.lock()
        if shared.N == shared.customers:
            shared.mutex.unlock()
            try_next_time()
        else:
            shared.customers += 1
            shared.mutex.unlock()
            shared.customer.signal()
            shared.barber.wait()

            get_haircut()

            shared.customer_done.signal()
            shared.barber_done.wait()

            shared.mutex.lock()
            shared.customers -= 1
            shared.mutex.unlock()

            grow_hair()


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
