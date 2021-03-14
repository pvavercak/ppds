from fei.ppds import Mutex, Event, Semaphore, Thread, print
from typing import Callable
from random import randint
from time import sleep

N_SENSORS = 3
N_MONITORS = 8


class LightSwitch:
    def __init__(self):
        self.cnt = 0
        self.mutex = Mutex()

    def lock(self, sem):
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == 1:
            sem.wait()
        self.mutex.unlock()
        return self.cnt

    def unlock(self, sem):
        self.mutex.lock()
        self.cnt -= 1
        if self.cnt == 0:
            sem.signal()
        self.mutex.unlock()


def sensor(id, update_time: Callable[[], float], data_present,
           sensor_ls, block_sensors, block_monitors):
    while True:
        sensor_count = sensor_ls.lock(block_monitors)
        block_sensors.wait()
        update = update_time()
        print(
            f'cidlo {id}: pocet_zapisujucich_cidiel={sensor_count}, trvanie_zapisu={update}')
        sleep(update / 1000)
        block_sensors.signal()
        sensor_ls.unlock(block_monitors)
        data_present.signal()
        sleep(randint(50, 60) / 1000)


def monitor(id):
    pass


data_present = Event()
block_sensors = Semaphore(1)
block_monitors = Semaphore(1)
sensor_ls = LightSwitch()
monitor_ls = LightSwitch()

sensors = [
    Thread(sensor, sensor_id, lambda: randint(10, 20),
           data_present, sensor_ls,
           block_sensors, block_monitors)
    for sensor_id in range(N_SENSORS - 1)]

sensors.append(
    Thread(sensor, N_SENSORS - 1, lambda: randint(20, 25),
           data_present, sensor_ls,
           block_sensors, block_monitors))

monitors = [Thread(monitor, monitor_id) for monitor_id in range(N_MONITORS)]

[thread.join() for thread in sensors + monitors]
