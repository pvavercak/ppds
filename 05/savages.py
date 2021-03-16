from fei.ppds import Mutex, Semaphore, Thread, print
from random import randint
from time import sleep


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.mutex = Mutex()
        self.cnt = 0
        self.sem = Semaphore(0)

    def wait(self, print_str, savage_id, print_last=False, print_each=False):
        self.mutex.lock()
        self.cnt += 1
        if print_each:
            print(print_str.format(savage_id, self.cnt))
        if self.cnt == self.N:
            self.cnt = 0
            if print_last:
                print(print_str.format(savage_id))
            self.sem.signal(self.N)
        self.mutex.unlock()
        self.sem.wait()


class Shared():
    def __init__(self, N=5):
        self.servings = 0
        self.mutex = Mutex()

        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(N)
        self.barrier2 = SimpleBarrier(N)


def savage(shared):
    pass


def cook(shared):
    pass


def run():
    N_SAVAGES = 5
