#!/usr/bin/env python3

def dispatch(greps):
    try:
        while True:
            line = (yield)
            for grep in greps:
                grep.send(line)
    except GeneratorExit:
        for grep in greps:
            grep.close()


def cat(f, next_fnc):
    for line in f:
        next_fnc.send(line)
    next_fnc.close()


def grep(substring, next_fnc):
    try:
        while True:
            line = (yield)
            next_fnc.send(line.count(substring))
    except(GeneratorExit):
        next_fnc.close()


def wc(substring):
    n = 0
    try:
        while True:
            n += (yield)
    except GeneratorExit:
        print(substring, n, flush=True)


def run_dispatched_wc(substrings):
    f = open("test.txt", 'r')
    greps = list()
    
    for s in substrings:
        w = wc(s)
        next(w)
        g = grep(s, w)
        next(g)
        greps.append(g)
    
    d = dispatch(greps)
    next(d)
    cat(f, d)

substrings = ["test", "string", "test_string"]

run_dispatched_wc(substrings)
