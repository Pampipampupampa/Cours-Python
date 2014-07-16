#! /usr/bin/env python
# -*- coding:Utf8 -*-


try:
    from .parameters import *
except SystemError as e:
    print("Local import")
    from parameters import *

from collections import OrderedDict as OrdD
from numpy import arange


#######################################
#### Classes, Methods, Functions : ####
#######################################

class EvalData(object):

    """
        Prepare all dataframes
    """

    sample = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    per_sample = 48

    def __init__(self, frame, steps=None, length=12):
        self.frame = frame
        self.steps = steps or [el*self.per_sample for el in self.sample]
        self.length = length
        self.fields = None

    def reduce_data(self, frame, fields, format=list,
                    steps=None, interval=None):
        """
            Return chunks of a dataframe
                - dataframe must be a pandas dataframe like
                - fields must match dataframe columns names
                - format is the output format
                - steps used to size chunks
                    None ---> steps = [el*self.per_sample for el in self.sample]
                - interval used to limit iteration
                    None ---> interval = 12

        """
        # Get new or initial values
        steps = steps or self.steps
        interval = interval or self.length
        return format(el for el in step_iterator(frame[fields],
                                                 steps=steps,
                                                 interval=interval))

    @staticmethod
    def keep_arange(frame, _range=(9, 18)):
        """
            Keep only values between a specific range
            frame must be a dataframe
            Be careful range match hours
                ---> dataframe index must be a datetime or timestep friendly
                ---> ``_range[1]`` is the highter hours value not higther limit
                        columns with ``8h 30 min`` will be kept
        """
        frame = frame.loc[frame.index.hour <= _range[1]]
        frame = frame.loc[frame.index.hour >= _range[0]]
        return frame

    @staticmethod
    def resample(frame, sample='30min', interpolate=True):
        if interpolate is True:
            return frame.resample(sample).interpolate()
        else:
            return frame.resample(sample)

    def add_column(self, frame, used_cols, operator='+'):
        """
            Return a new dataframe column with current columns
        """
        operations = {'+': frame[used_cols[0]] + frame[used_cols[1]],
                      '-': frame[used_cols[0]] - frame[used_cols[1]],
                      '/': frame[used_cols[0]] / frame[used_cols[1]],
                      '*': frame[used_cols[0]] * frame[used_cols[1]]}
        return operations[operator]

    def hist_energy_actions(self, frame, fields=None):
        """
            Proceed all treatments to extract structure to plot energy histogram
        """
        fields = fields or self.fields
        # Reduce dataframe
        frame = self.resample(frame)
        # Get chunks
        frame = self.reduce_data(frame, fields)
        # Get only last values for each chunks
        frame = [frame[i][-1:] for i in range(len(frame))]
        # Set each values difference to keep only energy evolution per sample
        frame = (frame[0],) + tuple(frame[ind+1] - frame[ind].values for ind in range(len(frame)-1))
        # Group all data together
        frame = pd.concat([el for el in frame])
        # Create indices
        indices = ["{:%B}".format(frame.index[i]) for i in range(self.length)]
        # Numerical index for each histogram
        frame.index = [el for el in range(1, self.length+1)]
        return frame, indices

    def diag_energy_actions(self, frame, fields=None, month=12,
                            new_fields=()):
        """
            Proceed all treatments to extract structure to plot energy diagram
            new_fields index must be strutured as below:
                0 : new column name
                1 : first column
                2 : second column
                3 : operator between 1 and 2 (can be '+', '-', '*', '/')
                    ---> frame[0] = frame[1] 3 frame[2]
        """
        # Default value for fields
        fields = fields or self.fields
        # Keep only last time step of ``month`` for all fields
        frame = frame[frame.index.month == month][-1:][fields]
        if new_fields:
            # For each new columns
            for new in new_fields:
                # Create new columns
                frame[new[0]] = self.add_column(frame,
                                                used_cols=(new[1], new[2]),
                                                operator=new[3])
        # Inverse columns and index
        frame = frame.T
        return frame

    def box_actions(self, frame, fields=None, diurnal=True):
        """
            Proceed all actions to prepare data for box plotting
        """
        fields = fields or self.fields
        # Reduce dataframe
        frame = self.resample(frame)
        # Get chunks
        frame = self.reduce_data(frame, fields)
        # Keep only diurnal values
        if diurnal:
            for ind in range(len(frame)):
                frame[ind] = self.keep_arange(frame[ind])
        return frame


