#! /usr/bin/env python
# -*- coding:Utf8 -*-

"""
    Base class used to create advanced plotters.
    All fonts properties can be found inside parameters.py
"""


try:
    from .parameters import *
except SystemError as e:
    print("Local import")
    from parameters import *


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
    font_title = {'size': 18,
                  'family': 'Anonymous Pro'}
    font_mainTitle = {'color': '#002b36',
                      'weight': 'bold',
                      'size': '25',
                      'family': 'Anonymous Pro'}
    width = 2  # Line width
    colormap = "Accent"  # Color set
    background_color = (1, 0.98, 0.98)  # background_color old=(0.84, 0.89, 0.9)

    def __init__(self, frames, title='Title',
                 steps=[365], length=12):
        self.frames = frames
        self.title = title
        self.steps = steps
        self.length = length

    def fig_init(self, figsize=(20, 10), facecolor=background_color,
                 ha='center'):
        """
            Create figure instance and add title to it
        """
        self.fig = plt.figure(figsize=figsize, facecolor=facecolor)
        self.fig.canvas.manager.set_window_title(self.title)
        plt.figtext(0.5, 0.95, self.title, ha=ha,
                    fontdict=self.font_mainTitle)

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

    def prepare(self):
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

    def show(self):
        """
            Show plot
        """
        plt.show()

    def draw(self):
        """
            Proceed to all Methods and show plot
        """
        self.prepare()
        self.show()


class CombiPlotter(Plotter):

    """
        Base class for combined plots
            - frames must be a list of dataframes
            - title the figure title
            - blocs a list of each columns names which will be extracted from
              from each dataframes
            - steps used to sample data step by step
                'month' lead to : self.steps = [el*48 for el in self.sample]
            - length used to limit iteration
            - sharex set to True to share xaxis with all plots
    """

    sample = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    def __init__(self, frames, title='Title',
                 steps='months', length=12, sharex=True):
        super().__init__(frames=frames, title=title)
        self.frames = frames
        self.title = title
        if steps == 'months':
            self.steps = [el*48 for el in self.sample]
        else:
            self.steps = steps
        self.length = length
        self.sharex = sharex

    def fig_init(self, figsize=(20, 10), facecolor='class_color',
                 ha='center'):
        if facecolor == 'class_color':
            facecolor = self.background_color
        # Drawing graphs according to number of dataframes
        if len(self.frames) >= 4:
            # int(len(self.frames)/2+0.5) is a trick to have
            # 3 rows for 5 and 6 and 2 rows for 4
            self.fig, self.axes = plt.subplots(nrows=int(len(self.frames)/2+0.5),
                                               ncols=2,
                                               figsize=figsize,
                                               sharex=self.sharex,
                                               facecolor=facecolor)
        else:
            self.fig, self.axes = plt.subplots(nrows=len(self.frames), ncols=1,
                                               figsize=figsize,
                                               sharex=self.sharex,
                                               facecolor=facecolor)
        self.fig.canvas.manager.set_window_title(self.title)
        plt.figtext(0.5, 0.95, self.title, ha=ha, fontdict=self.font_mainTitle)

    def forcing(self):
        self.fig.subplots_adjust(top=0.85, bottom=0.05, left=0.05, right=0.95)

    def reduce_data(self, dataframe, fields, format=list,
                    steps=None, interval=None):
        """
            Return chunks of a dataframe
                - dataframe must be a pandas dataframe like
                - fields must match dataframe columns names
                - format is the output format
                - steps used to size chunks
                    None ---> steps = [el*48 for el in self.sample]
                - interval used to limit iteration

        """
        if steps is None:
            steps = self.steps
        if interval is None:
            interval = self.length
        return format(el for el in step_iterator(dataframe[fields],
                                                 steps=steps,
                                                 interval=interval))


########################
#### Main Program : ####
########################


if __name__ == '__main__':
    pass
