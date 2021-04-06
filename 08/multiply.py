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