class MultiPlotter(object):

    """
        Base class for combined plots
            - frames must be a dict of dataframes or of list of dataframes
            - colors is a tuple of fiths' length tuples
            - title the figure title
            - sharex set to True to share xaxis with all plots
    """
    # Text formatters
    font_title = {'size': 18,
                  'family': 'Anonymous Pro'}
    font_mainTitle = {'color': '#002b36',
                      'weight': 'bold',
                      'size': '25',
                      'family': 'Anonymous Pro'}
    width = 2  # Line width
    colormap = "Accent"  # Color set
    background_color = (1, 0.98, 0.98)  # background_color old=(0.84, 0.89, 0.9)

    sample = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    names = ['January', 'February', 'March', 'April', 'May',
             'June', 'July', 'August', 'September', 'October',
             'November', 'December']

    def __init__(self, frames, colors, title='Title', nb_rows=2, nb_cols=2,
                 sharex=False):
        self.title = title
        self.frames = frames
        self.colors = colors
        self.title = title
        self.nb_rows = nb_rows
        self.nb_cols = nb_cols
        self.sharex = sharex
        # Get all dataframes names
        self.data_names = self.fig_names()
        # Space between boxplot groups
        self.pad = 1
        # Hist main value
        self.emph = "Boiler_Energy"

    def fig_init(self, figsize=(20, 10), facecolor=None,
                 ha='center'):
        # Default background color
        facecolor = facecolor or self.background_color
        # Drawing graphs according to number of dataframes
        self.fig, self.axes = plt.subplots(nrows=self.nb_rows,
                                           ncols=self.nb_cols,
                                           figsize=figsize,
                                           sharex=self.sharex,
                                           facecolor=facecolor)
        # Check is self.axes is subscriptable
        if not hasattr(self.axes, "__getitem__"):
            # Set self.axes subscriptable
            self.axes = (self.axes,)
        self.figure_title(ha=ha)

    def figure_title(self, ha='center', fonct_dict={}):
        self.fig.canvas.manager.set_window_title(self.title)
        plt.figtext(0.5, 0.95, self.title, ha=ha,
                    fontdict=fonct_dict or self.font_mainTitle)

    def adjust_plots(self, top=0.9,  bottom=0.05,  left=0.05,  right=0.95):
        """
            Force figure padding
        """
        self.fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right)

    def show(self):
        """
            Show plot
        """
        plt.show()

    def fig_names(self):
        return [el for el in self.frames]

    def optimize_xticks_pos(self, list_frame, start):
        """
            Only used by boxplots (used to center each xticks)
            len(frame) gives number of ticks
            len(frame.columns) gives number of plot per ticks
        """
        return [el for el in range(start,
                                   len(list_frame)*(len(list_frame[0].columns)+self.pad),
                                   len(list_frame[0].columns)+self.pad)]

    def specific_sharing(self, rel_pos, master=(0, 0)):
        """
            Allow sharing only a specific for a specific axe.
            Return new axis


            NOT WORKING YET


        """
        # print(self.axes)
        # temp = self.fig.add_subplot(self.nb_rows, self.nb_cols, rel_pos,
        #                             sharex=self.axes[master[0]][master[1]])
        # self.axes[0][1] = temp
        # print(self.axes)
        pass

    def auto_format(self):
        self.fig.autofmt_xdate()

    def set_xtiks_labels(self, pos, names, rotation=30):
        if self.nb_cols <= 1 or self.nb_rows <= 1:
            self.axes[pos[0]].set_xticklabels(names, rotation=rotation)
        else:
            self.axes[pos[0]][pos[1]].set_xticklabels(names, rotation=rotation)

    def set_boxes(self, box, linewidth=(1.5, 1, 1, 0.5, 1), marker=1,
                  colors=('#268bd2', '#002b36', '#268bd2',
                          '#268bd2', '#dc322f')):
            """
                Change boxplot color structure
                current display colors are :
                    - ('blue', 'black', 'blue', 'blue', 'red')
            """
            plt.setp(box['boxes'], color=colors[0], linewidth=linewidth[0])
            plt.setp(box['caps'], color=colors[1], linewidth=linewidth[1])
            plt.setp(box['whiskers'], color=colors[2], linewidth=linewidth[2])
            plt.setp(box['fliers'], color=colors[3], linewidth=linewidth[3],
                     marker=marker)
            plt.setp(box['medians'], color=colors[4], linewidth=linewidth[4])

    def boxes_mult_plot(self, list_frame, colors=(), loc='left', widths=0.6,
                        whis=1000, pos=(0, 0), title='Box me !'):
        """
            Draw a boxplot for each columns inside each dataframe of
            the list_frame. Each dataframe of the list set a group of boxes.
            Each groups have a space between them.
            - list_frame must be a list of dataframes
            - colors is a tuple of fiths' length tuples
            - loc used to set title position
            -
        """
        # Print data informations
        columns = list_frame[0].columns
        # Plot all plots
        print('\n---' + 'Plotting Boxplot' + '---' + '\n', columns)
        # Plot boxplots of dataframe
        if self.nb_cols <= 1 or self.nb_rows <= 1:
            self.axes[pos[0]].set_title(label=title,
                                        fontdict=self.font_title,
                                        loc=loc)
            for ind, col in enumerate(columns):
                # Get list of all values for each col
                vals = [el[col] for el in list_frame]
                xticks = self.optimize_xticks_pos(list_frame, start=ind)
                temp = self.axes[pos[0]].boxplot(vals,
                                                 positions=xticks,
                                                 widths=widths,
                                                 whis=whis)
                self.set_boxes(temp, colors=colors or self.colors[ind])
        else:
            self.axes[pos[0]][pos[1]].set_title(label=title,
                                                fontdict=self.font_title,
                                                loc=loc)
            for ind, col in enumerate(columns):
                # Get list of all values for each col
                vals = [el[col] for el in list_frame]
                xticks = self.optimize_xticks_pos(list_frame, start=ind)
                temp = self.axes[pos[0]][pos[1]].boxplot(vals,
                                                         positions=xticks,
                                                         widths=widths,
                                                         whis=whis)
                self.set_boxes(temp, colors=colors or self.colors[ind])
        start = int(len(list_frame[0].columns)/2+0.5) - 1  # Get group center
        # Set legend and xticks positions
        self.format_boxticks(list_frame, pos, start)

    def diag_plot(self, frame, to_diag=None, to_title='Taux de couverture',
                  loc='left', pos=(1, 0), explode=(0.1, 0, 0), radius=0.8,
                  colors=None):
        """
            Used only if more than 4 dataframe inside self.frames.
            Draw all bars
        """
        # Default value
        to_diag = to_diag or ['Radiator_Energy', 'DrawingUp_Energy', 'Pertes']
        # Print data informations
        columns = frame.columns
        print(columns)
        # Plot all plots
        print('\n---' + 'Plotting diagram' + '---' + '\n', frame)
        # Keep only needed values
        temp = pd.concat([frame[frame.index == el] for el in to_diag])
        text = "{1} : {0:.2%}".format(frame.get_value(to_title, columns[0]),
                                      to_title)
        if self.nb_cols <= 1 or self.nb_rows <= 1:
            self.axes[pos[0]].set_title(label=text,
                                        fontdict=self.font_title,
                                        loc=loc)
            self.axes[pos[0]].pie(temp, colors=colors or self.colors,
                                  labels=to_diag, shadow=True,
                                  autopct='%1.1f%%', startangle=90,
                                  explode=explode, radius=radius)
            # Set axe parameters
            self.axes[pos[0]].legend(prop=self.font_title)
        else:
            self.axes[pos[0]][pos[1]].set_title(label=text,
                                                fontdict=self.font_title,
                                                loc=loc)
            self.axes[pos[0]][pos[1]].pie(temp, colors=colors or self.colors,
                                          labels=to_diag, shadow=True,
                                          autopct='%1.1f%%', startangle=90,
                                          explode=explode, radius=radius)
            # Set axe parameters
            self.axes[pos[0]][pos[1]].legend(prop=self.font_title)

    def hist_cum_plot(self, frame, colors={}, loc='left', pos=(1, 1), names=[],
                      title='Hist me', l_width=3, h_width=0.9, ylabel="Kwh"):
        # Print data informations
        columns = frame.columns
        # Get names
        names = names or self.names
        print('\n---' + 'Plotting Histogram' + '---' + '\n', columns)
        if self.nb_cols <= 1 or self.nb_rows <= 1:
            # Plot all plots
            for ind, name in enumerate(self.data_names):
                # print('\n---' + name + '---' + '\n', self.frames[name])
                self.axes[pos[0]].set_title(label=title,
                                            fontdict=self.font_title,
                                            loc=loc)
                # Draw all bar and stock them inside an  Ordered dict
                temp = OrdD()
                for col in frame.columns:
                    temp[col] = self.axes[pos[0]].bar(frame.index.values,
                                                      frame[col].values,
                                                      color=self.colors[col],
                                                      width=h_width)
                # Draw a line at the top of each "Boiler_Energy" barplots
                tops = ([(el.get_x(), el.get_x()+temp[self.emph][0].get_width()),
                         (el.get_height(),)*2] for el in temp[self.emph])
                # Add lines to see emphase on all samples
                for top in tops:
                    l = matplotlib.lines.Line2D(*top,
                                                linewidth=l_width,
                                                color=self.colors[self.emph])
                    self.axes[pos[0]].add_line(l)
                # Set axe parameters
                self.axes[pos[0]].set_ylabel(ylabel=ylabel, labelpad=20)
                self.axes[pos[0]].set_xlim(h_width, len(names)+1)
                self.axes[pos[0]].set_xticks(arange(1.5-(1-h_width)/2,
                                                    len(names)+1.5-(1-h_width)/2,
                                                    1))
                # Add xticks labels
                self.set_xtiks_labels(pos, names)
            # Add auto legend
            self.axes[pos[0]].legend([temp[col] for col in columns], list(columns),
                                     loc="best", prop=self.font_title)
        else:
            # Plot all plots
            for ind, name in enumerate(self.data_names):
                # print('\n---' + name + '---' + '\n', self.frames[name])
                self.axes[pos[0]][pos[1]].set_title(label=title,
                                                    fontdict=self.font_title,
                                                    loc=loc)
                # Draw all bar and stock them inside an  Ordered dict
                temp = OrdD()
                for col in frame.columns:
                    temp[col] = self.axes[pos[0]][pos[1]].bar(frame.index.values,
                                                              frame[col].values,
                                                              color=self.colors[col],
                                                              width=h_width)
                # Draw a line at the top of each "Boiler_Energy" barplots
                tops = ([(el.get_x(), el.get_x()+temp[self.emph][0].get_width()),
                         (el.get_height(),)*2] for el in temp[self.emph])
                # Add lines to see emphase on all samples
                for top in tops:
                    l = matplotlib.lines.Line2D(*top,
                                                linewidth=l_width,
                                                color=self.colors[self.emph])
                    self.axes[pos[0]][pos[1]].add_line(l)
                # Set axe parameters
                self.axes[pos[0]][pos[1]].set_ylabel(ylabel=ylabel, labelpad=20)
                self.axes[pos[0]][pos[1]].set_xlim(h_width, len(names)+1)
                self.axes[pos[0]][pos[1]].set_xticks(arange(1.5-(1-h_width)/2,
                                                            len(names)+1.5-(1-h_width)/2,
                                                            1))
                # Add xticks labels
                self.set_xtiks_labels(pos, names)
            # Add auto legend
            self.axes[pos[0]][pos[1]].legend([temp[col] for col in columns], list(columns),
                                             loc="best", prop=self.font_title)

    def format_boxticks(self, list_frame, pos, start, names=[]):
        # Change xticks values to put xtickslabels between boxes
        # (same tick per boxes pair)
        cols = list_frame[0].columns
        names = names or self.names
        if self.nb_cols <= 1 or self.nb_rows <= 1:
            self.axes[pos[0]].set_xticks(self.optimize_xticks_pos(list_frame,
                                                                  start=start))
            self.axes[pos[0]].set_xlim(-1,
                                       len(list_frame)*(len(cols)+self.pad))
            # Add xticks labels
            self.set_xtiks_labels(pos, names)
            # Add legend by drawing curves and hiding them just after
            curves = []  # Container for Line2D
            for col in self.colors:
                # Unpack and keep only Line2D instances
                h, = self.axes[pos[0]].plot([1, 1], col[0],
                                            linewidth=self.width)
                curves.append(h)  # Add Line2D inside a list
            self.axes[pos[0]].legend(curves, list(cols),
                                     prop=self.font_title)
            for plot in curves:
                plot.set_visible(False)
        else:
            self.axes[pos[0]][pos[1]].set_xticks(self.optimize_xticks_pos(list_frame,
                                                                          start=start))
            self.axes[pos[0]][pos[1]].set_xlim(-1,
                                               len(list_frame)*(len(cols)+self.pad))
            # Add xticks labels
            self.set_xtiks_labels(pos, names)
            # Add legend by drawing curves and hiding them just after
            curves = []  # Container for Line2D
            for col in self.colors:
                # Unpack and keep only Line2D instances
                h, = self.axes[pos[0]][pos[1]].plot([1, 1], col[0],
                                                    linewidth=self.width)
                curves.append(h)  # Group all Line2D inside a list
            self.axes[pos[0]][pos[1]].legend(curves, list(cols),
                                             prop=self.font_title)
            for plot in curves:
                plot.set_visible(False)

    @property
    def clean_axes(self):
        """
            Delete useless axe
        """
        flat = [x for i in self.axes for x in i]
        if len(self.frames) < len(flat):
            row = len(self.axes) - 1
            col = len(self.axes[0]) - 1
            self.axes[row][col].set_visible(False)

