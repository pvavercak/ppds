from fei.ppds import Mutex, Semaphore
from time import sleep
from random import randint


class WareHouse:
    def __init__(self, capacity):
        self.free_space = Semaphore(capacity)
        self.items = Semaphore(0)
        self.mutex = Mutex()


def producer(warehouse, time_to_produce, time_to_store):
    sleep(time_to_produce)
    warehouse.free_space.wait()
    warehouse.mutex.lock()
    sleep(time_to_store)
    warehouse.mutex.unlock()
    warehouse.items.signal()


def consumer(warehouse, time_to_gain):
    warehouse.items.wait()
    warehouse.mutex.lock()
    sleep(time_to_gain)
    warehouse.mutex.unlock()
    warehouse.free_space.signal()
    sleep(randint(1, 10) / 500)
