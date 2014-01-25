#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""HOW TO USE AND CREATE CONTEXT MANAGER"""
" SAM AND MAX : WITH KEY WORD"

########################################
#### Classes and Methods imported : ####
########################################

import os
from contextlib import contextmanager  # Used to create simple context manager
from functools import wraps  # Use to keep decorated finction docstring access
import datetime

#####################
#### Constants : ####
#####################

#######################################
#### Classes, Methods, Functions : ####
#######################################


class MyContextManager(object):
    """How tocreate a simple context manger"""
    def __enter__(self):
        print("Just before !!")

    def __exit__(self, type, value, traceback):
        print("Just after")


class Cd(object):
    """Usefull context manger"""
    def __init__(self, dirname):
        self.dirname = dirname

    def __enter__(self):
        self.curdir = os.getcwd()
        os.chdir(self.dirname)
        return self.dirname, 33

    def __exit__(self, type, value, traceback):
        os.chdir(self.curdir)


@contextmanager
def tag(name):
    print("<{}>".format(name))
    yield name[::-1]
    print("</{}>".format(name))


class ContextDecorator(object):
    # __call__ is a magic function calls when we use () on an object
    def __call__(self, f):
        @wraps(f)
        def decorated(*args, **kwds):
            # with which calls itself, it's so kind
            with self:
                return f(*args, **kwds)
        return decorated


class TimeIt(ContextDecorator):
    """Context decorator used to time methods"""
    def __enter__(self):
        self.start = datetime.datetime.now()
        # print(self.start)

    def __exit__(self, type, value, traceback):
        print((datetime.datetime.now() - self.start).total_seconds())


def bad(max_range):
    liste = 0
    for el in range(0, max_range):
        if el % 3 == 0:
            liste += el
        elif el % 5 == 0:
            liste += el
    print(liste)


########################
#### Main Program : ####
########################


# Useless context manager
with MyContextManager():
    print("inside", "\n\n")


# Usefull context manager
with Cd("/home/pampi/Documents") as d:
    print(d, "\n\n")


# Simple decorator without class
with tag("chocolat") as b:
    print("mine", b)
print("\n\n")


# Decorator and context manager  ----> context decorator
with TimeIt():
    bad(1000)
bad(1000)  # No timer outside the context manager
