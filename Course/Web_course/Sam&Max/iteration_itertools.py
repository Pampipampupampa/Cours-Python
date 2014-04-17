#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""ITERTOOLS OR MAGIC ITERATIONS"""
"SAM AND MAX"

########################################
#### Classes and Methods imported : ####
########################################

import itertools

#####################
#### Constants : ####
#####################

#######################################
#### Classes, Methods, Functions : ####
#######################################


class DistributeurDeCapote():
    stock = True

    def allumer(self):
        while self.stock:
            yield "capote"


class myItertool(object):
    """Euh, ..."""

    def __iter__(self):
        yield "python"
        yield "c'est déjà"
        yield "fini."


########################
#### Main Program : ####
########################

# Example with itertools
d = DistributeurDeCapote().allumer()
generateur = itertools.chain("12345", d)
generateur = itertools.islice(generateur, 0, 10)
for x in generateur:
    print(x)

# How works iteration ?
gen = iter(myItertool())
try:
    print(next(gen))
    print(next(gen))
    print(next(gen))
    print(next(gen))
except StopIteration as e:
    print("Stop, no more elements")  # yes we use exception to top iteration

gen = iter(myItertool())
for el in gen:
    print(el)
