#! /usr/bin/env python
# -*- coding:Utf8 -*-


try:
    from .parameters import *
except SystemError as e:
    print("Local import")
    from parameters import *

from collections import OrderedDict as OrdD
from numpy import arange, zeros_like


#######################################
#### Classes, Methods, Functions : ####
#######################################

class EvalData(object):

    """
        Prepare all dataframes.
            - cumul hist
            - diag
            - box
            - ...
    """
    # Length of each samples
    sample = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    # Number of row = per_sample * sample[i]
    per_sample = 48

    def __init__(self, frame, steps=None, length=12):
        self.frame = frame
        self.steps = steps or [el*self.per_sample for el in self.sample]
        self.length = length
        self.fields = None
        self.columns = {columns for columns in self.frame}

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
    def keep_arange(frame, range_=(9, 18)):
        """
            Keep only values between a specific range
            frame must be a dataframe
            Be careful range match hours
                ---> dataframe index must be a datetime or timestep friendly
                ---> ``range_[1]`` is the highter hours value not higther limit
                        columns with ``8h 30 min`` will be kept
        """
        frame = frame.loc[frame.index.hour <= range_[1]]
        frame = frame.loc[frame.index.hour >= range_[0]]
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

    @staticmethod
    def change_col_name(old, new, columns):
        """
            Change a specific column name. Return a list of columns.
            Use example : frame.columns = change_col_name("old", "new",
                                                          frame.columns)
        """
        columns = list, columns or EvalData.frame.columns
        print(columns)
        columns[columns.index(old)] = new
        return columns

    def hist_energy_actions(self, frame, fields=None, new_fields=()):
        """
            Proceed all treatments to extract structure to plot energy histogram
            new_fields index must be strutured as below:
                0 : new column name
                1 : first column
                2 : second column
                3 : operator between 1 and 2 (can be '+', '-', '*', '/')
                    ---> frame[0] = frame[1] 3 frame[2]
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
        if new_fields:
            # For each new columns
            for new in new_fields:
                # Create new columns
                frame[new[0]] = self.add_column(frame,
                                                used_cols=(new[1], new[2]),
                                                operator=new[3])
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
    font_base = {'family': 'serif',
                 'size': 13}
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

    def fig_init(self, figsize=(20, 10), facecolor=None, sharex=None,
                 ha='center'):
        # Default parameters
        sharex = sharex or self.sharex
        facecolor = facecolor or self.background_color
        # Drawing graphs according to number of dataframes
        self.fig, self.axes = plt.subplots(nrows=self.nb_rows,
                                           ncols=self.nb_cols,
                                           figsize=figsize,
                                           sharex=self.sharex,
                                           facecolor=facecolor)
        self.figure_title(ha=ha)

    def figure_title(self, ha='center', fontdict={}):
        self.fig.canvas.manager.set_window_title(self.title)
        plt.figtext(0.5, 0.95, self.title, ha=ha,
                    fontdict=fontdict or self.font_mainTitle)

    def adjust_plots(self, top=None,  bottom=None,  left=None,  right=None,
                     hspace=None, wspace=None):
        """
            Force figure padding.
            None lead to default rc parameters
        """
        self.fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right,
                                 hspace=hspace, wspace=wspace)

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

    def catch_axes(self, nb_row, nb_col):
        """
            Return always right subscription of self.axes
        """
        if hasattr(self.axes, '__getitem__'):
            if self.nb_cols <= 1 or self.nb_rows <= 1:
                return self.axes[nb_row]
            else:
                return self.axes[nb_row][nb_col]
        else:
            return self.axes

    def auto_format(self):
        self.fig.autofmt_xdate()

    def set_xtiks_labels(self, pos, names, rotation=30):
            self.catch_axes(*pos).set_xticklabels(names, rotation=rotation)

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
                        whis=1000, pos=(0, 0), title='Box me !', **kwargs):
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
        self.catch_axes(*pos).set_title(label=title,
                                        fontdict=self.font_title,
                                        loc=loc)
        for ind, col in enumerate(columns):
            # Get list of all values for each col
            vals = [el[col] for el in list_frame]
            xticks = self.optimize_xticks_pos(list_frame, start=ind)
            temp = self.catch_axes(*pos).boxplot(vals,
                                                 positions=xticks,
                                                 widths=widths,
                                                 whis=whis, **kwargs)
            self.set_boxes(temp, colors=colors or self.colors[ind])
        start = int(len(list_frame[0].columns)/2+0.5) - 1  # Get group center
        # Set legend and xticks positions
        self.format_boxticks(list_frame, pos, start)

    def diag_plot(self, frame, to_diag, title='Diag me',
                  loc='left', pos=(1, 0), explode=(0.1, 0, 0), radius=0.8,
                  colors=None, **kwargs):
        """
            Used to plot diagrams with a dataframe prepared with EvalData class.
            - to_diag is a list of columns names to plot
            - title used as column name and text value for title
            - loc used to place title
            - pos used to set specific axe (always a tuple even if only one axe)
            - explode used to add specific emphaze (must match to_diag length)
            - radius used to change diagram size
            - colors are colors of parts. If None self.colors used
        """
        # Print data informations
        columns = frame.columns
        # Plot all plots
        # Keep only needed values (return a new dataframe)
        temp = pd.concat([frame[frame.index == el] for el in to_diag])
        print('\n---' + 'Plotting diagram' + '---' + '\n', temp)
        text = "{1} : {0:.2%}".format(frame.get_value(title, columns[0]),
                                      title)
        self.catch_axes(*pos).set_title(label=text,
                                        fontdict=self.font_title,
                                        loc=loc)
        self.catch_axes(*pos).pie(temp, colors=colors or self.colors,
                                  labels=to_diag, shadow=True,
                                  autopct='%1.1f%%', startangle=90,
                                  explode=explode, radius=radius, **kwargs)
        # Set axe parameters
        self.catch_axes(*pos).legend(prop=self.font_title)

    def bar_sup_plot(self, frame, fields, colors={}, loc='left', pos=(1, 1), names=[],
                     title='Hist me', l_width=3, h_width=0.9, ylabel="Kwh",
                     emphs=None, **kwargs):
        # Print data informations
        columns = frame[fields+emphs].columns
        # Get names
        names = names or self.names
        print('\n---' + 'Plotting Histogram' + '---' + '\n', columns)
        # Plot all plots
        self.catch_axes(*pos).set_title(label=title,
                                        fontdict=self.font_title,
                                        loc=loc)
        # Draw all bar and stock them inside an Ordered dict
        temp = OrdD()
        for col in columns:
            temp[col] = self.catch_axes(*pos).bar(frame.index.values,
                                                  frame[col].values,
                                                  color=self.colors[col],
                                                  width=h_width,
                                                  **kwargs)
        # Draw top line of ``emph`` bar
        if emphs:
            for emph in emphs:
                self.catch_axes(*pos).bar(left=frame.index.values,
                                          height=[1]*12,
                                          bottom=frame[emph].values,
                                          ec=self.colors[emph], fill=False,
                                          width=h_width, linewidth=3,
                                          **kwargs)
        # Set axe parameters
        self.catch_axes(*pos).set_ylabel(ylabel=ylabel, labelpad=20)
        self.catch_axes(*pos).set_xlim(h_width, len(names)+1)
        self.catch_axes(*pos).set_xticks(arange(1.5-(1-h_width)/2,
                                                len(names)+1.5-(1-h_width)/2,
                                                1))
        # Add xticks labels
        self.set_xtiks_labels(pos, names)
        # Add auto legend
        self.catch_axes(*pos).legend([temp[col] for col in columns],
                                     list(columns),
                                     loc="best", prop=self.font_title)

    def bar_cum_plot(self, frame, fields, pos=(1, 1), colors={}, loc='left',
                     names=[],  title='Hist me', h_width=0.9, ylabel="Kwh",
                     emphs=None, **kwargs):
        """
            Plot a cumulated bar plot of each fields inside the frame and
            for each row.
                - frame is a dataframe
                - fields is a list of dataframe columns names to plot
                - pos to get specific axe
                - colors is a dict of color (must have one color per field)
                - loc used to place title's text
                - names is a list of new xticks labels (empty list for defaults)
                - title is text to write as axe title
                - h_width is the bar width
                - emphs list of column name  used to draw a bar top line,
                  each emph of emphs must be a frame column name
                - **kwargs will be passed to axe.bar()
        """
        # Print data informations
        columns = frame[fields+emphs].columns
        # Get names
        names = names or self.names
        # Get fields
        fields = fields or columns
        print('\n---' + 'Plotting Histogram' + '---' + '\n', columns)
        self.catch_axes(*pos).set_title(label=title,
                                        fontdict=self.font_title,
                                        loc=loc)
        # Draw all bar and stock them inside an Ordered dict
        temp = OrdD()
        # Bottom for bars
        bottom = pd.DataFrame(zeros_like(frame[[columns[0]]]),
                              columns=["Bottom"], index=frame.index)
        for col in fields:
            temp[col] = self.catch_axes(*pos).bar(left=frame.index.values,
                                                  height=frame[col],
                                                  bottom=bottom["Bottom"],
                                                  width=h_width,
                                                  color=self.colors[col],
                                                  **kwargs)
            bottom += frame[[col]].values
        # Draw top line of ``emph`` bar
        if emphs:
            for emph in emphs:
                temp[emph] = self.catch_axes(*pos).bar(left=frame.index.values,
                                                       height=[0]*12,
                                                       bottom=frame[emph],
                                                       ec=self.colors[emph],
                                                       fill=False,
                                                       width=h_width,
                                                       linewidth=4,
                                                       **kwargs)
        # Set axe parameters
        self.catch_axes(*pos).set_ylabel(ylabel=ylabel, labelpad=20)
        self.catch_axes(*pos).set_xlim(h_width, len(names)+1)
        self.catch_axes(*pos).set_xticks(arange(1.5-(1-h_width)/2,
                                                len(names)+1.5-(1-h_width)/2,
                                                1))
        # Add xticks labels
        self.set_xtiks_labels(pos, names)
        # # Add auto legend
        self.catch_axes(*pos).legend([temp[col] for col in columns],
                                     list(columns),
                                     loc="best", prop=self.font_base)

    def format_boxticks(self, list_frame, pos=(0, 0), start=0, names=[],
                        **kwargs):
        """
            Place and format xticks. Add boxes legends.
                - list_frame is a list of dataframes
                - pos to get specific axe
                - start is the first tick of xticks values
                - names is a list of new xticks labels (empty list for defaults)
                - **kwargs will be passed to axe.legend()
        """
        cols = list_frame[0].columns  # Get columns names
        names = names or self.names  # Get x ticks labels
        self.catch_axes(*pos).set_xticks(self.optimize_xticks_pos(list_frame,
                                                                  start=start))
        self.catch_axes(*pos).set_xlim(-1, len(list_frame)*(len(cols)+self.pad))
        self.set_xtiks_labels(pos, names)

        # Add legend by drawing curves and hiding them just after
        curves = []  # Container for Line2D
        for col in self.colors:
            # Unpack and keep only Line2D instances
            h, = self.catch_axes(*pos).plot([1, 1], col[0],
                                            linewidth=self.width)
            curves.append(h)  # Add Line2D object inside a list
        self.catch_axes(*pos).legend(curves, list(cols),
                                     prop=self.font_title, **kwargs)
        for plot in curves:
            plot.set_visible(False)

    def change_xticks_labels(self, labels, pos=(1, 1), fontdict=None,
                             minor=False, **kwargs):
        """
            Method used to change xticks labels.
                - labels must be a list:
                    - list of list : each list will be zip and each elements of
                      list of lits will be concatenate
                    - list of elements : each elements will be concatenate
                    - example : ["b", "i"]  ---> ["b", "i"]
                                [["b", "i"], ["b", i"]]  ---> ["bi", "bi"]
                - pos to get specific axe
                - fontdict to use specific text format (None to keep default)
                - minor : False ---> major ticks, True ---> minor ticks
                - **kwargs will be passed to axe.set_xticklabels()
        """
        try:
            iter(labels[0])
        except TypeError:
            new_labs = ["".join(str(i) for i in el) for el in zip(labels)]
        else:
            new_labs = ["".join(str(i) for i in el) for el in zip(*labels)]
        self.catch_axes(*pos).set_xticklabels(labels=new_labs,
                                              fontdict=fontdict,
                                              minor=minor, **kwargs)

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

    # def add_line_to_top(self, frame, colors={}, loc='left', pos=(1, 1), names=[],
                   # title='Hist me', l_width=3, h_width=0.9, ylabel="Kwh"):
        """
            Just to remenber how to access top of barplots
        """
        # # Draw all bar and stock them inside an  Ordered dict
        # temp = OrdD()
        # for col in frame.columns:
        #     temp[col] = self.catch_axes(*pos).bar(frame.index.values,
        #                                           frame[col].values,
        #                                           color=self.colors[col],
        #                                           width=h_width)
        # Draw a line at the top of each "Boiler_Energy" barplots
        # tops = ([(el.get_x(), el.get_x()+temp[emph][0].get_width()),
        #          (el.get_height(),)*2] for el in temp[emph])
        # # Add lines to see emphase on all samples
        # for top in tops:
        #     l = matplotlib.lines.Line2D(*top,
        #                                 linewidth=l_width,
        #                                 color=self.colors[emph])
        #     self.catch_axes(*pos).add_line(l)

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
    # New fields
    new_fields = (("Besoins", "DrawingUp_Energy", "Radiator_Energy", "+"),
                  ("Consommations", "Collector_Energy", "Boiler_Energy", "+"),
                  ("Pertes", "Consommations", "Besoins", "-"),
                  ("Taux", "Collector_Energy", "Consommations", "/"))

    ##################  TESTING  EvalData class##################
    chamb = EvalData(frames["chambery"])
    names = tuple(key for key in frames)

    # HISTOGRAM
    chamb.hist = chamb.hist_energy_actions(chamb.frame, new_fields=new_fields,
                                           fields=["Collector_Energy", "Boiler_Energy",
                                                   "Radiator_Energy", "DrawingUp_Energy"])

    # DIAGRAM
    chamb.diag = chamb.diag_energy_actions(chamb.frame,
                                           fields=["Collector_Energy", "Boiler_Energy",
                                                   "Radiator_Energy", "DrawingUp_Energy"],
                                           new_fields=new_fields)

    # BOXPLOT
    chamb.box_T = chamb.box_actions(chamb.frame, fields=['T3', 'T4', 'T5'])
    chamb.box_H = chamb.box_actions(chamb.frame, fields=['HDifTil_collector',
                                                         'HDirTil_collector'])

    ##################  TESTING  MultiPlotter class##################
    # Prepare boxplots as first added data to plot class
    frames_ = {'Temps': chamb.box_T, 'Irradiations': chamb.box_H}
    # Color tuple for each box parameter
    colors = (('#268bd2', '#002b36', '#268bd2', '#268bd2', '#dc322f'),
              ('#586e75', '#002b36', '#586e75', '#586e75', '#dc322f'),
              ('#859900', '#002b36', '#859900', '#859900', '#dc322f'))
    title = "Bilan de la simulation de {}".format(names[0])

    # Create plot class
    Plot = MultiPlotter(frames_, nb_cols=2, nb_rows=2, colors=colors,
                        title=title)
    Plot.fig_init()
    Plot.figure_title()
    title = "Evolution mensuel de la variation des températures des ballons"
    Plot.boxes_mult_plot(Plot.frames['Temps'], pos=(0, 0),
                         title=title)
    title = "Evolution mensuel de la variation de la puissance captable"
    Plot.boxes_mult_plot(Plot.frames['Irradiations'], pos=(1, 0),
                         title=title)

    # Add diagram
    Plot.frames['Diagplot'] = chamb.diag  # Keep only dataframe
    Plot.colors = ["#fdf6e3", "#268bd2", '#cb4b16']
    Plot.diag_plot(Plot.frames['Diagplot'], pos=(0, 1), loc='center',
                   to_diag=['Radiator_Energy', 'DrawingUp_Energy', 'Pertes'],
                   title='Taux')

    # Add bar plot
    Plot.frames['Barplot'] = chamb.hist[0]  # Keep only dataframe
    # Change colors tuple to color dict
    Plot.colors = {"Boiler_Energy": "#dc322f", "Radiator_Energy": "#fdf6e3",
                   "DrawingUp_Energy": "#268bd2", "Collector_Energy": "orange",
                   "Pertes": "#cb4b16"}
    title = "Evolution mensuel des apports et consommations d'énergie (en KWh)"
    Plot.bar_cum_plot(Plot.frames['Barplot'], emphs=['Collector_Energy'],
                      pos=(1, 1), title=title,
                      fields=["DrawingUp_Energy",
                              "Radiator_Energy",
                              "Pertes"])
    # Prepare Taux (list of formatted data)
    short_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sept', 'Oct',
                   'Nov', 'Dec']
    percents = ['{:.1%}'.format(i) for i in Plot.frames['Barplot']['Taux'].values]
    Plot.change_xticks_labels([short_names, [' : ']*12,
                               percents])

    # Adjust plot format
    Plot.adjust_plots(hspace=0.3, top=0.85, left=0.05)
    Plot.show()

    print(Plot.frames['Diagplot'].columns)
    Plot.frames['Diagplot'].columns = EvalData.change_col_name('Pertes',
                                                               'gain',
                                                               Plot.frames['Diagplot'].columns)
    print(Plot.frames['Diagplot'].columns)
