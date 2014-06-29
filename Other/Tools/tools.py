#! /usr/bin/env python
# -*- coding:Utf8 -*-

"Useful functions"

from itertools import islice, zip_longest, chain

#######################################
#### Classes, Methods, Functions : ####
#######################################


def morceaux_format(iterable, step=1, format=iter):
    """
        Iterate through an <iterable> object by pieces
        and return <format> of elements (iterator, list, set, tuple)
        Be careful :
            If step > iterable rest ---> last output length lower than step
    """
    it = iter(iterable)
    while True:
        yield format(chain((next(it),), islice(it, step - 1)))


def morceaux(iterable, step=1, fillvalue=None):
    """
        Iterate through an iterable object by pieces
        and return tuples of elements.
        If step > iterable rest
            ---> missing values are filled-in with <fillvalue> argument
    """
    return zip_longest(*[iter(iterable)] * step, fillvalue=fillvalue)

########################
#### Main Program : ####
########################


if __name__ == '__main__':
    a = range(0, 20, 1)
    print("morceaux function example")
    print(type(morceaux(a, 3)))
    for el in morceaux(a, 3):
        print(el, "------------->", type(el))
    print("\nmorceaux_format function example")
    for el in morceaux_format(a, step=3):
        print(el, "------------->", type(el))
    for el in morceaux_format(a, step=3, format=set):
        print(el, "------------->", type(el))
