#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""Draw matplotlib representation of main variables"""


########################################
#### Classes and Methods imported : ####
########################################


import pandas as pd
import numpy as np
import datetime
import matplotlib

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

from matplotlib.patches import Ellipse  # Used to draw shapes inside plots
from matplotlib.dates import MinuteLocator, DateFormatter, SecondLocator


#####################
#### Constants : ####
#####################


# Change font properties
font_base = {'family' : 'serif',
             'size'   : 13}
font_title = {'size'   : 18,
              'family':'Anonymous Pro'}
font_mainTitle = {'color': '#002b36',
                  'weight': 'bold',
                  'size': '25',
                  'family': 'Anonymous Pro'}

# Change default label settings
matplotlib.rc('font', **font_base)
matplotlib.rc('xtick', labelsize=10)
matplotlib.rc('ytick', labelsize=10)
matplotlib.rc('legend', fontsize=10)
matplotlib.rc('legend', labelspacing=0.2)

# font = matplotlib.font_manager.FontProperties(family='Tahoma', size=12)
# matplotlib.rc('annotate', fontproperties=font)

# Adding artist element
el = Ellipse((2, -1), 0.5, 0.5)

# Formatter
minutes = MinuteLocator(interval=4)
minutes_formatter = DateFormatter("%M:%S")

secondes = SecondLocator(interval=10)
secondes_formatter = DateFormatter("%M:%S")

#######################################
#### Classes, Methods, Functions : ####
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
        output : 'year-month-day hour:minute:second'
    """
    try:
        solis_date, hour = solis_date.split(" ")
        year, month, day = map(int, reversed(solis_date.split("/")))
        hour, minute = map(int, hour.split(":"))
        return datetime.datetime(year+1, month, day, hour, minute)
    # Bad csv with some text inside values --> return None to remove them with groupby later
    except ValueError:
        return None


def printer_all(S_frame, csv_list):
    """
        Print field for each frame
    """
    for ind, data in enumerate(S_frame):
        print("\nData from {} dataframe".format(csv_list[ind]))
        for i, col in enumerate(data.columns):
            print("column {} \t\t{}".format(i, col))


def printer_spe(frame):
    """
        Print fields for a specific frame
    """
    for i, col in enumerate(frame.columns):
        print("column {} \t\t{}".format(i, col))


def read_csv(csv_list, skiprows=(1,), delimiter=(";",), index_col=("Date",),
             convert_index=(None,), in_conv_index=(None,)):
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
    """
    S_frame = {}
    for csv, row, sep, ind, conv, in_conv in zip(csv_list, skiprows, delimiter,
                                                 index_col, convert_index,
                                                 in_conv_index):
        if in_conv:
            frame = pd.read_csv(csv, skiprows=row, delimiter=sep, index_col=ind,
                                converters={"Date": convert_solis_to_datetime})
        else:
            frame = pd.read_csv(csv, skiprows=row, delimiter=sep, index_col=ind)
            # Process to conversions
            if conv is not None:
                frame.index = [ind for ind in conv(frame.index)]

        # Reduce data structure and remove duplicated values
        frame.groupby(frame.index).last()
        # Add frame to dictionnary
        S_frame[csv.split("\\")[-1].split(".")[0]] = frame
    return S_frame







########################
#### Main Program : ####
########################

csv = "olivier_house_read.csv"
