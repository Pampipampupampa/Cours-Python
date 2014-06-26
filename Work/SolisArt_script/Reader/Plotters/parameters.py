#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""Reader for csv files from Dymola or solisArt"""


########################################
#### Classes and Methods imported : ####
########################################


import pandas as pd
import datetime
import matplotlib

import matplotlib.pyplot as plt

from matplotlib.patches import Ellipse  # Used to draw shapes inside plots
from matplotlib.dates import MinuteLocator, DateFormatter, SecondLocator


#####################
#### Constants : ####
#####################

FOLDER = "D:\\GitHub\\SolarSystem\\Outputs\\"

# Create font properties
font_base = {'family': 'serif',
             'size': 13}
font_title = {'size': 18,
              'family': 'Anonymous Pro'}
font_mainTitle = {'color': '#002b36',
                  'weight': 'bold',
                  'size': '25',
                  'family': 'Anonymous Pro'}

# Change matplotlib default settings
matplotlib.rcParams['backend.qt4'] = "PySide"
matplotlib.rc('font', **font_base)
matplotlib.rc('xtick', labelsize=10)
matplotlib.rc('ytick', labelsize=10)
matplotlib.rc('legend', fontsize=10)
matplotlib.rc('legend', labelspacing=0.2)

# Artist shape used by annotations
el = Ellipse((2, -1), 0.5, 0.5)

# Formatter to change x values ticks
minutes = MinuteLocator(interval=4)
minutes_formatter = DateFormatter("%M:%S")

secondes = SecondLocator(interval=10)
secondes_formatter = DateFormatter("%M:%S")


#######################################
#### Classes, Methods, Functions : ####
#######################################


class Plotter:

    """
        Base class for plotting on matplotlib
            - fig_init used to create figure
            - plotting_shape used to group axes and figure structure
            - plotting used to group all data plots
            - artist used to group annotations and other artist stuff
    """

    width = 2  # Line width
    colormap = "Accent"  # Color set
    background_color = (1, 0.98, 0.98)  # background_color old=(0.84, 0.89, 0.9)

    def __init__(self, frame, title="Title"):
        self.frame = frame
        self.title = title

    def fig_init(self, figsize=(20, 10), facecolor=background_color,
                 ha='center'):
        """
            Create figure instance and add title to it
        """
        self.fig = plt.figure(figsize=figsize, facecolor=facecolor)
        self.fig.canvas.manager.set_window_title(self.title)
        plt.figtext(0.5, 0.95, self.title, ha=ha, fontdict=font_mainTitle)

    def plotting_shape(self):
        """
            Main plotting structure
        """
        pass

    def plotting(self):
        """
            Adding plots to plotting structure
        """
        pass

    def formatting(self):
        """
            Adding formatters
        """

    def artist(self):
        """
            Adding annotations or text to plots
        """
        pass

    def text(self):
        """
            Adding text inside figure
        """
        pass

    def forcing(self):
        """
            Adding some element to overwrite self.fig.autofmt_xdate()
        """
        pass

    def draw(self):
        """
            Proceed to all Methods
        """
        self.fig_init()
        self.plotting_shape()
        self.plotting()
        self.formatting()
        self.artist()
        self.text()
        self.fig.autofmt_xdate()
        self.forcing()
        plt.show()


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
