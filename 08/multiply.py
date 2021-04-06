#!/usr/bin/env python3

def dispatch(multipliers):
    try:
        while True:
            num = (yield)
            for multiplier in multipliers:
                multiplier.send(num)
    except GeneratorExit:
        for multiplier in multipliers:
            multiplier.close()


def send_numbers(nums, dispatch_fnc):
    for num in nums:
        dispatch_fnc.send(num)
    dispatch_fnc.close()


def num_multiplier(multiplier, printer):
    try:
        while True:
            num = (yield)
            printer.send(num * multiplier)
    except GeneratorExit:
        pass


def num_printer(multiplier):
    n = 0
    try:
        while True:
            n = (yield)
            print(f"{n:02} = {multiplier} x {n // multiplier}")
    except GeneratorExit:
        pass


numbers = [1, 2, 3, 4, 5, 6]
multipliers = [6, 5, 4, 3, 2, 1]

multipliers_list = list()

for m in multipliers:
    p = num_printer(m)
    next(p)

    nm = num_multiplier(m, p)
    next(nm)
    multipliers_list.append(nm)


dispatcher = dispatch(multipliers_list)
next(dispatcher)
send_numbers(numbers, dispatcher)
