#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""Problème avec le partage d'axe pour l'axe 21"""

########################################
#### Classes and Methods imported : ####
########################################


from parameters import *


#######################################
#### Classes, Methods, Functions : ####
#######################################

class S4Plotter(Plotter):

    """
        Pump S4 plotter
    """

    def __init__(self, frame, title):
        super().__init__(frame=frame, title=title)

    def plotting_shape(self):
        # Drawing graphs
        self.ax11 = self.fig.add_subplot(3, 2, 1)
        self.ax12 = self.fig.add_subplot(3, 2, 3, sharex=self.ax11)
        self.ax13 = self.fig.add_subplot(3, 2, 5, sharex=self.ax11)

        self.ax21 = self.fig.add_subplot(3, 2, 2)
        self.ax22 = self.fig.add_subplot(3, 2, 4, sharex=self.ax11)
        self.ax23 = self.fig.add_subplot(3, 2, 6, sharex=self.ax11)

        # Change title parameters
        self.ax11.set_title(label="Algorithme de controle de S4 : Circuit Off",
                            fontdict=font_title)
        self.ax21.set_title(label="Algorithme de controle de S4 : Circuit On",
                            fontdict=font_title)

    def plotting(self):
        # First column
        self.frame[['T1', 'T3', 'T4']].plot(ax=self.ax11,
                                            color=('#cb4b16', '#859900', '#268bd2'),
                                            ylim=(-1, 140), linewidth=3)
        self.ax11.legend(loc='upper left')
        self.frame[['Off1_state', 'Off2_state']].plot(ax=self.ax12,
                                                      colormap='Accent',
                                                      ylim=(-1, 120),
                                                      linewidth=3)
        self.frame.ix[:, 'Other_off_state':'ECS_state'].plot(ax=self.ax13,
                                                             colormap='Accent',
                                                             ylim=(-1, 120),
                                                             linewidth=3)

        # Second column
        self.frame['Flow_S4'].plot(ax=self.ax21, color='#cb4b16',
                                   ylim=(-20, 20), linewidth=3)
        self.ax21.legend(loc='upper left')
        self.ax21_bis = self.ax21.twinx()
        self.frame['DeltaT_1-4'].plot(ax=self.ax21_bis, color='#859900',
                                      ylim=(-20, 30), linewidth=3)
        self.ax21_bis.legend(loc='upper right')

        self.frame.ix[:, 'S4_flow_state':'Vextra_state'].plot(ax=self.ax22,
                                                              colormap='Accent',
                                                              ylim=(-1, 120),
                                                              linewidth=3)

        self.frame[['On_state', 'S4_state']].plot(ax=self.ax23,
                                                  colormap='Accent',
                                                  ylim=(-1, 120), linewidth=3)

        def formatting(self):
            # Color match between yaxis and lines
            for ytics in self.ax21_bis.get_yticklabels():
                ytics.set_color(self.ax21_bis.lines[0].get_color())

            # Formatting
            self.ax11.xaxis.set_major_formatter(minutes_formatter)
            self.ax21.xaxis.set_major_formatter(minutes_formatter)

            # Adding y axes labels with colors
            self.ax11.set_ylabel('°C')
            self.ax21.set_ylabel('litre/min')
            self.ax21_bis.set_ylabel('°C',
                                     color=self.ax21_bis.lines[0].get_color())

        def artist(self):
            self.ax23.annotate("S4 reste active\nsans conditions d'arrêt",
                               xy=('2014-01-01 00:02:00',
                                   self.frame["S4_state"]['2014-01-01 00:03:00']),
                               xycoords='data', xytext=(50, -30),
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
            # Active if on conditions and no off conditions
            self.ax23.annotate("S4 actif si conditions d'activations\n" +
                               "et aucunes conditions de mise à l'arrêt",
                               xy=('2014-01-01 00:011:30',
                                   self.frame["S4_state"]['2014-01-01 00:11:30']),
                               xycoords='data', xytext=(20, -30),
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

########################
#### Main Program : ####
########################


if __name__ == '__main__':
    S4 = FOLDER + "Issues\\Algo\\S4_algo_ECS_clean.csv"
    title = "Algorithme de controle de la pompe S4"
    frames = read_csv((S4,), convert_index=(convert_to_datetime,))
    S4Plotter(frames["S4_algo_ECS_clean"], title=title).draw()
