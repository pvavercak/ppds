#!/usr/bin/env python3

def dispatch(multipliers):
    try:
        pass
    except GeneratorExit:
        pass


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
    try:
        pass
    except GeneratorExit:
        pass
