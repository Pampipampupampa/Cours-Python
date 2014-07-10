#! /usr/bin/env python
# -*- coding:Utf8 -*-


try:
    from .parameters import *
    from . import plotter
except SystemError as e:
    print("Local import")
    from parameters import *
    import plotter


#######################################
#### Classes, Methods, Functions : ####
#######################################

class BoxPlotter(plotter.CombiPlotter):

    """
        Draw box plots for each steps (data length read) 'length' times
    """

    names = ['January', 'February', 'March', 'April', 'May',
             'June', 'July', 'August', 'September', 'October',
             'November', 'December']

    def __init__(self, frames, title, blocs, colors, steps='months',
                 length=12, diurnal=False, sharex=True):
        super().__init__(frames=frames, title=title, steps=steps,
                         length=length, sharex=sharex)
        self.blocs = blocs
        self.colors = colors
        self.frames_plt = {}
        for frame in self.frames:
            # Temporary variable "temp" used to make code more clean
            # "temp" becomes dataframe for each frame inside self.frames
            temp = self.reduce_data(self.frames[frame], self.blocs)
            # Keep only daily sun values (9am to 6:30pm)
            if diurnal:
                print("Keep only data values between 9am to 6:30pm.")
                for i in range(len(temp)):
                    temp[i] = temp[i].loc[temp[i].index.hour <= 18]
                    temp[i] = temp[i].loc[temp[i].index.hour >= 9]
            self.frames_plt.setdefault(frame, temp)

    def plotting(self, loc='left', widths=0.6, whis=10000):
        """
            Draw all plots according to subplots shape
            Each plot title get inside self.data_names
            Each plot column name get inside self.columns
            Each plot color tuple get inside self.colors
                - loc used to place title text
                - fontdict used to format title text
                - widths used to set boxes width
                - whis used as a multiplicator for get more or less values
                  inside whiskers

            Any argument you pass after `whis` will be passed to `self.set_boxes`.
        """
        if len(self.frames) >= 4:
            self.plot_boxes_col(loc=loc, widths=widths, whis=whis)
        else:
            self.plot_boxes_row(loc=loc, widths=widths, whis=whis)

    def formatting(self):
        """
            Change ticks values to always be between blocks of data.
            Add legend which always match plotting datas
                - fontdict used to format legend text
        """
        if len(self.frames) >= 4:
            self.formatting_col()
        else:
            self.formatting_row()

    def plotting_shape(self):
        self.positions = [el for el in range(0, 12*len(self.frames)+1,
                                             len(self.frames)+1)]
        self.data_names = [el for el in self.frames_plt]
        self.columns = self.frames_plt[self.data_names[0]][0].columns

    def forcing(self):
        self.fig.subplots_adjust(top=0.85, bottom=0.05, left=0.05, right=0.95)

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

    def plot_boxes_col(self, loc, widths, whis):
        """Used only if more than 4 dataframe inside self.frames."""
        # Print data informations
        print(self.data_names, self.columns)
        # Plot all plots
        for ind1, name in enumerate(self.data_names):
            self.axes[ind1 // 2][ind1 % 2].set_title(label=name,
                                                     fontdict=self.font_title,
                                                     loc=loc)
            for ind2, plot in enumerate(self.columns):
                vals = [el[plot] for el in self.frames_plt[name]]
                pos = [el for el in range(ind2, 12*(len(self.columns)+1),
                                          len(self.columns)+1)]
                temp = self.axes[ind1 // 2][ind1 % 2].boxplot(vals,
                                                              positions=pos,
                                                              widths=widths,
                                                              whis=whis)
                self.set_boxes(temp, colors=self.colors[ind2])

    def plot_boxes_row(self, loc, widths, whis):
        """Used only if less than 4 dataframe inside self.frames."""
        # Print data informations
        print(self.data_names, self.columns)
        # Plot all plots
        for ind1, name in enumerate(self.data_names):
            self.axes[ind1].set_title(label=name,
                                      fontdict=self.font_title,
                                      loc=loc)
            for ind2, plot in enumerate(self.columns):
                vals = [el[plot] for el in self.frames_plt[name]]
                pos = [el for el in range(ind2, 12*(len(self.columns)+1),
                                          len(self.columns)+1)]
                temp = self.axes[ind1].boxplot(vals,
                                               positions=pos,
                                               widths=widths,
                                               whis=whis)
                self.set_boxes(temp, colors=self.colors[ind2])

    def formatting_col(self):
        """Used only if more than 4 dataframe inside self.frames."""
        # Change xticks values to put xtickslabels between boxes (same tick per boxes pair)
        self.axes[0][0].set_xticks([el for el in range(1, 12*(len(self.columns)+1),
                                                       len(self.columns)+1)])
        self.axes[0][0].set_xlim((-1, 12*(len(self.columns)+1)))
        self.axes[0][0].set_xticklabels(self.names)
        # Add legend by drawing curves and hiding them just after
        curves = []  # Container for Line2D
        for col in self.colors:
            # Unpack and keep only Line2D instances
            h, = self.axes[0][0].plot([1, 1], col[0], linewidth=2)
            curves.append(h)  # Group all Line2D inside a list
        self.axes[0][0].legend(curves, list(self.columns), prop=self.font_title)
        for plot in curves:
            plot.set_visible(False)

    def formatting_row(self):
        """Used only if less than 4 dataframe inside self.frames."""
        # Change xticks values to put xtickslabels between boxes (same tick per boxes pair)
        self.axes[0].set_xticks([el for el in range(1, 12*(len(self.columns)+1),
                                                    len(self.columns)+1)])
        self.axes[0].set_xlim((-1, 12*(len(self.columns)+1)))
        self.axes[0].set_xticklabels(self.names)
        # Add legend by drawing curves and hiding them just after
        curves = []  # Container for Line2D
        for col in self.colors:
            # Unpack and keep only Line2D instances
            h, = self.axes[0].plot([1, 1], col[0], linewidth=2)
            curves.append(h)  # Group all Line2D inside a list
        self.axes[0].legend(curves, list(self.columns), prop=self.font_title)
        for plot in curves:
            plot.set_visible(False)


