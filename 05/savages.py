from fei.ppds import Mutex, Semaphore, Thread, print
from random import randint
from time import sleep

TIME_DIVIDER = 1


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self, print_str, id, print_last=False, print_each=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each:
            print(print_str.format(id, self.cnt))
        if self.cnt == self.N:
            self.cnt = 0
            if print_last:
                print(print_str.format(id))
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


class Shared():
    def __init__(self, n_savages=5, n_cooks=3):
        self.servings = 0
        self.mutex = Mutex()
        self.SERVINGS_NEEDED = n_savages

        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)

        self.barrier1 = SimpleBarrier(n_savages)
        self.barrier2 = SimpleBarrier(n_savages)

        self.cookBarrier1 = SimpleBarrier(n_cooks)
        self.cookBarrier2 = SimpleBarrier(n_cooks)


def get_serving(savage_id, shared):
    print(f"divoch {savage_id:02}: beriem si veceru")
    shared.servings -= 1


def eat_serving(savage_id):
    print(f"divoch {savage_id:02}: hodujem")
    sleep(randint(3, 4) / TIME_DIVIDER)


def make_servings(cook_id, shared):
    print(f"kuchar {cook_id:02}: varim")
    sleep(randint(3, 6) / TIME_DIVIDER)
    shared.servings = shared.SERVINGS_NEEDED


def savage(savage_id, shared):
    while True:
        shared.barrier1.wait(
            "divoch {0:02}: prisiel som na veceru, uz nas je {1:02}",
            savage_id,
            print_each=True)
        shared.barrier2.wait(
            "divoch {0:02}: uz sme vsetci, zaciname vecerat",
            savage_id,
            print_last=True)
        shared.mutex.lock()
        if not shared.servings:
            print(f"savage_{savage_id}: budim kuchara")
            shared.empty_pot.signal()
            shared.full_pot.wait()
        get_serving(savage_id, shared)
        shared.mutex.unlock()
        eat_serving(savage_id)


def cook(cook_id, shared):
    while True:
        shared.empty_pot.wait()
        make_servings(shared)
        shared.full_pot.signal()


def run():
    N_SAVAGES = 5
    N_COOKS = 2

    shared = Shared(N_SAVAGES, N_COOKS)

    savages = [Thread(savage, i, shared) for i in range(N_SAVAGES)]

    cooks = [Thread(cook, i, shared) for i in range(N_COOKS)]

    [th.join() for th in savages + cooks]


run()
