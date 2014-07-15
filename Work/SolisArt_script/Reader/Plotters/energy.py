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
    """

    names = ['January', 'February', 'March', 'April', 'May',
             'June', 'July', 'August', 'September', 'October',
             'November', 'December']
    fields = ["Collector_Energy", "Boiler_Energy",
              "Radiator_Energy", "DrawingUp_Energy"]

    def __init__(self, frames, title, blocs, colors, steps='months',
                 length=12, sharex=True, plane=4):
        super().__init__(frames=frames, title=title, steps=steps,
                         length=length, sharex=sharex, plane=plane)
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
            Store all dataframes names and its fields.
        """
        self.data_names = [el for el in self.frames_plt]
        self.columns = self.frames_plt[self.data_names[0]].columns

    def fig_title(self):
        self.fig.canvas.manager.set_window_title(self.title)
        plt.figtext(0.5, 0.95, self.title, ha=ha, fontdict=self.font_mainTitle)

    def plotting(self, loc='left'):
        """
            Draw all plots according to subplots shape
            Each plot title get inside self.data_names
            Each plot column name get inside self.columns
            Each plot color tuple get inside self.colors
        """
        # Because of subplots tuple creation (doesn't affect plots organization)
        if len(self.frames) <= 2:
            self.plot_row(loc=loc)
        elif len(self.frames) >= self.plane:
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
            - radius used to change pies sizes
            - explode used to emphase pie parts
    """

    def __init__(self, frames, title, blocs, colors, explode, radius=0.8,
                 steps='months', length=12, sharex=True, plane=1):
        super().__init__(frames=frames, title=title, blocs=blocs, colors=colors,
                         steps=steps, length=length, sharex=sharex, plane=plane)
        # Prepare how and what to print
        self.to_diag = ['Radiator_Energy', 'DrawingUp_Energy', 'Pertes']
        self.to_title = 'Taux de couverture'
        self.radius = radius
        self.explode = explode

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
                self.frames_plt[key] = temp

    def plot_col(self, loc):
        """
            Used only if more than 4 dataframe inside self.frames.
            Draw all bars
        """
        # Print data informations
        print(self.data_names, self.columns)
        # Plot all plots
        for ind1, name in enumerate(self.data_names):
            print('\n---' + name + '---' + '\n', self.frames_plt[name])
            temp = pd.concat([self.frames_plt[name][self.frames_plt[name].index == el] for el in self.to_diag])
            text = "{1} : {0:.2%}".format(self.frames_plt[name].get_value(self.to_title, self.columns[0]),
                                          name)
            self.axes[ind1 // 2][ind1 % 2].set_title(label=text,
                                                     fontdict=self.font_title,
                                                     loc=loc)
            # Draw all bar and stock them inside a dict to access right data
            self.axes[ind1 // 2][ind1 % 2].pie(temp, colors=list(self.colors),
                                               labels=self.to_diag, shadow=True,
                                               autopct='%1.1f%%', startangle=90,
                                               explode=self.explode, radius=self.radius)
            # Set axe parameters
            self.axes[ind1 // 2][ind1 % 2].legend(prop=self.font_title)
        flat = [x for i in self.axes for x in i]
        if len(self.frames_plt) < len(flat):
            row = len(self.axes) - 1
            col = len(self.axes[0]) - 1
            self.axes[row][col].set_visible(False)

    def plot_row(self, loc):
        """Used only if less than 4 dataframe inside self.frames."""
        # Print data informations
        print(self.data_names, self.columns)
        # Plot all plots
        for ind1, name in enumerate(self.data_names):
            print('\n---' + name + '---' + '\n', self.frames_plt[name])
            temp = pd.concat([self.frames_plt[name][self.frames_plt[name].index == el] for el in self.to_diag])
            text = "{1} : {0:.2%}".format(self.frames_plt[name].get_value(self.to_title, self.columns[0]),
                                          name)
            self.axes[ind1].set_title(label=text,
                                      fontdict=self.font_title,
                                      loc=loc)
            # Draw all bar and stock them inside a dict to access right data
            self.axes[ind1].pie(temp, colors=list(self.colors),
                                labels=self.to_diag, shadow=True,
                                autopct='%1.1f%%', startangle=90,
                                explode=self.explode, radius=self.radius)
            # Set axe parameters
            self.axes[ind1].legend(prop=self.font_title)


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
                 length=12, sharex=True, width=0.9):
        super().__init__(frames=frames, title=title, blocs=blocs, colors=colors,
                         steps=steps, length=length, sharex=sharex)
        self.width = width
        # Field to redraw. Each top bar will be redraw to upgrade it vision
        self.emph = "Boiler_Energy"
        # For each sample of dataframe
        for key, frame in self.frames_plt.items():
                temp = pd.concat([el for el in frame])
                self.indices = ["{:%B}".format(temp.index[i]) for i in range(self.length)]
                temp.index = [el for el in range(1, self.length+1)]
                self.frames_plt[key] = temp

    def plot_col(self, loc):
        """
            Used only if more than 4 dataframe inside self.frames.
            Draw all bars
        """
        # Print data informations
        print(self.data_names, self.columns)
        # Plot all plots
        for ind1, name in enumerate(self.data_names):
            print('\n---' + name + '---' + '\n', self.frames_plt[name])
            self.axes[ind1 // 2][ind1 % 2].set_title(label=name,
                                                     fontdict=self.font_title,
                                                     loc=loc)
            # Draw all bar and stock them inside a dict
            temp = {col: self.axes[ind1 // 2][ind1 % 2].bar(self.frames_plt[name].index.values,
                                                            self.frames_plt[name][col].values,
                                                            color=self.colors[col],
                                                            width=self.width) for col in self.frames_plt[name].columns}
            # Draw a line at the top of each "Boiler_Energy" barplots
            tops = ([(el.get_x(), el.get_x()+temp[self.emph][0].get_width()),
                     (el.get_height(),)*2] for el in temp[self.emph])
            # Add lines to see emphase on all samples
            for top in tops:
                l = matplotlib.lines.Line2D(*top,
                                            linewidth=3,
                                            color=self.colors[self.emph])
                self.axes[ind1 // 2][ind1 % 2].add_line(l)
            # Set axe parameters
            self.axes[ind1 // 2][ind1 % 2].set_ylabel("Energie en Kwh", labelpad=20)
            self.axes[ind1 // 2][ind1 % 2].set_xlim(self.width, len(self.names)+1)
            self.axes[ind1 // 2][ind1 % 2].set_xticks(arange(1.5-(1-self.width)/2,
                                                             len(self.names)+1.5-(1-self.width)/2,
                                                             1))
            self.axes[ind1 // 2][ind1 % 2].set_xticklabels(self.names)
        # Add auto legend
        self.axes[0][0].legend([temp[col] for col in self.columns], list(self.columns),
                               loc="best", prop=self.font_title)
        flat = [x for i in self.axes for x in i]
        if len(self.frames_plt) < len(flat):
            row = len(self.axes) - 1
            col = len(self.axes[0]) - 1
            self.axes[row][col].set_visible(False)

    def plot_row(self, loc):
        """Used only if less than 4 dataframe inside self.frames."""
        # Print data informations
        print(self.data_names, self.columns)
        # Plot all plots
        for ind1, name in enumerate(self.data_names):
            print('\n---' + name + '---' + '\n', self.frames_plt[name])
            self.axes[ind1].set_title(label=name,
                                      fontdict=self.font_title,
                                      loc=loc)
            # Draw all bar and stock them inside a dict to access right data
            #
            temp = {col: self.axes[ind1].bar(self.frames_plt[name].index.values,
                                             self.frames_plt[name][col].values,
                                             color=self.colors[col],
                                             width=self.width) for col in self.frames_plt[name].columns}
            # Draw a line at the top of each "Boiler_Energy" barplots
            tops = ([(el.get_x(), el.get_x()+temp[self.emph][0].get_width()),
                     (el.get_height(),)*2] for el in temp[self.emph])
            # Add lines to see emphase on all samples
            for top in tops:
                l = matplotlib.lines.Line2D(*top,
                                            linewidth=3,
                                            color=self.colors[self.emph])
                self.axes[ind1].add_line(l)
            # Set axe parameters
            self.axes[ind1].set_ylabel("Energie en Kwh", labelpad=20)
            self.axes[ind1].set_xlim(self.width, len(self.names)+1)
            self.axes[ind1].set_xticks(arange(1.5-(1-self.width)/2,
                                              len(self.names)+1.5-(1-self.width)/2,
                                              1))
            self.axes[ind1].set_xticklabels(self.names)
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
    lyon = FOLDER / "clean/chambery_26062014.csv"

    title = ["Evolution mensuel des apports et consommations d'énergie (en KWh)",
             "Diagrammes d'énergie"]

    # Color dict which must match all plots columns
    colors1 = {"Boiler_Energy": "#dc322f", "Radiator_Energy": "#fdf6e3",
               "DrawingUp_Energy": "#268bd2", "Collector_Energy": "orange",
               "Pertes": '#cb4b16'}
    colors2 = ["#dc322f", "#fdf6e3", "#268bd2", "orange", '#cb4b16']

    fields = ["Collector_Energy", "Boiler_Energy", "Radiator_Energy", "DrawingUp_Energy"]
    names = {"Radiator_Energy", "DrawingUp_Energy", "Pertes"}

    # Read all csv and store values as a dict
    frames = read_csv((chambery, marseille, strasbourg, lyon),
                      convert_index=(convert_to_datetime,)*10,
                      delimiter=(";",)*10,
                      index_col=("Date",)*10,
                      in_conv_index=(None,)*10,
                      skiprows=(1,)*10,
                      splitters=("_",)*10)

    # Resample each dataframes to keep only one value each 30min
    # Reduce data treatment and increase speed
    for frame in frames:
        frames[frame] = frames[frame][:].resample('30min').interpolate()

    DiagEnergy = EnergyDiagPlotter(frames, title[1], blocs=fields,
                                   radius=0.5, explode=(0.1, 0, 0),
                                   colors=colors2, plane=4).draw()
    HistEnergy = EnergyHistPlotter(frames, title[0], blocs=fields,
                                   colors=colors1, width=0.5).draw()
