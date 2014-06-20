#! /usr/bin/env python
# -*- coding:Utf8 -*-


########################################
#### Classes and Methods imported : ####
########################################


try:
    from .parameters import *
except SystemError as e:
    print("Local import")
    from parameters import *


#######################################
#### Classes, Methods, Functions : ####
#######################################


class ChauffPlotter(Plotter):

    """
        Chauff state plotter
    """

    def __init__(self, frame, title):
        super().__init__(frame=frame, title=title)
        self.frame_plt = self.frame["Chauff_algo_clean"]

    def plotting_shape(self):
        # Create Axes instance to plot in
        self.ax11 = self.fig.add_subplot(3, 2, 1)
        self.ax11.set_title(label="Control en zone 1",
                            fontdict=font_title)
        self.ax12 = self.fig.add_subplot(3, 2, 3, sharex=self.ax11)  # sharex allow to share x axis for all actions
        self.ax13 = self.fig.add_subplot(3, 2, 5, sharex=self.ax11)

        self.ax21 = self.fig.add_subplot(3, 2, 2)
        self.ax21.set_title(label="Control en zone 2",
                            fontdict=font_title)
        self.ax22 = self.fig.add_subplot(3, 2, 4, sharex=self.ax21)
        self.ax23 = self.fig.add_subplot(3, 2, 6, sharex=self.ax21)

    def plotting(self):
        # First column
        self.frame_plt[['T12_1', 'compare1']].plot(ax=self.ax11, colormap='Accent',
                                                   ylim=(-10, 120), linewidth=self.width)
        self.ax11.legend(loc='upper left')
        self.ax11_bis = self.ax11.twinx()
        self.frame_plt['DTeco'].plot(ax=self.ax11_bis, color='#cb4b16',
                                     ylim=(-0.1, 0.5), linewidth=self.width)
        self.ax11_bis.legend(loc='upper right', ncol=1)
        self.frame_plt['T12_1_state'].plot(ax=self.ax12,
                                           colormap='Accent',
                                           ylim=(-10, 120),
                                           linewidth=self.width)
        self.ax12.legend(loc='upper left')
        self.ax12_bis = self.ax12.twinx()
        self.frame_plt['ECS_state'].plot(ax=self.ax12_bis, color='#cb4b16',
                                         ylim=(-10, 120), linewidth=self.width)
        self.ax12_bis.legend(loc='upper right', ncol=1)

        self.frame_plt[['CHAUFF_1_state']].plot(ax=self.ax13, colormap='Accent',
                                                ylim=(-10, 120),
                                                linewidth=self.width)

        # Second column
        self.frame_plt[['T12_2', 'compare2']].plot(ax=self.ax21,
                                                   colormap='Accent',
                                                   ylim=(-10, 120),
                                                   linewidth=self.width)
        self.ax21.legend(loc='upper left')
        self.ax21_bis = self.ax21.twinx()
        self.frame_plt['DTeco'].plot(ax=self.ax21_bis, color='#cb4b16',
                                     ylim=(-0.1, 0.5), linewidth=self.width)
        self.ax21_bis.legend(loc='upper right', ncol=1)
        self.frame_plt['T12_2_state'].plot(ax=self.ax22,
                                           colormap='Accent',
                                           ylim=(-10, 120),
                                           linewidth=self.width)
        self.ax22.legend(loc='upper left')
        self.ax22_bis = self.ax22.twinx()
        self.frame_plt['ECS_state'].plot(ax=self.ax22_bis, color='#cb4b16',
                                         ylim=(-10, 120), linewidth=self.width)
        self.ax22_bis.legend(loc='upper right', ncol=1)

        self.frame_plt[['CHAUFF_2_state']].plot(ax=self.ax23, colormap='Accent',
                                                ylim=(-10, 120),
                                                linewidth=self.width)

    def formatting(self):
        # Color match between yaxis and lines
        for ytics in self.ax11_bis.get_yticklabels():
            ytics.set_color(self.ax11_bis.lines[0].get_color())
        for ytics in self.ax21_bis.get_yticklabels():
            ytics.set_color(self.ax21_bis.lines[0].get_color())
        for ytics in self.ax12_bis.get_yticklabels():
            ytics.set_color(self.ax12_bis.lines[0].get_color())
        for ytics in self.ax22_bis.get_yticklabels():
            ytics.set_color(self.ax22_bis.lines[0].get_color())

        # Formatting
        self.ax11.xaxis.set_major_formatter(minutes_formatter)
        self.ax21.xaxis.set_major_formatter(minutes_formatter)

        # Adding y axes labels with colors
        self.ax11.set_ylabel('°C')
        self.ax21.set_ylabel('°C')
        self.ax11_bis.set_ylabel('°C',
                                 color=self.ax11_bis.lines[0].get_color())
        self.ax21_bis.set_ylabel('°C',
                                 color=self.ax21_bis.lines[0].get_color())

    def text(self):
        # Add ylabel legend
        text = ("compare1 = T12_1 < Tconsigne1(=20°C) - DTeco + CHAUFF_1_state/4",
                "compare2 = T12_2 < Tconsigne2(=20°C) - DTeco + CHAUFF_2_state/4")
        plt.text(0.5, -0.5, text[0], horizontalalignment='center',
                 verticalalignment='center', transform=self.ax13.transAxes)
        plt.text(0.5, -0.5, text[1], horizontalalignment='center',
                 verticalalignment='center', transform=self.ax23.transAxes)


########################
#### Main Program : ####
########################

if __name__ == '__main__':
    chauff = FOLDER + "Issues\\Algo\\Chauff_algo_clean.csv"
    title = "Algorithme de controle de la variable Chauff"
    frames = read_csv((chauff,), convert_index=(convert_to_datetime,))
    ChauffPlotter(frames, title=title).draw()
