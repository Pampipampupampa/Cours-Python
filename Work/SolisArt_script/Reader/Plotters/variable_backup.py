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

class VarBackPlotter(Plotter):

    """
        Variables and backup plotter
    """

    style = {'Vextra_state': '--', 'ECS_state': '-', 'CHAUFF_state': '-'}

    def __init__(self, frames, title):
        super().__init__(frame=frames, title=title)
        self.frame_var = self.frame["variables_algo_clean"]
        self.frame_backup = self.frame["backup_algo_clean"]

    def plotting_shape(self):
        self.ax11 = self.fig.add_subplot(3, 2, 1)
        self.ax12 = self.fig.add_subplot(3, 2, 3, sharex=self.ax11)
        self.ax13 = self.fig.add_subplot(3, 2, 5, sharex=self.ax11)

        self.ax21 = self.fig.add_subplot(3, 2, 2)
        self.ax22 = self.fig.add_subplot(3, 2, 4, sharex=self.ax21)
        self.ax23 = self.fig.add_subplot(3, 2, 6, sharex=self.ax21)
        self.ax11.set_title(label="Algorithme de controle de DTeco et Tconsigne solaire",
                            fontdict=font_title)
        self.ax21.set_title(label="Algorithme de controle de la mise en route de l'appoint",
                            fontdict=font_title)

    def plotting(self):
        # First column
        self.frame_var[['T1', 'T7',
                        'T9']].plot(ax=self.ax11,
                                    color=('#cb4b16',
                                           '#859900',
                                           '#268bd2'),
                                    ylim=(-10, 120),
                                    linewidth=self.width)
        self.ax11.legend(loc='best', ncol=3)
        self.frame_var[['T1_state']].plot(ax=self.ax12,
                                          colormap=self.colormap,
                                          ylim=(-1, 120),
                                          linewidth=self.width)
        self.frame_var['Tsolaire'].plot(ax=self.ax13,
                                        color='#cb4b16',
                                        ylim=(20, 25),
                                        linewidth=self.width)
        self.ax13.legend(loc='upper left')
        self.ax13_bis = self.ax13.twinx()
        self.frame_var['DTeco'].plot(ax=self.ax13_bis,
                                     color='#859900',
                                     ylim=(-0.1, 0.5),
                                     linewidth=self.width)
        self.ax13_bis.legend(loc='upper right')

        # Second column
        self.frame_backup['T8'].plot(ax=self.ax21, color='#cb4b16',
                                     ylim=(10, 50), linewidth=self.width)
        self.ax21_bis = self.ax21.twinx()
        self.frame_backup.ix[:, 'CHAUFF_state':
                                'Vextra_state'].plot(ax=self.ax21_bis,
                                                     colormap=self.colormap,
                                                     ylim=(-1, 120),
                                                     linewidth=self.width)
        self.ax21.legend(loc='upper left')
        self.ax21_bis.legend(loc='upper right', ncol=3)

        self.frame_backup[['T8_state',
                           'Or_state']].plot(ax=self.ax22,
                                             colormap=self.colormap,
                                             ylim=(-1, 120),
                                             linewidth=self.width)

        self.frame_backup[['Backup_state']].plot(ax=self.ax23,
                                                 colormap=self.colormap,
                                                 ylim=(-1, 120),
                                                 linewidth=self.width)

    def formatting(self):
        # Color match between yaxis and lines
        for ytics in self.ax13_bis.get_yticklabels():
            ytics.set_color(self.ax13_bis.lines[0].get_color())

        for ytics in self.ax21.get_yticklabels():
            ytics.set_color(self.ax21.lines[0].get_color())

        for ytics in self.ax13.get_yticklabels():
            ytics.set_color(self.ax13.lines[0].get_color())

        # Formatting
        self.ax11.xaxis.set_major_formatter(minutes_formatter)
        self.ax21.xaxis.set_major_formatter(minutes_formatter)

        # Adding y axes labels with colors
        self.ax11.set_ylabel('°C')
        self.ax13.set_ylabel('°C')
        self.ax21.set_ylabel('°C',
                             color=self.ax21.lines[0].get_color())
        self.ax13_bis.set_ylabel('°C',
                                 color=self.ax13_bis.lines[0].get_color())
        self.ax13.set_ylabel('°C',
                             color=self.ax13.lines[0].get_color())

    def text(self):
        # Add ylabel legend
        text = ("T1_state =  T1 >= T7 + 5 - 15*DTeco",
                "Tsolaire = Tconsigne + 3 - (Text_mini+Text)/18",
                "DTeco = Si T1_state alors 0.3 sinon 0",
                "T8_state =  T8 <= 30",
                "Or_state = (T8_state and CHAUFF_state) or ECS_state",
                "Backup_state = Or_state and Vextra_state")
        plt.text(0.1, -0.5, text[0]+"\n"+text[1]+"\n"+text[2],
                 horizontalalignment='left', verticalalignment='center',
                 transform=self.ax13.transAxes)
        plt.text(0.1, -0.5, text[3]+"\n"+text[4]+"\n"+text[5],
                 horizontalalignment='left', verticalalignment='center',
                 transform=self.ax23.transAxes)

########################
#### Main Program : ####
########################


if __name__ == '__main__':
    variable = FOLDER + "Issues\\Algo\\variables_algo_clean.csv"
    backup = FOLDER + "Issues\\Algo\\backup_algo_clean.csv"
    title = "Algorithme déterminant la consigne solaire et le besoin en appoint"
    frames = read_csv((variable, backup), convert_index=(convert_to_datetime,
                                                         convert_to_datetime),
                      delimiter=(";", ";"), index_col=("Date", "Date"),
                      in_conv_index=(None, None), skiprows=(1, 1))
    print(frames.keys())
    # bug issue : bad date formatting and length mismatch
    frames["variables_algo_clean"] = frames["variables_algo_clean"].ix[:-1, :][:]
    frames["backup_algo_clean"].index = frames["variables_algo_clean"].index

    VarBackPlotter(frames, title=title).draw()
