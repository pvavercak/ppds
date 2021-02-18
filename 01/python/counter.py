from fei.ppds import Thread, Mutex


class Shared():
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()

    def safe_increment(self):
        if self.counter < self.end:
            self.array[self.counter] += 1


class Histogram(dict):
    def __init__(self, seq=[]):
        for item in seq:
            self[item] = self.get(item, 0) + 1


def counter1(shared):
    while True:
        if shared.counter >= shared.end:
            break
        shared.mutex.lock()
        if shared.counter < shared.end:
            shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


def counter2(shared):
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            shared.mutex.unlock()
            break
        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


def counter3(shared):
    while True:
        shared.mutex.lock()
        cnt = shared.counter
        shared.counter +=1
        shared.mutex.unlock()
        if cnt >= shared.end:
            break
        shared.array[cnt] += 1


for i in range(5):
    sh = Shared(1_000_000)
    t1 = Thread(counter3, sh)
    t2 = Thread(counter3, sh)

    t1.join()
    t2.join()

    print(Histogram(sh.array))
