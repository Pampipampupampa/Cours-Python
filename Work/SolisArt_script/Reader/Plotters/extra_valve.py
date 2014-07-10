#! /usr/bin/env python
# -*- coding:Utf8 -*-


########################################
#### Classes and Methods imported : ####
########################################


import numpy as np

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


class ExtraValvePlotter(plotter.Plotter):

    """
        Pump algo plotter
    """

    style = {'T7': "--", 'T7_state': "--",
             'T4': "--", 'T4_state': "--"}

    def __init__(self, frames, title):
        super().__init__(frames=frames, title=title)
        self.frame_plt = self.frames["V3Vextra_algo_clean"]
        self.conds = {'on1': np.where(self.frame_plt['On1_state'] > 50)[0][0],
                      'on2': np.where(self.frame_plt['On2_state'] > 50)[0][0],
                      'on3': np.where(self.frame_plt['On3_state'] > 50)[0][0]}

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
        self.frame_plt[['T1', 'T4', 'T7',
                        'T12_house']].plot(ax=self.ax11,
                                           colormap=self.colormap,
                                           ylim=(0, 130),
                                           style=self.style,
                                           linewidth=self.width)
        self.frame_plt[['T1_state', 'T4_state', 'T7_state',
                        'T12_state']].plot(ax=self.ax12,
                                           colormap=self.colormap,
                                           style=self.style,
                                           ylim=(-1, 120), linewidth=self.width)
        self.frame_plt[['Vextra_state']].plot(ax=self.ax13,
                                              colormap=self.colormap,
                                              style=self.style,
                                              ylim=(-1, 120),
                                              linewidth=self.width)

        # Second column
        self.frame_plt.ix[:, 'ECS_state':'CHAUFF_state'].plot(ax=self.ax21,
                                                              colormap=self.colormap,
                                                              ylim=(0, 130),
                                                              linewidth=self.width)
        self.frame_plt[['On1_state', 'On2_state',
                        'On3_state']].plot(ax=self.ax22,
                                           colormap=self.colormap,
                                           style=self.style,
                                           ylim=(-1, 120),
                                           linewidth=self.width)
        self.frame_plt[['ECS_out_state',
                        'CHAUFF_out_state']].plot(ax=self.ax23,
                                                  colormap=self.colormap,
                                                  style=self.style,
                                                  ylim=(-1, 120),
                                                  linewidth=self.width)

    def formatting(self):
        # Change x major ticks
        self.ax11.xaxis.set_major_formatter(minutes_formatter)
        self.ax21.xaxis.set_major_formatter(minutes_formatter)

        # Adding y axes labels with colors
        self.ax11.set_ylabel('°C')

    def artist(self):
        # Extra valve annotations
        self.ax13.annotate("On1_state",
                           xy=(self.frame_plt.index[self.conds['on1']],
                               self.frame_plt['Vextra_state'][self.conds['on1']]),
                           xycoords='data', xytext=(60, -30),
                           textcoords='offset points',
                           size=10, va="center", ha="center",
                           bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9),
                                     ec="none"),
                           arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                           fc=(0.84, 0.89, 0.9), ec="none",
                                           patchA=el,
                                           relpos=(0.2, 0.5),
                                           )
                           )
        self.ax13.annotate("On2_state",
                           xy=(self.frame_plt.index[self.conds['on2']],
                               self.frame_plt['Vextra_state'][self.conds['on2']]),
                           xycoords='data', xytext=(60, -30),
                           textcoords='offset points',
                           size=10, va="center", ha="center",
                           bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9),
                                     ec="none"),
                           horizontalalignment='right',
                           verticalalignment='bottom',
                           arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                           fc=(0.84, 0.89, 0.9), ec="none",
                                           patchA=el,
                                           relpos=(0.2, 0.5),
                                           )
                           )
        self.ax13.annotate("On3_state",
                           xy=(self.frame_plt.index[self.conds['on3']],
                               self.frame_plt['Vextra_state'][self.conds['on3']]),
                           xycoords='data', xytext=(60, -30),
                           textcoords='offset points',
                           size=10, va="center", ha="center",
                           bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9),
                                     ec="none"),
                           horizontalalignment='right',
                           verticalalignment='bottom',
                           arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                           fc=(0.84, 0.89, 0.9), ec="none",
                                           patchA=el,
                                           relpos=(0.2, 0.5),
                                           )
                           )
        # ECS annotations
        self.ax23.annotate("Force ECS off (On2_state)",
                           xy=(self.frame_plt.index[self.conds['on2']],
                               self.frame_plt['ECS_out_state'][self.conds['on2']]),
                           xycoords='data', xytext=(60, 30),
                           textcoords='offset points',
                           size=10, va="center", ha="center",
                           bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9),
                                     ec="none"),
                           horizontalalignment='right',
                           verticalalignment='bottom',
                           arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                           fc=(0.84, 0.89, 0.9), ec="none",
                                           patchA=el,
                                           relpos=(0.2, 0.5),
                                           )
                           )
        # CHAUFF annotations
        self.ax23.annotate("Force CHAUFF off (On3_state)",
                           xy=(self.frame_plt.index[self.conds['on3']],
                               self.frame_plt['CHAUFF_out_state'][self.conds['on3']]),
                           xycoords='data', xytext=(60, 30),
                           textcoords='offset points',
                           size=10, va="center", ha="center",
                           bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9),
                                     ec="none"),
                           horizontalalignment='right',
                           verticalalignment='bottom',
                           arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                           fc=(0.84, 0.89, 0.9), ec="none",
                                           patchA=el,
                                           relpos=(0.2, 0.5),
                                           )
                           )

    def text(self):
        text1 = ("T1_state = T1 > T4 + 11 - 8*Vextra_state",
                 "T4_state = T4 >= 55 - Vextra_state",
                 "T7_state = T1 >= T7 + 10",
                 "T12_state = T12 > Tconsigne_solaire - 0.1",
                 "Tconsigne_solaire = Tconsigne(20°C) + 3 - (Text_mini + Text)/18",
                 "Vextra_state = On1_state or On2_state or On3_state")
        plt.text(0.1, -0.5, text1[0]+"\n"+text1[1]+"\n"+text1[2]+"\n"+text1[3]+"\n"+text1[4]+"\n"+text1[5],
                 horizontalalignment='left', verticalalignment='center',
                 transform=self.ax13.transAxes)
        text2 = ("On1_state = not(ECS_state) and not(CHAUFF_state)",
                 "On2_state = ECS_state and T1_state and T4_state",
                 "On3_state = not(ECS_state) and CHAUFF_state and T7_state and T12_state",
                 "ECS_out_state = Si On2_state alors 0 sinon ECS_state",
                 "CHAUFF_out_state = Si On3_state alors 0 sinon CHAUFF_state")
        plt.text(0.1, -0.5, text2[0]+"\n"+text2[1]+"\n"+text2[2]+"\n"+text2[3]+"\n"+text2[4],
                 horizontalalignment='left', verticalalignment='center',
                 transform=self.ax23.transAxes)

########################
#### Main Program : ####
########################


if __name__ == '__main__':
    extra_valve = FOLDER / "Issues/Algo/V3Vextra_algo_clean.csv"
    title = "Contrôle de la vanne d'appoint"
    frames = read_csv((extra_valve,), convert_index=(convert_to_datetime,))
    ExtraValvePlotter(frames, title=title).draw()
