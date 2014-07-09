#! /usr/bin/env python
# -*- coding:Utf8 -*-


########################################
#### Classes and Methods imported : ####
########################################


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


class SolarValvePlotter(plotter.Plotter):

    """
        Pump algo plotter
    """

    def __init__(self, frames, title):
        super().__init__(frames=frames, title=title)
        self.frame_plt = self.frames["V3Vsolar_algo_clean"]

    def plotting_shape(self):
        # Drawing graphs
        self.ax11 = self.fig.add_subplot(3, 2, 1)
        self.ax12 = self.fig.add_subplot(3, 2, 3, sharex=self.ax11)
        self.ax13 = self.fig.add_subplot(3, 2, 5, sharex=self.ax11)

        self.ax21 = self.fig.add_subplot(3, 2, 2, sharex=self.ax11)
        self.ax22 = self.fig.add_subplot(3, 2, 4, sharex=self.ax11)
        self.ax23 = self.fig.add_subplot(3, 2, 6, sharex=self.ax11)

    def plotting(self):
        # First column
        self.frame_plt[['T1', 'T3']].plot(ax=self.ax11,
                                          colormap=self.colormap,
                                          ylim=(0, 130),
                                          linewidth=self.width)
        self.frame_plt[['compare1', 'compare2',
                        'compare3']].plot(ax=self.ax12,
                                          colormap=self.colormap,
                                          ylim=(-1, 130),
                                          linewidth=self.width)
        self.frame_plt[['On1_state', 'On2_state']].plot(ax=self.ax13,
                                                        colormap=self.colormap,
                                                        ylim=(-1, 130),
                                                        linewidth=self.width)
        # Second column
        self.frame_plt[['T4', 'T5']].plot(ax=self.ax21,
                                          colormap=self.colormap,
                                          ylim=(0, 130),
                                          linewidth=self.width)
        self.frame_plt[['compare2_state',
                        'compare3_state']].plot(ax=self.ax22,
                                                colormap=self.colormap,
                                                ylim=(0, 130),
                                                linewidth=self.width)
        self.frame_plt[['Vsolar_state']].plot(ax=self.ax23,
                                              colormap=self.colormap,
                                              ylim=(-1, 130),
                                              linewidth=self.width)

    def formatting(self):
        # Change x major ticks
        self.ax11.xaxis.set_major_formatter(minutes_formatter)
        self.ax21.xaxis.set_major_formatter(minutes_formatter)

        # Adding y axes labels with colors
        self.ax11.set_ylabel('°C')
        self.ax21.set_ylabel('°C')
        self.ax12.set_ylabel('°C')

    def text(self):
        text1 = ("compare1 = min(T3, T4) - 2*Vsolar_state",
                 "compare2 = T5 - 2*Vsolar_state",
                 "compare3 = 30 - 2*Vsolar_state")
        plt.text(0.1, -0.5, text1[0]+"\n"+text1[1]+"\n"+text1[2],
                 horizontalalignment='left', verticalalignment='center',
                 transform=self.ax13.transAxes)
        text2 = ("compare2_state = T1 > compare2",
                 "compare3_state = T3 >= compare3 ",
                 "On1_state = T1 >= compare1",
                 "On2_state = compare2_state and compare3_state")
        plt.text(0.1, -0.5, text2[0]+"\n"+text2[1]+"\n"+text2[2]+"\n"+text2[3],
                 horizontalalignment='left', verticalalignment='center',
                 transform=self.ax23.transAxes)

########################
#### Main Program : ####
########################


if __name__ == '__main__':
    solar_valve = FOLDER / "Issues/Algo/V3Vsolar_algo_clean.csv"
    title = "Contrôle de la vanne solaire"
    frames = read_csv((solar_valve,), convert_index=(convert_to_datetime,))
    SolarValvePlotter(frames, title=title).draw()