########################
#### Main Program : ####
########################


if __name__ == '__main__':
    chambery = FOLDER / "clean/chambery_30062014.csv"
    # Read all csv and store values as a dict
    frames = read_csv((chambery, ),
                      convert_index=(convert_to_datetime,)*10,
                      delimiter=(";",)*10,
                      index_col=("Date",)*10,
                      in_conv_index=(None,)*10,
                      skiprows=(1,)*10,
                      splitters=("_",)*10)

    ##################  TESTING  EvalData class##################
    test = EvalData(frames["chambery"])

    # HISTOGRAM
    test.hist = test.hist_energy_actions(test.frame,
                                         fields=["Collector_Energy", "Boiler_Energy",
                                                 "Radiator_Energy", "DrawingUp_Energy"])
    # print(test.hist, type(test.hist))

    # DIAGRAM
    # New fields
    new_fields = (("Besoins", "DrawingUp_Energy", "Radiator_Energy", "+"),
                  ("Consommations", "Collector_Energy", "Boiler_Energy", "+"),
                  ("Pertes", "Consommations", "Besoins", "-"),
                  ("Taux de couverture", "Collector_Energy", "Consommations", "/"))
    test.diag = test.diag_energy_actions(test.frame,
                                         fields=["Collector_Energy", "Boiler_Energy",
                                                 "Radiator_Energy", "DrawingUp_Energy"],
                                         new_fields=new_fields)
    # print(test.diag)

    # BOXPLOT
    test.box_T = test.box_actions(test.frame, fields=['T3', 'T4', 'T5'])
    test.box_H = test.box_actions(test.frame, fields=['HDifTil_collector',
                                                      'HDirTil_collector'])
    # print(len(test.box_T))

    ##################  TESTING  MultiPlotter class##################
    # Add boxplots
    frames_ = {'Temps': test.box_T, 'Irradiations': test.box_H}
    colors = (('#268bd2', '#002b36', '#268bd2', '#268bd2', '#dc322f'),
              ('#586e75', '#002b36', '#586e75', '#586e75', '#dc322f'),
              ('#859900', '#002b36', '#859900', '#859900', '#dc322f'))
    title = "Bilan de la simulation de Chambery"
    Plot = MultiPlotter(frames_, nb_cols=2, nb_rows=2, colors=colors,
                        title=title)
    Plot.fig_init()
    Plot.figure_title()
    title = "Evolution mensuel de la variation des températures des ballons"
    Plot.boxes_mult_plot(Plot.frames['Temps'], pos=(0, 0),
                         title=title)
    title = "Evolution mensuel de la variation de la puissance captée"
    Plot.boxes_mult_plot(Plot.frames['Irradiations'], pos=(1, 0),
                         title=title)

    # Add diagram
    Plot.frames['Diagplot'] = test.diag  # Keep only dataframe
    Plot.colors = ["#dc322f", "#fdf6e3", "#268bd2", "orange", '#cb4b16']
    Plot.diag_plot(Plot.frames['Diagplot'], pos=(0, 1))

    # Add histogramme to frames dict
    Plot.frames['Histplot'] = test.hist[0]  # Keep only dataframe
    # Change colors tuple to color dict
    Plot.colors = {"Boiler_Energy": "#dc322f", "Radiator_Energy": "#fdf6e3",
                   "DrawingUp_Energy": "#268bd2", "Collector_Energy": "orange",
                   "Pertes": '#cb4b16'}
    title = "Evolution mensuel des apports et consommations d'énergie (en KWh)"
    Plot.hist_cum_plot(Plot.frames['Histplot'], pos=(1, 1),
                       title=title)

    # Plot.auto_format()
    Plot.adjust_plots()
    Plot.show()
