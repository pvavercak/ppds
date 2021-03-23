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


def cut_hair(n_of_customers):
    print(
        f"barber: striham zakaznika, pocet cakajucich {n_of_customers}")
    sleep(TIME_OF_SERVICE / TIME_DIVIDER)


def get_haircut(cid, noc):
    print(
        f"cust_{cid:02}: som v hlavnom kresle, pocet cakajucich je {noc:02}")
    sleep(TIME_OF_SERVICE / TIME_DIVIDER)


def try_next_time(cid):
    print(f"cust_{cid:02}: kadernictvo je plne, pridem inokedy")
    sleep(randint(2, 3) / TIME_DIVIDER)


def grow_hair(cid):
    print(f"cust_{cid:02}: cakam, kym mi dorastu vlasy")
    sleep(randint(2, 4) / TIME_DIVIDER)


def customer(cid, shared):
    while True:
        shared.mutex.lock()
        if shared.N == shared.customers:
            shared.mutex.unlock()
            try_next_time(cid)
        else:
            shared.customers += 1
            print(f"cust_{cid:02}: posadil som sa do cakacieho kresla")
            shared.mutex.unlock()
            shared.customer.signal()
            shared.barber.wait()

            get_haircut(cid, shared.customers)

            shared.customer_done.signal()
            shared.barber_done.wait()

            shared.mutex.lock()
            shared.customers -= 1
            shared.mutex.unlock()

            grow_hair(cid)


def barber(shared):
    while True:
        shared.customer.wait()
        shared.barber.signal()

        cut_hair(shared.customers - 1)

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
