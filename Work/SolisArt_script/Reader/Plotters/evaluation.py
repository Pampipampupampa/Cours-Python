#! /usr/bin/env python
# -*- coding:Utf8 -*-


try:
    from .parameters import *
except SystemError as e:
    print("Local import")
    from parameters import *

from collections import OrderedDict as OrdD
from numpy import arange, zeros_like, average

from functools import wraps  # Keep trace of decorated functions arguments

#######################################
#### Classes, Methods, Functions : ####
#######################################


def benchmark(func):
    """
        Time function
    """
    import time

    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.process_time()
        res = func(*args, **kwargs)
        print("{} has spent {} sec to finish".format(func.__name__,
                                                     time.process_time()-t))
        return res
    return wrapper


class EvalData(object):

    """
        Prepare all dataframes.
            - cumul hist
            - diag
            - box
            - line
            - area
            - ...
        Some tools to abstact some actions and make them more friendly.
    """

    def __init__(self, frame):
        """
            Parameters informations below :
                - frame must be a dataframe like
            Default steps create an iterator which chunks a full year of data
            into a list of data per month (48 rows per day * nb_day_of_month)
            See _sample and _per_sample.
        """
        self.frame = frame
        # Length of each samples
        self._sample = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        # Number of row = per_sample * sample[i]
        self._per_sample = 48
        # Iterator
        self._steps = [el*self._per_sample for el in self._sample]
        self.length = 12
        self.fields = None
        self.columns = {columns for columns in self.frame}

    def change_steps(self, sample, per_sample):
        """
            Change to a specific sampling iterator.
        """
        self._sample = sample
        self._per_sample = per_sample
        self._steps = [el*self._per_sample for el in self._sample]

    def reduce_data(self, frame, fields, format=list,
                    steps=None, interval=None):
        """
            Return chunks of a dataframe
                - dataframe must be a pandas dataframe like
                - fields must match dataframe columns names
                - format is the output format
                - steps used to size chunks
                  None ---> steps = self._steps
                - interval used to limit iteration
                  None ---> interval = 12
        """
        # Get new or initial values
        steps = steps or self._steps
        interval = interval or self.length
        return format(el for el in step_iterator(frame[fields],
                                                 steps=steps,
                                                 interval=interval))

    @staticmethod
    def keep_hour_range(frame, range_=(9, 18)):
        """
            Keep only values between a specific range
            frame must be a dataframe.
            Be careful range match hours :
                ---> dataframe index must be a datetime or timestep friendly
                ---> `range_[1]` is the highter hours value not highter limit
                     so if range_[1]==8 columns with ``8h 30 min`` will be kept.
        """
        frame = frame.loc[frame.index.hour <= range_[1]]
        frame = frame.loc[frame.index.hour >= range_[0]]
        return frame

    @staticmethod
    def keep_month(frame, month):
        """
            Return frame without rows where year not match.
            Index must be datetime friendly.
        """
        return frame.loc[frame.index.month == month]

    @staticmethod
    def keep_year(frame, year=2014):
        """
            Return frame without rows where year not match.
            Index must be datetime friendly.
        """
        return frame.loc[frame.index.year == year]

    @staticmethod
    def resample(frame, sample='30min', interpolate=True, **kwargs):
        """
            Reduce dataframe with a datetime index.
            **kwargs can be fill_method, limit, label, loffset, axis, kind, ...
                ---> See DataFrame.resample or Series.resample
        """
        if interpolate is True:
            return frame.resample(sample, **kwargs).interpolate()
        else:
            return frame.resample(sample, **kwargs)

    def add_column(self, frame, used_cols, operator='+'):
        """
            Return a new dataframe column with current columns.
        """
        operations = {'+': frame[used_cols[0]] + frame[used_cols[1]],
                      '-': frame[used_cols[0]] - frame[used_cols[1]],
                      '/': frame[used_cols[0]] / frame[used_cols[1]],
                      '*': frame[used_cols[0]] * frame[used_cols[1]]}
        return operations[operator]

    def change_names(self, conv_dict={}, columns=None):
        """
            Change a specific list name. Return a list of news columns.
            Example : frame.columns = change_names({"old": "new"},
                                                      frame.columns)
        """
        if columns is None:
            columns = list(self.frame.columns)
        else:
            columns = list(columns)
        for before, after in conv_dict.items():
            try:
                columns[columns.index(before)] = after
            except ValueError as e:
                print(e, " of columns")
        return columns

    def col_sum_map(self, frame, cols_map, match_map, used_col="index",
                    start_sum=0, debug=False):
        """
            Return sum of used_col values for all cols_map which
            respect match_map structure and a dict of each timestep of match.
                - frame : DataFrame
                - cols_map : list of columns to test
                - match_map : sequence of corresponding cols_map value
                              (wanted value for each col of cols_map)
                - used_col : column used for operations of summation
                - summation : start value for frame summation
                - debug : print(summation, dict of step summation)
        """
        # Init
        frame = frame[:]  # Create explicit copy to avoid warning message
        summation = start_sum
        step_list, flag = [], False
        # Avoid duplicate operations
        all_ind, last_ind = frame.index, frame[len(frame)-1:].index
        # Check parameters
        assert len(cols_map) == len(match_map), "Must have same lengths"
        # Add `Test` column
        frame["Test"] = 1
        # Change `Test` column values (0 if not match, else not change)
        for el in range(len(cols_map)):
            frame.loc[(frame[cols_map[el]] != match_map[el]), "Test"] = 0
        # Start iteration over dataframe index
        for ind in all_ind:
            pass_test = True
            if not frame["Test"][ind] == 1:
                pass_test = False
            if pass_test and not flag:
                if used_col == "index":
                    prev_val = ind
                else:
                    prev_val = col_op[ind]
                prev_ind = ind
                flag = 1
            # Sum rows
            elif (not pass_test or ind == last_ind) and flag:
                if used_col == "index":
                    summ = ind - prev_val
                else:
                    summ = col_op[ind] - prev_val
                summation += summ
                step_list.append({"sum": summ,
                                  "start": prev_ind,
                                  "end": ind})
                flag = 0
        summation = summation - start_sum
        if debug:
            print("Summation : {}\n{}\n{}\n".format(summation,
                                                    step_list,
                                                    frame))
        return summation, step_list

    def bar_energy(self, frame, fields=None, new_fields=(),
                   interval=None):
        """
            Proceed all treatments to extract structure to plot energy Bar
            new_fields index must be strutured as below:
                0 : new column name
                1 : first column of values
                2 : second column of values
                3 : operator between 1 and 2 (can be '+', '-', '*', '/')
                    ---> frame[0] = frame[1] operator[3] frame[2]
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
        lab_interval = interval or self.length
        # Create indices
        indices = ["{:%B}".format(frame.index[i]) for i in range(lab_interval)]
        # Numerical index for each Bar
        frame.index = [el for el in range(1, lab_interval+1)]
        if new_fields:
            # For each new columns
            for new in new_fields:
                # Create new columns
                frame[new[0]] = self.add_column(frame,
                                                used_cols=(new[1], new[2]),
                                                operator=new[3])
        return frame, indices

    def diag_energy(self, frame, fields=None, month=12,
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
        """ Proceed all actions to prepare data for box plotting """
        fields = fields or self.fields
        # Reduce dataframe
        frame = self.resample(frame)
        # Get chunks
        frame = self.reduce_data(frame, fields)
        # Keep only diurnal values
        if diurnal:
            for ind in range(len(frame)):
                frame[ind] = self.keep_hour_range(frame[ind])
        return frame


class MultiPlotter(object):

    """
        Base class for combined plots
            - frames must be a dict of dataframes or of list of dataframes
            - colors is a tuple of fiths' length tuples
            - title the figure title
            - sharex set to True to share xaxis with all plots
            - sharey set to True to share yaxis with all plots
    """
    # Text formatters
    font_title = {'size': 16,
                  'family': 'Anonymous Pro'}
    font_mainTitle = {'color': '#002b36',
                      'weight': 'bold',
                      'size': '25',
                      'family': 'Anonymous Pro'}
    font_base = {'family': 'serif',
                 'size': 13}
    font_legend = {'size': 13,
                   'family': 'Anonymous Pro'}
    width = 2  # Line width
    colormap = "Accent"  # Color set
    background_color = (1, 0.98, 0.98)  # background_color old=(0.84, 0.89, 0.9)

    sample = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    names = ['January', 'February', 'March', 'April', 'May',
             'June', 'July', 'August', 'September', 'October',
             'November', 'December']

    def __init__(self, frames, colors, title='Title', nb_rows=2, nb_cols=2,
                 sharex=False, sharey=False):
        self.title = title
        self.frames = frames
        self.colors = colors
        self.title = title
        self.nb_rows = nb_rows
        self.nb_cols = nb_cols
        self.sharex = sharex
        self.sharey = sharey
        # Get all dataframes names
        self.data_names = self.fig_names()
        # Space between boxplot groups
        self.pad = 1

    def fig_init(self, figsize=(20, 10), title_pos=(0.5, 0.93), facecolor=None,
                 ha='center', sharex=None, sharey=None):
        """ Create all needed axes """
        # Default parameters
        sharex = sharex or self.sharex
        sharey = sharey or self.sharey
        facecolor = facecolor or self.background_color
        # Drawing graphs according to number of dataframes
        self.fig, self.axes = plt.subplots(nrows=self.nb_rows,
                                           ncols=self.nb_cols,
                                           figsize=figsize,
                                           sharex=self.sharex,
                                           sharey=self.sharey,
                                           facecolor=facecolor)
        self.figure_title(ha=ha, pos=title_pos)
        self._zoomed = False
        # Add event on click (see zoom, unzoom and on_key_m)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        # Tollbar instance
        self.toolbar = self.fig.canvas.toolbar

    def zoom(self, selected_ax):
        """
            Additional option to zoom to full screen current selected_ax.
        """
        # Set visible to false for all figures
        for ax in self.axes.flat:
            ax.set_visible(False)
        # Get selected_ax current position and change to full screen
        self._original_size = selected_ax.get_position()
        selected_ax.set_position([0.125, 0.1, 0.775, 0.8])
        selected_ax.set_visible(True)
        # Change flag to change effect on next click
        self._zoomed = True

    def unzoom(self, selected_ax):
        """
            Additional option to unzoom current selected_ax.
        """
        selected_ax.set_position(self._original_size)
        for ax in self.axes.flat:
            ax.set_visible(True)
        # Change flag to change effect on next click
        self._zoomed = False

    def display_axis(self, selected_ax):
        """ Additional option to hide/show current selected_ax. """
        if selected_ax.get_visible() is True:
            selected_ax.set_visible(False)
        else:
            selected_ax.set_visible(True)

    def on_key(self, event):
        """
            Event to run zoom or unzoom function.
        """
        # If no axes under mouse
        if event.inaxes is None:
            return
        if event.key == "m":
            if self._zoomed:
                self.unzoom(event.inaxes)  # Axe instance
            else:
                self.zoom(event.inaxes)  # Axe instance
        elif event.key == "k":
            self.display_axis(event.inaxes)
        self.fig.canvas.draw()

    def figure_title(self, pos=(0.5, 0.95), ha='center', fontdict={}):
        """ Set title text inside canvas and figure """
        self.fig.canvas.manager.set_window_title(self.title)
        plt.figtext(pos[0], pos[1], self.title, ha=ha,
                    fontdict=fontdict or self.font_mainTitle)

    def adjust_plots(self, top=None,  bottom=None,  left=None,  right=None,
                     hspace=None, wspace=None):
        """ Force figure padding.  None lead to default rc parameters. """
        self.fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right,
                                 hspace=hspace, wspace=wspace)

    def show(self):
        """ Show plot  """
        plt.show()

    def fig_names(self):
        """ Return name of each dataframes inside self.frames """
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
            Return always right subscription of self.axes.
            Used when squeeze=True inside plt.subplots.
        """
        if hasattr(self.axes, '__getitem__'):
            if self.nb_cols <= 1 or self.nb_rows <= 1:
                return self.axes[nb_row]
            else:
                return self.axes[nb_row][nb_col]
        else:
            return self.axes

    def auto_format(self):
        """ Quick access to date auto formatter. """
        self.fig.autofmt_xdate()

    def set_xtiks_labels(self, pos, names, rotation=30):
        """ Quick access to set xticks labels. """
        self.catch_axes(*pos).set_xticklabels(names, rotation=rotation)

    def change_title(self, pos, title, font, loc='center'):
        """ Quick access to axis title. """
        self.catch_axes(*pos).set_title(label=title,
                                        fontdict=font or self.font_title,
                                        loc=loc)

    def set_boxes(self, box, marker=('', '', '', '1', ''), kw={}):
            """
                Change boxplot color structure.
                Boxes parts list order for each values :
                    - boxes, caps, whiskers, fliers, medians
                - marker used to set marker specifications
                    - marker[0] must exist but not used
                - kw will be passed to each plt.setp() :
                     - each kw parameters must be a list or tuple of 5 values.
                       to match box parts.
            """
            # Default kw
            kw = kw or {'linewidth': (1.5, 1, 1, 0.5, 10),
                        'alpha': (0.6, 1, 1, 1, 0.2),
                        'color': ('#268bd2', '#002b36', '#268bd2',
                                  '#268bd2', '#dc322f')}
            # Unpack kw inside all parts
            plt.setp(box['boxes'],
                     **{key: val[0] for key, val in kw.items()})
            plt.setp(box['caps'], marker=marker[1],
                     **{key: val[1] for key, val in kw.items()})
            plt.setp(box['whiskers'], marker=marker[2],
                     **{key: val[2] for key, val in kw.items()})
            plt.setp(box['fliers'], marker=marker[3],
                     **{key: val[3] for key, val in kw.items()})
            plt.setp(box['medians'], marker=marker[4],
                     **{key: val[4] for key, val in kw.items()})

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
                                     prop=self.font_legend, **kwargs)
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

    def clean_axes(self, number=None):
        """
            Delete useless axe according to number
            default to None : number = len(self.frames)
        """
        try:
            flat = [x for i in self.axes for x in i]
        # Catch error when only one plot
        except TypeError:
            print("Only one axe, so nothing deleted")
            flat = [None]
        # If number is None (default)
        if not number:
            number = len(self.frames)
        if number < len(flat):
            row = len(self.axes) - 1
            col = len(self.axes[0]) - 1
            self.axes[row][col].set_visible(False)

    def frame_plot(self, frame, fields="all", title='Line me', loc='left',
                   kind="area", pos=(0, 0), colormap="default", colors=None,
                   legend=True, **kwargs):
        """
            Used to plot dataframes.
            - title used as text value for title
            - loc used to place title
            - pos used to set specific axe (always a tuple even if only one axe)
            - colors are colors of parts. If None self.colors used
            - **kwargs will be passed to axe.pie()
        """
        if colormap == "default":
            colormap = self.colormap
        if fields == "all":
            columns = frame.columns
        else:
            columns = fields
        print('\n---' + 'Plotting {}2D'.format(kind.capitalize()) +
              '---' + '\n', columns, "\n")

        # Plot all plots
        self.catch_axes(*pos).set_title(label=title,
                                        fontdict=self.font_title,
                                        loc=loc)
        if colormap:
            frame[columns].plot(ax=self.catch_axes(*pos), kind=kind,
                                colormap=colormap, **kwargs)
        else:
            frame[columns].plot(ax=self.catch_axes(*pos), kind=kind,
                                colors=colors, **kwargs)

    def boxes_mult_plot(self, list_frame, colors=(None,)*5,  title='Box me !',
                        loc='left', pos=(0, 0), widths=0.6, whis=1000,
                        mean=True, mean_dict={}, box_dict={}, **kwargs):
        """
            Draw a boxplot for each columns inside each dataframe of
            the list_frame. Each groups have space between them.
            - list_frame must be a list of dataframes
            - colors is a tuple of tuple :
                - one tuple of five colors for each column of data
            - title used as column name and text value for title
            - loc used to place title
            - pos used to set specific axe (always a tuple even if only one axe)
            - widths used to set boxes width
            - whis used as a factor for
            - mean can be True or False :
                - True  ---> box['medians'] = average of each box
                - False ---> box['medians'] = median of each box
            - mean_dict used as a Dict of parameters passed to axe.plot()
            - box_dict used as a Dict of parameters passed to self.set_boxes()
                - None leads to default value
            - **kwargs will be passed to axe.boxplot()
        """
        # Defaults
        mean_dict = mean_dict or {'color': '#fdf6e3', 'marker': '*',
                                  'markeredgecolor': '#002b36', 'alpha': 0.5}
        box_dict = box_dict or {'linewidth': (1.5, 1, 1, 0.5, 2),
                                'alpha': (0.6, 1, 1, 1, 0.2)}
        # Print data informations
        columns = list_frame[0].columns
        # Plot all plots
        print('\n---' + 'Plotting Boxes' + '---' + '\n', columns)
        # Plot boxplots of dataframe
        self.catch_axes(*pos).set_title(label=title,
                                        fontdict=self.font_title,
                                        loc=loc)
        for ind, col in enumerate(columns):
            # Get list of all values for each col
            vals = [el[col] for el in list_frame]
            # Switch between default and user value according to mean boolean
            average_dict = {True: [average(el[col]) for el in list_frame],
                            False: None}
            xticks = self.optimize_xticks_pos(list_frame, start=ind)
            temp = self.catch_axes(*pos).boxplot(vals,
                                                 positions=xticks,
                                                 widths=widths,
                                                 whis=whis,
                                                 usermedians=average_dict[mean],
                                                 **kwargs)
            # Draw average or medians markers value for each box
            for i in range(len(vals)):
                # Get x and y values of each box and keep average value
                med_x = average(temp['medians'][i].get_xdata())
                med_y = average(temp['medians'][i].get_ydata())
                self.catch_axes(*pos).plot(med_x, med_y, **mean_dict)
            # Add or change color tuple inside box_dict dict
            box_dict['color'] = colors[ind] or self.colors[ind]
            # Set boxes parameters
            self.set_boxes(temp, kw=box_dict)
        # Get group center
        start = int(len(list_frame[0].columns)/2+0.5) - 1
        # Set legend and xticks positions
        self.format_boxticks(list_frame, pos, start)

    def diag_plot(self, frame, to_diag, title='Diag me', labels=None,
                  loc='left', pos=(1, 0), explode=(0.1, 0, 0), radius=0.8,
                  colors=None, legend=False, **kwargs):
        """
            Used to plot diagrams with a dataframe prepared with EvalData class.
            - to_diag is a list of columns names to plot
            - title used as column name and text value for title
            - loc used to place title
            - pos used to set specific axe (always a tuple even if only one axe)
            - explode used to add specific emphaze (must match to_diag length)
            - radius used to change diagram size
            - colors are colors of parts. If None self.colors used
            - labels used to change pie part names
            - **kwargs will be passed to axe.pie()
        """
        # Plot all plots
        # Keep only needed values (return a new dataframe)
        temp = pd.concat([frame[frame.index == el] for el in to_diag])
        print('\n---' + 'Plotting Diagrams' + '---' + '\n', temp)
        self.catch_axes(*pos).set_title(label=title,
                                        fontdict=self.font_title,
                                        loc=loc)
        self.catch_axes(*pos).pie(temp, colors=colors or self.colors,
                                  labels=labels or to_diag, shadow=True,
                                  autopct='%1.1f%%', startangle=90,
                                  explode=explode, radius=radius, **kwargs)
        # Set axe parameters
        self.catch_axes(*pos).legend(prop=self.font_legend)
        self.catch_axes(*pos).legend().set_visible(legend)

    def bar_sup_plot(self, frame, fields, colors={}, loc='left', pos=(1, 1),
                     names=[], title='Hist me', h_width=0.9,
                     ylabel="Kwh", emphs=None, **kwargs):
        """
            Plot a superimposed bar plot of each fields inside the frame and
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
        print('\n---' + 'Plotting superimposed Bars' + '---' + '\n', columns)
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
                                     loc="best", prop=self.font_legend)

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
        print('\n---' + 'Plotting cumulated Bars' + '---' + '\n', columns)
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
        # Add auto legend
        self.catch_axes(*pos).legend([temp[col] for col in columns],
                                     list(columns),
                                     loc="best", prop=self.font_legend)


########################
#### Main Program : ####
########################


if __name__ == '__main__':
    fold = FOLDER / "clean"
    # Dynamic selection
    welcome = "Please choose csv file name inside this folder or default " + \
              "(press enter) :\n{} : ".format(fold)
    name = input(welcome)
    if name == "":
        name = "chambery_20140825.csv"  # Only lower cases with _daymonthyear.csv
    dataframe = fold / name
    name = name.split("_")[0]

    # Read csv and store values as a dict
    frames = read_csv((dataframe, ),
                      convert_index=(convert_to_datetime,)*10,
                      delimiter=(";",)*10,
                      index_col=("Date",)*10,
                      in_conv_index=(None,)*10,
                      skiprows=(1,)*10,
                      splitters=("_",)*10)

    #
    ################## EvalData class : Prepare datas ##################
    #

    data = EvalData(frames[name])

    # Change data columns names
    conv_dict = {"DrawingUp_Energy": "ECS", "Radiator_Energy": "Chauffage",
                 "Collector_Energy": "Energie solaire",
                 "Boiler_Energy": "Appoint",
                 "HDifTil_collector": "Diffus", "HDirTil_collector": "Direct"}

    print("\n---Csv columns names after treatments---")
    data.frame.columns = data.change_names(conv_dict, data.frame.columns)
    print(data.frame.columns)

    # New fields
    new_fields = (("Besoins", "ECS", "Chauffage", "+"),
                  ("Consommations", "Energie solaire", "Appoint", "+"),
                  ("Pertes", "Consommations", "Besoins", "-"),
                  ("Taux de couverture", "Energie solaire", "Consommations", "/"))

    # Prepare all plots
    # BAR
    data.hist = data.bar_energy(data.frame, new_fields=new_fields,
                                        fields=["Energie solaire", "Appoint",
                                                "Chauffage", "ECS"])

    # DIAGRAM
    data.diag = data.diag_energy(data.frame,
                                         fields=["Energie solaire", "Appoint",
                                                 "Chauffage", "ECS"],
                                         new_fields=new_fields)

    # BOXPLOT
    data.box_T = data.box_actions(data.frame, fields=['T3', 'T4', 'T5'])
    data.box_H = data.box_actions(data.frame, fields=['Diffus', 'Direct'])

    # LINE2D
    data.line = data.resample(frame=data.frame, sample='12h')

    # #
    # ################## MultiPlotter class : Plot datas ##################
    # #

    # Prepare boxplots as first added data to MultiPlotter class
    frames_ = {'Temps': data.box_T, 'Irradiations': data.box_H}

    # Colors
    col_dict = {'box': (('#268bd2', '#002b36', '#268bd2', '#268bd2', '#268bd2'),
                        ('#586e75', '#002b36', '#586e75', '#586e75', '#268bd2'),
                        ('#859900', '#002b36', '#859900', '#859900', '#268bd2')),
                'diag': ['#fdf6e3', '#268bd2', '#cb4b16'],
                'bar': {"Appoint": "#dc322f", "Chauffage": "#fdf6e3",
                        "ECS": "#268bd2", "Energie solaire": "orange",
                        "Pertes": "#cb4b16"}}
    # # Plotter main title
    title = "Bilan de la simulation de " + name[0].upper() + name[1:]
    # Create plotter class
    Plot = MultiPlotter(frames_, nb_cols=2, nb_rows=2, colors=col_dict["box"],
                        title=title)
    Plot.fig_init()
    Plot.figure_title()

    # # LINE2D
    # Plot.frame_plot(data.line, fields=['Energie solaire', 'Appoint'], linewidth=2)

    # Add boxplots
    title = "Evolution mensuel de la variation des températures des ballons"
    Plot.boxes_mult_plot(Plot.frames['Temps'], pos=(0, 0),
                         title=title, patch_artist=True)
    title = "Evolution mensuel de la variation de la puissance captable"
    Plot.boxes_mult_plot(Plot.frames['Irradiations'], pos=(1, 0),
                         title=title, patch_artist=True)

    # Add diagram
    Plot.frames['Diagplot'] = data.diag  # Keep only dataframe
    Plot.colors = col_dict["diag"]
    Plot.diag_plot(Plot.frames['Diagplot'], pos=(0, 1), loc='center',
                   to_diag=['Chauffage', 'ECS', 'Pertes'],
                   title='Taux de couverture', legend=False)

    # Add bar plot
    Plot.frames['Barplot'] = data.hist[0]  # Keep only dataframe
    # Change colors tuple to color dict
    Plot.colors = col_dict["bar"]
    title = "Evolution mensuel des apports et consommations d'énergie"
    Plot.bar_cum_plot(Plot.frames['Barplot'], emphs=['Energie solaire'],
                      pos=(1, 1), title=title,
                      fields=["ECS", "Chauffage", "Pertes"])
    # Prepare Taux de couverture (list of formatted data)
    short_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                   'Jun', 'Jul', 'Aug', 'Sept', 'Oct',
                   'Nov', 'Dec']
    # Each xticks = short month name + Taux de couverture de couverture solaire mensuelle
    percents = ['{:.1%}'.format(i) for i in Plot.frames['Barplot']['Taux de couverture'].values]
    Plot.change_xticks_labels([short_names, [' : ']*12,
                               percents])

    # Adjust plot format
    Plot.adjust_plots(hspace=0.3, top=0.85, left=0.05)
    # Removes empty axes (only last one for now)
    Plot.clean_axes()
    Plot.show()

    @benchmark
    def test():
        somme, steps = data.col_sum_map(data.frame, debug=False,
                                        cols_map=["S2_state",
                                                  "Vsolar_state",
                                                  "Vextra_state"],
                                        match_map=(100, 100, 100),
                                        start_sum=datetime.datetime(year=2014,
                                                                    month=1,
                                                                    day=1))
        print("Durée du chauffage solaire annuel pour {} : {}".format(name, somme))

    test()
