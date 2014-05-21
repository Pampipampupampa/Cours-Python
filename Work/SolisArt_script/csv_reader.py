#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""

    Some useful reader examples

"""

########################################
#### Classes and Methods imported : ####
########################################


import datetime
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# from matplotlib.patches import Ellipse  # Used to draw shapes inside plots

#######################################
#### Classes, Methods, Functions : ####
#######################################


def convert_to_datetime(step, start=datetime.datetime(2014, 1, 1)):
    """
      This parser convert to a real datetime format
    """
    for el in step:
        yield start + datetime.timedelta(seconds=int(el))


def printer(title="Algo : pump mass flow rate", size=(30, 18),
            bg=(0.84, 0.89, 0.9)):
    fig = plt.figure(figsize=size, facecolor=bg)
    fig.canvas.manager.set_window_title(title)
    return fig


def reader(csv_file, skiprows=1, delimiter=";", index_col="Date"):
    return pd.read_csv(csv_file, skiprows=skiprows, delimiter=delimiter,
                       index_col=index_col)


def algo_flow(csv_file, convert=True, sampling=None):
    if not convert and sampling is not None:
        raise 'Can only sample DatetimeData, please pass convert to True'
    # Your Dataframe structure
    pump_algo = reader(csv_file)
    if convert:
        pump_algo.index = [ind for ind in convert_to_datetime(pump_algo.index)]
    print(type(pump_algo.index))
    for i, col in enumerate(pump_algo.columns):
        print("column {} \t\t{}".format(i, col))
    if sampling:
        pump_algo = pump_algo[:].resample(sampling)
    # Adding fig instance
    fig = printer(title="Algo : pump mass flow rate")
    # Create Axes instance to plot in
    ax11 = fig.add_subplot(3, 2, 1)
    ax11.set_title(label="Evolution du débit des pompes solaires", fontdict=font_title)
    ax12 = fig.add_subplot(3, 2, 3, sharex=ax11)  # sharex allow to share x axis for all actions like zoom
    ax13 = fig.add_subplot(3, 2, 5, sharex=ax11)

    ax21 = fig.add_subplot(3, 2, 2)
    ax21.set_title(label="Evolution du débit des pompes de chauffage", fontdict=font_title)
    ax22 = fig.add_subplot(3, 2, 4, sharex=ax21)
    ax23 = fig.add_subplot(3, 2, 6, sharex=ax21)

    # Add plot in each axes
    # First plot
    flow_mini1 = pump_algo['Flow_Solar'].plot(ax=ax11, color='#cb4b16',
                                              ylim=(0, 120), linewidth=3)
    ax11_bis = ax11.twinx()
    state = pump_algo['Vextra_state'].plot(ax=ax11_bis, color='#859900',
                                           ylim=(0, 120), linewidth=3)
    ax11.legend(loc='upper left')
    ax11_bis.legend(loc='upper right')

    flow_mini2 = pump_algo['Flow_Heating'].plot(ax=ax21, color='#cb4b16',
                                                ylim=(0, 120), linewidth=3)
    ax21_bis = ax21.twinx()
    state = pump_algo['Vextra_state'].plot(ax=ax21_bis, color='#859900',
                                           ylim=(0, 120), linewidth=3)
    ax21.legend(loc='upper left')
    ax21_bis.legend(loc='upper right')

    # Second plot
    state1 = pump_algo.ix[:, 'S6_state':'S5_state'].plot(ax=ax12, colormap='Accent', style=style,
                                                         ylim=(0, 130), linewidth=3)
    state2 = pump_algo.ix[:, 'S1_state':'S3_state'].plot(ax=ax22, colormap='Accent', style=style,
                                                         ylim=(0, 130), linewidth=3)
    # Third plot
    flow_out1 = pump_algo.ix[:, 'Flow_S6_out':'Flow_S5_out'].plot(ax=ax13, colormap='Accent', style=style,
                                                                  ylim=(0, 80), linewidth=3)
    flow_out2 = pump_algo.ix[:, 'Flow_S1_out':'Flow_S3_out'].plot(ax=ax23, colormap='Accent', style=style,
                                                                  ylim=(0, 100), linewidth=3)

    # Avoid overlapping
    # ax11.set_xticklabels([""])
    # ax12.set_xticklabels([""])
    # ax13.set_xticklabels([""])
    # ax21.set_xticklabels([""])
    # ax22.set_xticklabels([""])
    # ax23.set_xticklabels([""])

    for tick in ax11.get_xticks():
        print(tick)

    # Update legend after all modifications
    ax12.legend(loc='best', ncol=2)
    ax22.legend(loc='best', ncol=3)

    plt.show()

########################
#### Main Program : ####
########################

folder = "C:\\Users\\bois\\Documents\\GitHub\\SolarSystem\\Outputs\\Issues\\Algo_flow"
pump_csv = folder + "\\algo_flow_mod_01_clean.csv"

style = {'Vextra_state': 'k:', 'Pump_nb_heating': '-',
         'Flow_Solar': '--', 'Flow_Heating': '--',
         'Flow_S6_out': '-', 'Flow_S5_out': '-', 'Flow_S4_out': '-',
         'Flow_S1_out': '-', 'Flow_S2_out': '-', 'Flow_S3_out': '-',
         'S6_state': '-', 'S5_state': '-', 'S4_state': '-',
         'S1_state': '-', 'S2_state': '-', 'S3_state': '--'}

# Change font properties
font_base = {'family': 'serif',
             'size': 15}
# Changing graphs' title parameters
font_title = {'family': 'serif',
              'size': 20}

# Change default label settings
matplotlib.rc('font', **font_base)  # Overwrite default fonts parameters
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)

algo_flow(csv_file=pump_csv)