########################
#### Main Program : ####
########################


if __name__ == '__main__':
    chambery = FOLDER / "clean/chambery_30062014.csv"
    marseille = FOLDER / "clean/marseille_30062014.csv"
    strasbourg = FOLDER / "clean/strasbourg_07072014.csv"
    bordeaux = FOLDER / "clean/bordeaux_30062014.csv"

    title = ("Plage de variation des températures T1 et T12",
             "Plage de variation des températures des ballons",
             "Plage de variation de l'irradiation capté par les capteurs")

    colors = (('#268bd2', '#002b36', '#268bd2', '#268bd2', '#dc322f'),
              ('#586e75', '#002b36', '#586e75', '#586e75', '#dc322f'),
              ('#859900', '#002b36', '#859900', '#859900', '#dc322f'))

    # Read all csv and store values as a dict
    frames = read_csv((chambery, marseille, strasbourg),
                      convert_index=(convert_to_datetime,)*4,
                      delimiter=(";",)*4,
                      index_col=("Date",)*4,
                      in_conv_index=(None,)*4,
                      skiprows=(1,)*4,
                      splitters=("_",)*4)

    # Resample each dataframes to keep only one value each 30min
    # Reduce data treatment and increase speed
    for frame in frames:
        frames[frame] = frames[frame][:].resample('30min').interpolate()

    T1_T12 = BoxPlotter(frames, title=title[0], blocs=['T1', 'T12_house'],
                        colors=colors, diurnal=True).draw()
    tanks = BoxPlotter(frames, title=title[1], blocs=['T3', 'T4', 'T5'],
                       colors=colors, diurnal=False).draw()
    irradiation = BoxPlotter(frames, title=title[2], blocs=['HDifTil_collector',
                                                            'HDirTil_collector'],
                             colors=colors, diurnal=True).draw()
