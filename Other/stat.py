#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""Visitors stats"""

########################################
#### Classes and Methods imported : ####
########################################

import time
from functools import reduce, wraps
from random import randint

#######################################
#### Classes, Methods, Functions : ####
#######################################


def benchmark(func):
    """
        Time function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.process_time()
        res = func(*args, **kwargs)
        print("{} has spent {} sec to finish".format(func.__name__,
                                                     time.process_time()-t))
        return res
    return wrapper


# Used to unpack input
tuple_input = lambda: tuple(map(int, input().split()))


def dico_sol():
    days, number = tuple_input()
    visitors = tuple_input()

    cumul_dict = {}
    cumul_dict[0] = 0
    cumul_sum = 0
    for i, v in enumerate(visitors):
        cumul_sum += v
        cumul_dict[i+1] = cumul_sum

    for i in range(number):
        start, end = tuple_input()
        if 1 <= start <= end <= days:
            print(cumul_dict[end] - cumul_dict[start-1])


def list_sol():
    days, number = map(int, input().split())
    visitors = tuple_input()
    for loop in range(number):
        start, end = map(int, input().split())
        print(reduce(lambda x, y: x+y, visitors[start-1:end], 0))


# Test
@benchmark
def dico_sol_test(days, number, visitors):

    cumul_dict = {}
    cumul_dict[0] = 0
    cumul_sum = 0
    for i, v in enumerate(visitors):
        cumul_sum += v
        cumul_dict[i+1] = cumul_sum

    for _ in range(number):
        start = randint(1, len(visitors))
        end = randint(start, len(visitors))
        a = cumul_dict[end] - cumul_dict[start-1]


@benchmark
def list_sol_test(days, number, visitors):
    for _ in range(number):
        start = randint(1, len(visitors))
        end = randint(start, len(visitors))
        a = reduce(lambda x, y: x+y, visitors[start-1:end])


@benchmark
def main(days, number, visitors):
    cumul = 0

    def ajouter(nbVisiteurs):
        nonlocal cumul
        cumul += int(nbVisiteurs)
        return cumul

    nbVisiteursCumules = [0] + list(map(ajouter, visitors))
    for loop in range(number):
        start = randint(1, len(visitors))
        end = randint(start, len(visitors))
        a = nbVisiteursCumules[end] - nbVisiteursCumules[start-1]


def reduce_func(x, y):
    global nbVisiteursCumules
    nbVisiteursCumules.append(x+y)
    return x+y


@benchmark
def reduce_sol_test(days, number, visitors):
    global nbVisiteursCumules
    nbVisiteursCumules = [0]
    reduce(reduce_func, visitors)
    print(nbVisiteursCumules, len(nbVisiteursCumules))
    for _ in range(number):
        start = randint(1, len(visitors))
        end = randint(start, len(visitors))
        try:
            print(nbVisiteursCumules[end-1] - nbVisiteursCumules[start-1])
        except IndexError as e:
            print(start, end)
            raise e

########################
#### Main Program : ####
########################

if __name__ == '__main__':
    # dico_sol()
    # list_sol()

    days, number = 1000, 10000
    visitors = [i for i in range(1, 1001)]

    # dico_sol_test(days, number, visitors)
    # list_sol_test(days, number, visitors)
    # main(days, number, visitors)
    reduce_sol_test(days, number, visitors)


