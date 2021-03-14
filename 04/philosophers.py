from fei.ppds import Thread, Semaphore, print

from time import sleep
from random import randint


PHIL_NUM = 5


# def phil(forks, footman, phil_id):
#     while True:
#         think(phil_id)
#         get_forks(forks, footman, phil_id)
#         eat(phil_id)
#         put_forks(forks, footman, phil_id)


def phil(forks, phil_id, fork1, fork2):
    while True:
        think(phil_id)
        get_forks(forks, phil_id, fork1, fork2)
        eat(phil_id)
        put_forks(forks, phil_id, fork1, fork2)


def think(phil_id):
    print(f'{phil_id:02d}: thinking')
    sleep(randint(40, 50)/1000)


def eat(phil_id):
    print(f'{phil_id:02d}: eating')
    sleep(randint(40, 50)/1000)


# def get_forks(forks, footman, phil_id):
#     footman.wait()
#     forks[phil_id].wait()
#     forks[(phil_id + 1) % PHIL_NUM].wait()


def get_forks(forks, phil_id, fork1, fork2):
    forks[fork1].wait()
    forks[fork2].wait()


# def put_forks(forks, footman, phil_id):
#     footman.signal()
#     forks[phil_id].signal()
#     forks[(phil_id + 1) % PHIL_NUM].signal()

def put_forks(forks, phil_id, fork1, fork2):
    forks[fork1].signal()
    forks[fork2].signal()


def main():
    forks = [Semaphore(1) for _ in range(PHIL_NUM)]
    footman = Semaphore(PHIL_NUM - 1)

    # phils = [Thread(phil, forks, footman, id) for id in range(PHIL_NUM)]

    lefties = randint(1, PHIL_NUM - 1)
    phil_type = [0] * lefties + [1] * (PHIL_NUM - lefties)
    phils = list()
    for phil_id in range(PHIL_NUM):
        if phil_type[phil_id]:
            phils.append(
                Thread(phil, forks, phil_id, phil_id, ((phil_id+1) % PHIL_NUM)
                       ))
        else:
            phils.append(
                Thread(phil, forks, phil_id, ((phil_id+1) % PHIL_NUM), phil_id
                       ))

    for p in phils:
        p.join()


if __name__ == '__main__':
    main()
