#! /usr/bin/env python
# -*- coding:Utf8 -*-


########################################
#### Classes and Methods imported : ####
########################################

import matplotlib.gridspec as gridspec

from parameters import *

#######################################
#### Classes, Methods, Functions : ####
#######################################


class HousePlotter(Plotter):

    """
        House plotter
    """

    def __init__(self, frame, title):
        super().__init__(frame=frame, title=title)

    def plotting_shape(self):
        self.G = gridspec.GridSpec(2, 2)

        # Drawing graphs
        self.ax11 = plt.subplot(self.G[0, :1])
        self.ax12 = plt.subplot(self.G[1, :1], sharex=self.ax11)
        self.ax13 = plt.subplot(self.G[:, 1:])

        # Change title parameters
        self.ax12.set_title(label="Evolution de la demande en chauffage au cours de l'année",
                            fontdict=font_title)
        self.ax11.set_title(label="Evolution des températures au cours de l'année",
                            fontdict=font_title)
        self.ax13.set_title(label="Evolution de l'énergie au cours de l'année",
                            fontdict=font_title)

    def plotting(self):
        self.frame['House_Energy'].plot(ax=self.ax13, colormap="Accent",
                                        linewidth=5, linestyle="-")
        self.frame['House_Power'].plot(ax=self.ax12, colormap="Accent",
                                       linewidth=2, linestyle="-",
                                       ylim=(-1, 5000))
        self.frame[['T12_house', 'T12_rad_house',
                    'T9_ext']].plot(ax=self.ax11, colormap="Accent",
                                    linewidth=2, linestyle="-")

    def formatting(self):
        self.ax11.set_ylabel('°C')
        self.ax12.set_ylabel('W')
        self.ax13.set_ylabel('KWh')

    def artist(self):
        ax13_text1 = "Energie consommée : " + \
                     "{1:.0f} kWh \n{0:%Y-%m-%d}".format(self.frame.idxmax(axis=0)["House_Energy"],
                                                         self.frame.max(axis=0)["House_Energy"])
        ax13_text2 = "Energie consommée : " + \
                     "{1:.0f} kWh \n{0}".format("2014-05-19",
                                                self.frame["House_Energy"]["2014-05-19 9:00:00"])
        ax13_text3 = "Energie consommée : " + \
                     "{1:.0f} kWh \n{0}".format("2014-10-01",
                                                self.frame["House_Energy"]["2014-10-01 9:00:00"])
        self.ax13.annotate(ax13_text1,
                           xy=(self.frame.idxmax(axis=0)["House_Energy"],
                               self.frame.max(axis=0)["House_Energy"]),
                           xycoords='data', xytext=(-150, 50), ha="center",
                           textcoords='offset points', size=10, va="center",
                           bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9),
                                     ec="none"),
                           arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                           fc=(0.84, 0.89, 0.9), ec="none",
                                           patchA=el,
                                           relpos=(0.2, 0.5),
                                           )
                           )
        self.ax13.annotate(ax13_text2,
                           xy=("2014-05-19 9:00:00",
                               self.frame["House_Energy"]["2014-05-19 9:00:00"]),
                           xycoords='data', xytext=(-50, 50), ha="center",
                           textcoords='offset points', size=10, va="center",
                           bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9),
                                     ec="none"),
                           arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                           fc=(0.84, 0.89, 0.9), ec="none",
                                           patchA=el,
                                           relpos=(0.2, 0.5),
                                           )
                           )
        self.ax13.annotate(ax13_text3,
                           xy=("2014-10-01 9:00:00",
                               self.frame["House_Energy"]["2014-10-01 9:00:00"]),
                           xycoords='data', xytext=(-50, -50),
                           textcoords='offset points', ha="center",
                           size=10, va="center",
                           bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9),
                                     ec="none"),
                           arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                           fc=(0.84, 0.89, 0.9), ec="none",
                                           patchA=el,
                                           relpos=(0.2, 0.5),
                                           )
                           )


########################
#### Main Program : ####
########################


if __name__ == '__main__':
    house = FOLDER + "clean\\olivier_house_read.csv"
    title = "Evolution des principaux paramètres caractéristiques du bâtiment"
    frames = read_csv((house,), convert_index=(convert_to_datetime,))
    frames["olivier_house_read"] = frames["olivier_house_read"][:].resample('60min')
    HousePlotter(frames["olivier_house_read"], title=title).draw()
