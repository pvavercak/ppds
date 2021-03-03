from fei.ppds import Thread, Mutex, Semaphore


class LightSwitch:
    """Implementacia lightswitch ADT."""

    def __init__(self):
        self.cnt = 0
        self.mutex = Mutex()

    def lock(self, sem):
        """Zamknutie Semaphore objektu.

        sem -- Semaphore objekt sluziaci na synchronizaciu vlakien
        """
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == 1:
            sem.wait()
        self.mutex.unlock()

    def unlock(self, sem):
        """Odomknutie Semaphore objektu.

        sem -- Semaphore objekt sluziaci na synchronizaciu vlakien
        """
        self.mutex.lock()
        self.cnt -= 1
        if self.cnt == 0:
            sem.signal()
        self.mutex.unlock()
