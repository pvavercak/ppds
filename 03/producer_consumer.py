from fei.ppds import Mutex, Semaphore, Thread
from time import sleep
from time import time as timestamp
from random import randint
import pickle


def save_to_pickle(results):
    tstmp = str(timestamp()).replace('.', '-')
    unique_filename = f"results-{tstmp}.pickle"
    with open(unique_filename, "wb") as file_handle:
        pickle.dump(results, file_handle)


def load_from_pickle(pickle_file):
    results = dict()
    with open(pickle_file, "rb") as file_handle:
        results = pickle.load(file_handle)
    return results


class WareHouse:
    def __init__(self, capacity):
        self.free_space = Semaphore(capacity)
        self.items = Semaphore(0)
        self.mutex = Mutex()
        self.produced = 0
        self.consumed = 0
        self.closed = False

    def produce(self, time_to_produce):
        sleep(time_to_produce)
        self.mutex.lock()
        self.produced += 1
        self.mutex.unlock()

    def consume(self, time_to_consume):
        sleep(time_to_consume)
        self.mutex.lock()
        self.consumed += 1
        self.mutex.unlock()

    def stop_production(self, time_period):
        sleep(time_period)
        self.closed = True
        self.items.signal(100)
        self.free_space.signal(100)


def producer(warehouse, time_to_produce, time_to_store):
    while True:
        warehouse.produce(time_to_produce)
        warehouse.free_space.wait()
        warehouse.mutex.lock()
        sleep(time_to_store)
        warehouse.mutex.unlock()
        warehouse.items.signal()
        if warehouse.closed:
            break


def consumer(warehouse, time_to_consume):
    while True:
        warehouse.items.wait()
        warehouse.mutex.lock()
        sleep(randint(1, 10) / 500)
        warehouse.mutex.unlock()
        warehouse.free_space.signal()
        warehouse.consume(time_to_consume)
        if warehouse.closed:
            break


def producer_benchmark(repetitions, service_time):
    keys = ["production_times", "producers_count", "produced_items"]
    data = {keys[0]: [], keys[1]: [], keys[2]: []}
    for t_production in range(1, 5):
        for n_producers in range(1, 5):
            partial_sum = 0
            production_time = t_production / 100
            for _ in range(repetitions):
                warehouse = WareHouse(10)
                consumers = [Thread(consumer, warehouse, 0.05)
                             for _ in range(10)]
                producers = [
                    Thread(producer, warehouse, production_time, 0.01)
                    for _ in range(n_producers)]
                warehouse.stop_production(service_time)
                [thread.join() for thread in consumers + producers]
                partial_sum += warehouse.produced / service_time
            produced_per_sec = partial_sum / repetitions
            data[keys[0]].append(production_time)
            data[keys[1]].append(n_producers)
            data[keys[2]].append(produced_per_sec)
    save_to_pickle(data)
    return data
