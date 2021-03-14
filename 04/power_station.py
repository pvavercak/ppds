from fei.ppds import Mutex, Event, Semaphore, Thread


N_SENSORS = 3
N_MONITORS = 8


class LightSwitch:
    def __init__(self):
        self.cnt = 0
        self.mutex = Mutex()

    def lock(self, sem):
        pass

    def unlock(self, sem):
        pass


def sensor(id):
    pass


def monitor(id):
    pass


data_present = Event()
block_sensors = Semaphore(1)
block_monitors = Semaphore(1)
sensor_ls = LightSwitch()
monitor_ls = LightSwitch()

sensors = [Thread(sensor, sensor_id) for sensor_id in range(N_SENSORS - 1)]
sensors.append(Thread(sensor, N_SENSORS - 1))

monitors = [Thread(monitor, monitor_id) for monitor_id in range(N_MONITORS)]

[thread.join() for thread in sensors + monitors]
