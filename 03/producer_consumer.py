from fei.ppds import Mutex, Semaphore, Thread
from time import sleep
from random import randint


class WareHouse:
    def __init__(self, capacity):
        self.free_space = Semaphore(capacity)
        self.items = Semaphore(0)
        self.mutex = Mutex()
        self.produced = 0
        self.closed = False


def producer(warehouse, time_to_produce, time_to_store):
    while True:
        sleep(time_to_produce)
        warehouse.free_space.wait()
        warehouse.mutex.lock()
        sleep(time_to_store)
        warehouse.produced += 1
        warehouse.mutex.unlock()
        warehouse.items.signal()
        if warehouse.closed:
            break


def consumer(warehouse, time_to_gain):
    while True:
        warehouse.items.wait()
        warehouse.mutex.lock()
        sleep(time_to_gain)
        warehouse.mutex.unlock()
        warehouse.free_space.signal()
        sleep(randint(1, 10) / 500)
        if warehouse.closed:
            break


def producer_consumer_benchmark():
    keys = ["production_times", "producers_count", "produced_items"]
    data = {keys[0]: [], keys[1]: [], keys[2]: []}
    repeat = 1
    service_time = 0.1
    for t_production in range(1, 5):
        for n_producers in range(1, 5):
            partial_sum = 0
            production_time = t_production / 100
            for _ in range(repeat):
                warehouse = WareHouse(10)
                consumers = [Thread(consumer, warehouse, 0.05)
                             for _ in range(10)]
                producers = [
                    Thread(producer, warehouse, production_time, 0.01)
                    for _ in range(n_producers)]

                sleep(service_time)
                warehouse.closed = True
                warehouse.items.signal(100)
                warehouse.free_space.signal(100)

                for thread in consumers + producers:
                    thread.join()

                partial_sum += warehouse.produced / service_time
            produced_per_sec = partial_sum / repeat
            print(produced_per_sec)
            data[keys[0]].append(production_time)
            data[keys[1]].append(n_producers)
            data[keys[2]].append(produced_per_sec)
    return data
