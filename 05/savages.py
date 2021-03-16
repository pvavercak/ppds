from fei.ppds import Mutex, Semaphore, Thread, print
from random import randint
from time import sleep

TIME_DIVIDER = 10


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


def get_serving(id, shared):
    print(f"divoch {id:02}: beriem si veceru")
    shared.servings -= 1


def eat_serving(id):
    print(f"divoch {id:02}: hodujem")
    sleep(randint(3, 4) / TIME_DIVIDER)


def make_servings(shared):
    print("kuchar: varim")
    sleep(randint(3, 6) / TIME_DIVIDER)
    shared.servings = shared.SERVINGS_NEEDED


def savage(shared):
    pass


def cook(shared):
    pass


def run():
    N_SAVAGES = 5

    shared = Shared(N_SAVAGES)

    thread_pool = [Thread(savage, i, shared) for i in range(N_SAVAGES)]
    thread_pool.append(Thread(cook, shared))

    [th.join() for th in thread_pool]


run()
