#! /usr/bin/env python
# -*- coding:Utf8 -*-


########################################
#### Classes and Methods imported : ####
########################################

import numpy as np

try:
    from .parameters import *
except SystemError as e:
    print("Local import")
    from parameters import *


#######################################
#### Classes, Methods, Functions : ####
#######################################


class PumpAlgoPlotter(Plotter):

    """
        Pump algo plotter
    """

    style = {'Vextra_state': "k:", 'Pump_nb_solar': '-',
             'Pump_nb_heating': "-", 'Flow_Solar': "--",
             'Flow_Heating': "--", 'Flow_S6_out': "-",
             'Flow_S5_out': "-", 'Flow_S4_out': "-",
             'Flow_S1_out': "-", 'Flow_S2_out': "-",
             'Flow_S3_out': "-", 'S6_state': "-",
             'S5_state': "-", 'S4_state': "-", 'S1_state': "-",
             'S2_state': "-", 'S3_state': "--",
             }

    def __init__(self, frame, title):
        super().__init__(frame=frame, title=title)
        self.frame_plt = self.frame["algo_flow_mod_01_clean"]
        self.conds = {'Vextra': np.where(self.frame_plt['Vextra_state'] > 1),
                      'mod_S5': np.where(self.frame_plt['Flow_S5_out'] == 45/2),
                      'mod_S6': np.where(self.frame_plt['Flow_S6_out'] == 30),
                      'temp_S2': self.frame_plt.index[np.where(self.frame_plt['Flow_S2_out'] < 1)]}

    def plotting_shape(self):
        # Drawing graphs
        self.ax11 = self.fig.add_subplot(3, 2, 1)
        self.ax12 = self.fig.add_subplot(3, 2, 3, sharex=self.ax11)
        self.ax13 = self.fig.add_subplot(3, 2, 5, sharex=self.ax11)
        self.ax21 = self.fig.add_subplot(3, 2, 2)
        self.ax22 = self.fig.add_subplot(3, 2, 4, sharex=self.ax21)
        self.ax23 = self.fig.add_subplot(3, 2, 6, sharex=self.ax21)

        # Change title parameters
        self.ax11.set_title(label="Evolution du débit des pompes solaires",
                            fontdict=font_title)
        self.ax21.set_title(label="Evolution du débit des pompes de chauffage",
                            fontdict=font_title)

    def plotting(self):
        # First column
        self.frame_plt[['Flow_Solar',
                        'Vextra_state']].plot(ax=self.ax11,
                                              color=('#cb4b16', '#859900'),
                                              ylim=(0, 120), linewidth=self.width)
        self.ax11.legend(loc='upper left')
        self.ax11_bis = self.ax11.twinx()
        self.frame_plt['Pump_nb_solar'].plot(ax=self.ax11_bis,
                                             color='#268bd2', ylim=(0, 6),
                                             linewidth=self.width)
        self.ax11_bis.legend(loc='upper right')
        self.frame_plt.ix[:, 'S6_state':'S5_state'].plot(ax=self.ax12,
                                                         colormap='Accent',
                                                         style=self.style,
                                                         ylim=(0, 130),
                                                         linewidth=self.width)
        self.frame_plt.ix[:, 'Flow_S6_out':'Flow_S5_out'].plot(ax=self.ax13,
                                                               colormap='Accent',
                                                               style=self.style,
                                                               ylim=(0, 80),
                                                               linewidth=self.width)
        # Second column
        self.frame_plt[['Flow_Heating',
                        'Vextra_state']].plot(ax=self.ax21,
                                              color=('#CB4B16', '#859900'),
                                              ylim=(0, 120), linewidth=self.width)
        self.ax21.legend(loc='upper left')
        self.ax21_bis = self.ax21.twinx()
        self.frame_plt['Pump_nb_heating'].plot(ax=self.ax21_bis, color='#268BD2',
                                               ylim=(0, 6), linewidth=self.width)
        self.ax21_bis.legend(loc='upper right')
        self.frame_plt.ix[:, 'S4_state':'S3_state'].plot(ax=self.ax22,
                                                         colormap='Accent',
                                                         style=self.style,
                                                         ylim=(0, 130),
                                                         linewidth=self.width)
        self.frame_plt.ix[:, 'Flow_S4_out':'Flow_S3_out'].plot(ax=self.ax23,
                                                               colormap='Accent',
                                                               style=self.style,
                                                               ylim=(0, 100),
                                                               linewidth=self.width)

    def formatting(self):
        # Color match between yaxis and lines
        for ytics in self.ax11_bis.get_yticklabels():
            ytics.set_color(self.ax11_bis.lines[0].get_color())
        for ytics in self.ax21_bis.get_yticklabels():
            ytics.set_color(self.ax21_bis.lines[0].get_color())

        # Change x major ticks
        self.ax11.xaxis.set_major_formatter(minutes_formatter)
        self.ax21.xaxis.set_major_formatter(minutes_formatter)

        # Adding y axes labels with colors
        self.ax11.set_ylabel('litre/min',
                             color=self.ax11.lines[0].get_color())
        self.ax21.set_ylabel('litre/min',
                             color=self.ax21.lines[0].get_color())
        self.ax13.set_ylabel('litre/min')
        self.ax23.set_ylabel('litre/min')

    def artist(self):
      # Max flow and nb_pumps
        self.ax11.annotate("Max 'Flow_Solar'",
                           xy=('2014-01-01 00:02:00',
                               self.frame_plt['Flow_Solar']['2014-01-01 00:02:00']),
                           xycoords='data', xytext=(0, 20),
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
        self.ax11_bis.annotate("Mini 'Pump_nb_solar'",
                               xy=('2014-01-01 00:02:00',
                                   self.frame_plt['Pump_nb_solar']['2014-01-01 00:02:00']),
                               xycoords='data', xytext=(0, -20),
                               textcoords='offset points',
                               size=10, va="center", ha="center",
                               bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9),
                                         ec="none"),
                               arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                               fc=(0.84, 0.89, 0.9), ec="none",
                                               patchA=el,
                                               relpos=(0.8, 0.5),
                                               )
                               )

        # Extra valve switch
        self.ax11.annotate("Ouvert vers appoint",
                           xy=(self.frame_plt.index[self.conds['Vextra'][0][0]],
                               self.frame_plt['Vextra_state'][self.frame_plt.index[self.conds['Vextra'][0][0]]]),
                           xycoords='data', xytext=(50, 20),
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
        self.ax21.annotate("Ouvert vers appoint",
                           xy=(self.frame_plt.index[self.conds['Vextra'][0][0]],
                               self.frame_plt['Vextra_state'][self.frame_plt.index[self.conds['Vextra'][0][0]]]),
                           xycoords='data', xytext=(50, 20),
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

        # Modulation
        self.ax13.annotate("S5 : 50%",
                           xy=(self.frame_plt.index[self.conds['mod_S5'][0][1]],
                               self.frame_plt['Flow_S5_out'][self.frame_plt.index[self.conds['mod_S5'][0][1]]]),
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
        self.ax13.annotate("S6 : 50%",
                           xy=(self.frame_plt.index[self.conds['mod_S6'][0][1]],
                               self.frame_plt['Flow_S6_out'][self.conds['mod_S6'][0][1]]),
                           xycoords='data', xytext=(80, 20),
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

        # Temporization
        self.ax22.annotate("S2 : demande d'activation",
                           xy=(self.conds['temp_S2'][2],
                               self.frame_plt['S2_state'][self.conds['temp_S2'][2]]),
                           xycoords='data', xytext=(110, 30),
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
        self.ax23.annotate("S2 : temporisation",
                           xy=(self.conds['temp_S2'][2],
                               self.frame_plt['Flow_S2_out'][self.conds['temp_S2'][2]]),
                           xycoords='data', xytext=(80, 30),
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


########################
#### Main Program : ####
########################


if __name__ == '__main__':
    algo_pump = FOLDER + "Issues\\Algo_flow\\algo_flow_mod_01_clean.csv"
    title = "Fonctionnement de l'algorithme de controle du débit des pompes"
    frames = read_csv((algo_pump,), convert_index=(convert_to_datetime,))
    PumpAlgoPlotter(frames, title=title).draw()
