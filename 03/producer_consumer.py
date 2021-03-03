from fei.ppds import Mutex, Semaphore


class WareHouse:
    def __init__(self, capacity):
        self.free_space = Semaphore(capacity)
        self.items = Semaphore(0)
        self.mutex = Mutex()


def producer(warehouse):
    pass


def consumer(warehouse):
    pass
