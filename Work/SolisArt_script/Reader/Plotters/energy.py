#! /usr/bin/env python
# -*- coding:Utf8 -*-


from numpy import arange


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

class EnergyPlotter(plotter.CombiPlotter):

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
            - diurne flag used when we need only diurnal values
    """

    names = ['January', 'February', 'March', 'April', 'May',
             'June', 'July', 'August', 'September', 'October',
             'November', 'December']
    fields = ["Collector_Energy", "Boiler_Energy",
              "Radiator_Energy", "DrawingUp_Energy"]

    def __init__(self, frames, title, blocs, colors, steps='months',
                 length=12, sharex=True):
        super().__init__(frames=frames, title=title, steps=steps,
                         length=length, sharex=sharex)
        self.blocs = blocs
        self.colors = colors
        self.frames_plt = {}
        for frame in self.frames:
            # Temporary variable "temp" used to make code more clean
            # "temp" becomes dataframe for each frame inside self.frames
            temp = self.reduce_data(self.frames[frame], self.blocs)
            # Keep only last value for each sample
            temp = [temp[i][-1:] for i in range(len(temp))]
            # Substract next value with current values to get only energy
            # used/lost inside each sample
            temp = (temp[0],) + tuple(temp[ind+1] - temp[ind].values for ind in range(len(temp)-1))
            self.frames_plt.setdefault(frame, temp)

    def plotting_shape(self):
        """
            Store all dataframes names and its fields
        """
        self.data_names = [el for el in self.frames_plt]
        self.columns = self.frames_plt[self.data_names[0]][0].columns

    def plotting(self, loc='left'):
        """
            Draw all plots according to subplots shape
            Each plot title get inside self.data_names
            Each plot column name get inside self.columns
            Each plot color tuple get inside self.colors
        """
        if len(self.frames) >= 4:
            self.plot_col(loc=loc)
        else:
            self.plot_row(loc=loc)

    def plot_col(self, loc):
        """Used only if more than 4 dataframe inside self.frames."""
        # Print data informations
        print(self.data_names, self.columns)

    def plot_row(self, loc):
        """Used only if less than 4 dataframe inside self.frames."""
        # Print data informations
        print(self.data_names, self.columns)


class EnergyDiagPlotter(EnergyPlotter):

    """
        To draw Energy diagrams
            - frames must be a list of dataframes
            - title the figure title
            - blocs a list of each columns names which will be extracted from
              from each dataframes
            - steps used to sample data step by step
                'month' lead to : self.steps = [el*48 for el in self.sample]
            - length used to limit iteration
            - sharex set to True to share xaxis with all plots
            - diurne flag used when we need only diurnal values
    """

    def __init__(self, frames, title, blocs, colors, steps='months',
                 length=12, sharex=True):
        super().__init__(frames=frames, title=title, blocs=blocs, colors=colors,
                         steps=steps, length=length, sharex=sharex)

        # For each sample of dataframe
        for frame in self.frames_plt.values():
            # Only if necessary columns names are presents
            for data in frame:
                if all([el in data.columns for el in self.fields if el in self.fields]):
                    # Diurnal overheating inside energy_ch["Radiator_Energy"]. Bad issue ???
                    data["Besoins"] = (data["DrawingUp_Energy"] +
                                       data["Radiator_Energy"])
                    data["Consommations"] = (data["Collector_Energy"] +
                                             data["Boiler_Energy"])
                    data["Pertes"] = data["Consommations"] - data["Besoins"]
                    data["Taux de couverture"] = (data["Collector_Energy"] /
                                                  data["Consommations"])
        # For each sample of dataframe
        for key, frame in self.frames_plt.items():
                temp = pd.concat([el for el in frame])
                # Cumul all months values to get a fully year for each columns
                temp = pd.DataFrame(temp.sum(), columns=['Full year'])
                # Update solar cover to real value
                temp[-1:] = (temp["Collector_Energy":"Collector_Energy"].values /
                             temp["Consommations":"Consommations"].values)
                # Add dataframe to frames dict
                self.frames_plt[key] = [temp]
        print(self.frames_plt['marseille'])  # Test


class EnergyHistPlotter(EnergyPlotter):

    """
        To draw Energy histograms
            - frames must be a list of dataframes
            - title the figure title
            - blocs a list of each columns names which will be extracted from
              from each dataframes
            - steps used to sample data step by step
                'month' lead to : self.steps = [el*48 for el in self.sample]
            - length used to limit iteration
            - sharex set to True to share xaxis with all plots
    """

    def __init__(self, frames, title, blocs, colors, steps='months',
                 length=12, sharex=True):
        super().__init__(frames=frames, title=title, blocs=blocs, colors=colors,
                         steps=steps, length=length, sharex=sharex)
        # Field to redraw. Each top bar will be redraw to upgrade it vision
        self.emph = "Boiler_Energy"
        # For each sample of dataframe
        for key, frame in self.frames_plt.items():
                temp = pd.concat([el for el in frame])
                self.indices = ["{:%B}".format(temp.index[i]) for i in range(self.length)]
                temp.index = [el for el in range(1, self.length+1)]
                self.frames_plt[key] = temp
        print(self.frames_plt['chambery'])  # Test

    def plotting_shape(self):
        """
            Store all dataframes names and its fields.
            Overload from inherit class
        """
        self.data_names = [el for el in self.frames_plt]
        self.columns = self.frames_plt[self.data_names[0]].columns

    def plot_col(self, loc):
        """
            Used only if more than 4 dataframe inside self.frames.
            Draw all bars
        """
        # Print data informations
        print(self.data_names, self.columns)
        # Plot all plots
        for ind1, name in enumerate(self.data_names):
            self.axes[ind1 // 2][ind1 % 2].set_title(label=name,
                                                     fontdict=self.font_title,
                                                     loc=loc)
            # Draw all bar and stock them inside a dict
            temp = {col: self.axes[ind1 // 2][ind1 % 2].bar(self.frames_plt[name].index.values,
                                                            self.frames_plt[name][col].values,
                                                            color=self.colors[col],
                                                            width=0.9) for col in self.frames_plt[name].columns}
            # Draw a line at the top of each "Boiler_Energy" barplots
            tops = ([(el.get_x(), el.get_x()+temp[self.emph][0].get_width()),
                     (el.get_height(),)*2] for el in temp[self.emph])
            # Add lines to see emphase on all samples
            for top in tops:
                l = matplotlib.lines.Line2D(*top,
                                            linewidth=3,
                                            color=colors[self.emph])
                self.axes[ind1 // 2][ind1 % 2].add_line(l)
            # Set axe parameters
            self.axes[ind1 // 2][ind1 % 2].set_ylabel("Energie en Kwh", labelpad=20)
            self.axes[ind1 // 2][ind1 % 2].set_xlim(0.9, len(self.names)+1)
            self.axes[ind1 // 2][ind1 % 2].set_xticks(arange(1.45, len(self.names)+1.45, 1))
            self.axes[ind1 // 2][ind1 % 2].set_xticklabels(self.names)
            print(temp)

    def plot_row(self, loc):
        """Used only if less than 4 dataframe inside self.frames."""
        # Print data informations
        print(self.data_names, self.columns)
        # Plot all plots
        for ind1, name in enumerate(self.data_names):
            self.axes[ind1].set_title(label=name,
                                      fontdict=self.font_title,
                                      loc=loc)
            # Draw all bar and stock them inside a dict to access right data
            #
            temp = {col: self.axes[ind1].bar(self.frames_plt[name].index.values,
                                             self.frames_plt[name][col].values,
                                             color=self.colors[col],
                                             width=0.9) for col in self.frames_plt[name].columns}
            # Draw a line at the top of each "Boiler_Energy" barplots
            tops = ([(el.get_x(), el.get_x()+temp[self.emph][0].get_width()),
                     (el.get_height(),)*2] for el in temp[self.emph])
            # Add lines to see emphase on all samples
            for top in tops:
                l = matplotlib.lines.Line2D(*top,
                                            linewidth=3,
                                            color=colors[self.emph])
                self.axes[ind1].add_line(l)
            # Set axe parameters
            self.axes[ind1].set_ylabel("Energie en Kwh", labelpad=20)
            self.axes[ind1].set_xlim(0.9, len(self.names)+1)
            self.axes[ind1].set_xticks(arange(1.45, len(self.names)+1.45, 1))
            self.axes[ind1].set_xticklabels(self.names)
            print(temp)
        # Add auto legend
        self.axes[0].legend([temp[col] for col in self.columns], list(self.columns),
                            loc="best", prop=self.font_title)

########################
#### Main Program : ####
########################


if __name__ == '__main__':
    chambery = FOLDER / "clean/chambery_30062014.csv"
    marseille = FOLDER / "clean/marseille_30062014.csv"
    strasbourg = FOLDER / "clean/strasbourg_07072014.csv"
    bordeaux = FOLDER / "clean/bordeaux_30062014.csv"

    title = "Evolution mensuel des apports et consommations d'énergie (en KWh)"

    # Color dict which must match all plots columns
    colors = {"Boiler_Energy": "#dc322f", "Radiator_Energy": "#fdf6e3",
              "DrawingUp_Energy": "#268bd2", "Collector_Energy": "orange",
              "Pertes": '#cb4b16'}

    fields = ["Collector_Energy", "Boiler_Energy", "Radiator_Energy", "DrawingUp_Energy"]
    names = {"Radiator_Energy", "DrawingUp_Energy", "Pertes"}

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

    # DiagEnergy = EnergyDiagPlotter(frames, title, blocs=fields, colors=colors).draw()
    DiagEnergy = EnergyHistPlotter(frames, title, blocs=fields, colors=colors).draw()
