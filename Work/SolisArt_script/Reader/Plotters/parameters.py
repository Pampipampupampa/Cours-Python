#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""Parameters and constants for all plotters class"""


########################################
#    Classes and Methods imported :    #
########################################


import datetime
import matplotlib

import pandas as pd
# Used by all script which import this module
import matplotlib.pyplot as plt

from matplotlib.patches import Ellipse  # Used to draw shapes inside plots
from matplotlib.dates import MinuteLocator, DateFormatter, SecondLocator

from path import path  # Nice object oriented path API
from os import name  # Get os name
from math import ceil

from itertools import chain, islice
from collections import deque

######################
#    Parameters :    #
######################


# Specific folder in linux or windows
if name == 'nt':
    FOLDER = path("D:/GitHub/solarsystem/Outputs")
elif name == 'posix':
    FOLDER = path('~').expanduser() / "Documents/Git/solarsystem/Outputs"

# Create font properties
# Can be use to plot for publication
# font_base = {'size': 30,
#              'family': 'STIXGeneral'}
# #             'mathtext.fontset': 'stix'
# #             'text.usetex': True}  # Used to force latex inside figures
# Favorite
font_base = {'size': 18,
             'family': 'Source Code Pro'}

# # Restore default
# matplotlib.rcParams.update({'font.size': 12,
#                             'font.family': 'sans',
#                             'text.usetex': False})

# Change matplotlib default settings
matplotlib.rcParams['backend.qt4'] = "PySide"
matplotlib.rc('font', **font_base)
matplotlib.rc('xtick', labelsize=12)
# matplotlib.rc('xtick', labelsize=30)
matplotlib.rc('ytick', labelsize=16)
# matplotlib.rc('ytick', labelsize=30)
# matplotlib.rc('legend', fontsize=12)
# matplotlib.rc('legend', labelspacing=0.2)

# Artist shape used by annotations
el = Ellipse((2, -1), 0.5, 0.5)

# Formatter to change x values ticks
minutes = MinuteLocator(interval=4)
minutes_formatter = DateFormatter("%M:%S")

secondes = SecondLocator(interval=10)
secondes_formatter = DateFormatter("%M:%S")

#######################################
#    Classes, Methods, Functions :    #
#######################################


def convert_to_datetime(step, start=datetime.datetime(2014, 1, 1)):
    """
      This parser convert to a real datetime format
    """
    for el in step:
        yield start + datetime.timedelta(seconds=int(el))


def convert_solis_to_datetime(solis_date):
    """
        This parseur convert SolisArt software format to a real datetime format
        input : 'day/month/year hour:minute'
        output : datetime(year-month-day hour:minute:second)
    """
    try:
        solis_date, hour = solis_date.split(" ")
        year, month, day = map(int, reversed(solis_date.split("/")))
        hour, minute = map(int, hour.split(":"))
        return datetime.datetime(year+1, month, day, hour, minute)
    # Bad csv with some text inside values --> return None to remove them with groupby later
    except ValueError:
        return None


def step_iterator(dataframe, start=0, steps=[], interval=None):
    """
        Create an iterator to treat a dataframe by parts

        example :
            start=0 (start at beginning)
            steps=[el*48 for el in (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)]
                ---> Length of months
                With 48 as number of steps (inside dataframe) between iterations
                ---> A dataframe step size of 30min ---> 48 steps per day
            interval=12 (12 month inside one year)
        --> Month dataframe iterator
    """
    end = start + steps[0]
    yield dataframe[start:end]
    for el in range(interval-1):
        start = end
        end += steps[el+1]
        yield dataframe[start:end]


def chunks(seq, chunksize, process=tuple):
    """
        Yields items from an iterator in iterable chunks.
    """
    it = iter(seq)
    while True:
        yield process(chain([next(it)], islice(it, chunksize - 1)))


def window(iterable, size=2):
    """
        Yields iterms by bunch of a given size, but rolling only one item
        in and out at a time when iterating.
    """
    iterable = iter(iterable)
    d = deque(islice(iterable, size), size)
    yield d
    for x in iterable:
        d.append(x)
        yield d


def printer_all(S_frame, csv_list):
    """
        Print field for each dataframe inside a list
    """
    for ind, data in enumerate(S_frame):
        print("\nData from {} dataframe".format(csv_list[ind]))
        for i, col in enumerate(data.columns):
            print("column {} \t\t{}".format(i, col))


def printer_spe(frame):
    """
        Print fields for each dataframe inside a dictionnary
    """
    for key, val in frame.items():
        print("\n----> " + key)
        for i, col in enumerate(val.columns):
            print("column {} \t\t{}".format(i, col))


def to_table(nb_vals):
    """
        Return an optimize number of row and columns
    """
    assert nb_vals != 0, "nb_vals must be greater than 0"
    n_row = None
    for nb_col in range(1, nb_vals+1):
        n_row = ceil(nb_vals / nb_col)
        if 0 <= n_row - nb_col <= 1:
            return n_row, nb_col


def read_csv(csv_list, skiprows=(1,), delimiter=(";",), index_col=("Date",),
             convert_index=(None,), in_conv_index=(None,), splitters=(".",)):
    """
        Read all csv files and clean/format datas
            - csv_list is a list which contains path of csv_files
            - skiprows allows to start read the in_file after <x> rows
            - delimiter is a tuple or list of in and out file columns separators
            - index_col is the column name to convert into index column
            - convert_index is an index converter:
                - None to do nothing
                - convert_to_datetime ---> datetime real format
            - in_conv_index is an inplace converter to convert when loading file
                - None to do nothing
                - convert_solis_to_datetime ---> SolisArt datetime to real datetime
            - splitters used to datas keys names to something more readable
                Keep only left side of split according to splitter value
                ---> (".",) get only file name without extension
    """
    S_frame = {}
    for csv, row, sep, ind, conv, in_conv, splitter in zip(csv_list,
                                                           skiprows,
                                                           delimiter,
                                                           index_col,
                                                           convert_index,
                                                           in_conv_index,
                                                           splitters):
        if in_conv:
            frame = pd.read_csv(csv, skiprows=row, delimiter=sep, index_col=ind,
                                converters={"Date": convert_solis_to_datetime})
        else:
            frame = pd.read_csv(csv, skiprows=row, delimiter=sep, index_col=ind)
            # Process to conversions
            if conv is not None:
                frame.index = [ind for ind in conv(frame.index)]
        # Reduce data structure and remove duplicated values
        frame = frame.groupby(frame.index).last()
        # Add frame to dictionnary
        S_frame[path(csv).name.split(splitter)[0]] = frame
    return S_frame
