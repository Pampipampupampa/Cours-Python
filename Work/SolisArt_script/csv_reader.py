#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""

    Some useful reader examples

"""

########################################
#### Classes and Methods imported : ####
########################################


import pandas as pd
import numpy as np
import datetime
import matplotlib
import matplotlib.pyplot as plt

# Used to draw shapes inside plots
from matplotlib.patches import Ellipse
# Used as tick label formatter
from matplotlib.dates import DateFormatter
from matplotlib.dates import MinuteLocator, SecondLocator


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


def artiste_house(ax11, ax12, ax13, house_data):
    # Adding value emphazing
    el = Ellipse((2, -1), 0.5, 0.5)
    ax13.add_patch(el)
    # Max
    ax13.annotate("Energie consommée : " +
                  "{1:.0f} kWh \n{0:%Y-%m-%d}".format(house_data.idxmax(axis=0)["House_Energy"],
                                                      house_data.max(axis=0)["House_Energy"]),
                  xy=(house_data.idxmax(axis=0)["House_Energy"],
                      house_data.max(axis=0)["House_Energy"]),
                  xycoords='data', xytext=(-150, 50), textcoords='offset points',
                  size=15, va="center", ha="center",
                  bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9), ec="none"),
                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                  fc=(0.84, 0.89, 0.9), ec="none",
                                  patchA=el,
                                  relpos=(0.2, 0.5),
                                  )
                  )
    # All solar use start
    ax13.annotate("Energie consommée : " +
                  "{1:.0f} kWh \n{0}".format("2014-05-19",
                                             house_data["House_Energy"]["2014-05-19 9:00:00"]),
                  xy=("2014-05-19 9:00:00",
                      house_data["House_Energy"]["2014-05-19 9:00:00"]),
                  xycoords='data', xytext=(-150, 50), textcoords='offset points',
                  size=15, va="center", ha="center",
                  bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9), ec="none"),
                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                  fc=(0.84, 0.89, 0.9), ec="none",
                                  patchA=el,
                                  relpos=(0.2, 0.5),
                                  )
                  )
    # All solar use end
    ax13.annotate("Energie consommée : " +
                  "{1:.0f} kWh \n{0}".format("2014-10-01",
                                             house_data["House_Energy"]["2014-10-01 9:00:00"]),
                  xy=("2014-10-01 9:00:00",
                      house_data["House_Energy"]["2014-10-01 9:00:00"]),
                  xycoords='data', xytext=(-150, 50), textcoords='offset points',
                  size=15, va="center", ha="center",
                  bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9), ec="none"),
                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                  fc=(0.84, 0.89, 0.9), ec="none",
                                  patchA=el,
                                  relpos=(0.2, 0.5),
                                  )
                  )


def artiste_pump_algo(ax11, ax11_bis, ax12, ax13, ax21, ax21_bis, ax22, ax23,
                      pump_algo):
    # Adding artist element
    el = Ellipse((2, -1), 0.5, 0.5)
    ax11.add_patch(el)
    ax21.add_patch(el)

    conds = {'Vextra': np.where(pump_algo['Vextra_state'] > 1),
             'mod_S5': np.where(pump_algo['Flow_S5_out'] == 45/2),
             'mod_S6': np.where(pump_algo['Flow_S6_out'] == 30),
             'temp_S2': pump_algo.index[np.where(pump_algo['Flow_S2_out'] < 1)]}

    # Max flow and nb_pumps
    ax11.annotate("Max 'Flow_Solar'",
                  xy=('2014-01-01 00:02:00',
                      pump_algo['Flow_Solar']['2014-01-01 00:02:00']),
                  xycoords='data', xytext=(0, 20), textcoords='offset points',
                  size=15, va="center", ha="center",
                  bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9), ec="none"),
                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                  fc=(0.84, 0.89, 0.9), ec="none",
                                  patchA=el,
                                  relpos=(0.2, 0.5),
                                  )
                  )
    ax11_bis.annotate("Mini 'Pump_nb_solar'",
                      xy=('2014-01-01 00:02:00',
                          pump_algo['Pump_nb_solar']['2014-01-01 00:02:00']),
                      xycoords='data', xytext=(0, -20),
                      textcoords='offset points',
                      size=15, va="center", ha="center",
                      bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9),
                                ec="none"),
                      arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                      fc=(0.84, 0.89, 0.9), ec="none",
                                      patchA=el,
                                      relpos=(0.8, 0.5),
                                      )
                      )

    # Extra valve switch
    ax11.annotate("Ouvert vers appoint",
                  xy=(pump_algo.index[conds['Vextra'][0][0]],
                      pump_algo['Vextra_state'][pump_algo.index[conds['Vextra'][0][0]]]),
                  xycoords='data', xytext=(50, 30), textcoords='offset points',
                  size=15, va="center", ha="center",
                  bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9), ec="none"),
                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                  fc=(0.84, 0.89, 0.9), ec="none",
                                  patchA=el,
                                  relpos=(0.2, 0.5),
                                  )
                  )
    ax21.annotate("Ouvert vers appoint",
                  xy=(pump_algo.index[conds['Vextra'][0][0]],
                      pump_algo['Vextra_state'][pump_algo.index[conds['Vextra'][0][0]]]),
                  xycoords='data', xytext=(50, 30), textcoords='offset points',
                  size=15, va="center", ha="center",
                  bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9), ec="none"),
                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                  fc=(0.84, 0.89, 0.9), ec="none",
                                  patchA=el,
                                  relpos=(0.2, 0.5),
                                  )
                  )

    # Modulation
    ax13.annotate("S5 : 50%",
                  xy=(pump_algo.index[conds['mod_S5'][0][1]],
                      pump_algo['Flow_S5_out'][pump_algo.index[conds['mod_S5'][0][1]]]),
                  xycoords='data', xytext=(50, -30), textcoords='offset points',
                  size=15, va="center", ha="center",
                  bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9), ec="none"),
                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                  fc=(0.84, 0.89, 0.9), ec="none",
                                  patchA=el,
                                  relpos=(0.2, 0.5),
                                  )
                  )
    ax13.annotate("S6 : 50%",
                  xy=(pump_algo.index[conds['mod_S6'][0][1]],
                      pump_algo['Flow_S6_out'][pump_algo.index[conds['mod_S6'][0][1]]]),
                  xycoords='data', xytext=(80, 30), textcoords='offset points',
                  size=15, va="center", ha="center",
                  bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9), ec="none"),
                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                  fc=(0.84, 0.89, 0.9), ec="none",
                                  patchA=el,
                                  relpos=(0.2, 0.5),
                                  )
                  )

    # Temporization
    ax22.annotate("S2 : demande d'activation",
                  xy=(conds['temp_S2'][2],
                      pump_algo['S2_state'][conds['temp_S2'][2]]),
                  xycoords='data', xytext=(110, 30), textcoords='offset points',
                  size=15, va="center", ha="center",
                  bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9), ec="none"),
                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                  fc=(0.84, 0.89, 0.9), ec="none",
                                  patchA=el,
                                  relpos=(0.2, 0.5),
                                  )
                  )
    ax23.annotate("S2 : temporisation",
                  xy=(conds['temp_S2'][2],
                      pump_algo['Flow_S2_out'][conds['temp_S2'][2]]),
                  xycoords='data', xytext=(80, 30), textcoords='offset points',
                  size=15, va="center", ha="center",
                  bbox=dict(boxstyle="round", fc=(0.84, 0.89, 0.9), ec="none"),
                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                  fc=(0.84, 0.89, 0.9), ec="none",
                                  patchA=el,
                                  relpos=(0.2, 0.5),
                                  )
                  )


def house(csv_file, convert=True, sampling='60min'):
    print("House reader")
    if not convert and sampling is not None:
        raise 'Can only sample DatetimeData, please pass convert to True'
    # Your Dataframe structure
    house_data = reader(csv_file)
    if convert:
        house_data.index = [ind for ind in convert_to_datetime(house_data.index)]
    print(type(house_data.index))
    for i, col in enumerate(house_data.columns):
        print("column {} \t\t{}".format(i, col))
    if sampling:
        house_data = house_data[:].resample(sampling)

    # Adding fig instance
    fig = printer(title="House Reader")

    # Drawing graphs
    ax11 = fig.add_axes([.02, 0.55, .52, .4])
    ax12 = fig.add_axes([.02, 0.05, .52, .4], sharex=ax11)
    ax13 = fig.add_axes([0.6, 0.05, 0.38, 0.9])

    # Change title parameters
    ax12.set_title(label="Evolution de la demande en chauffage au cours de l'année",
                   fontdict=font_title)
    ax11.set_title(label="Evolution des températures au cours de l'année",
                   fontdict=font_title)
    ax13.set_title(label="Evolution de l'énergie au cours de l'année",
                   fontdict=font_title)

    # Adding plots to graphs
    house_data['House_Energy'].plot(ax=ax13, colormap="Accent",
                                    linewidth=5, linestyle="-")
    house_data['House_Power'].plot(ax=ax12, colormap="Accent",
                                   linewidth=2, linestyle="-", )
    house_data[['T12_house', 'T12_rad_house',
                'T9_ext']].plot(ax=ax11, colormap="Accent",
                                linewidth=2, linestyle="-", )

    artiste_house(ax11, ax12, ax13, house_data)

    # Allow to plot axis labels only in the lower plot
    fig.autofmt_xdate()
    plt.show()


def algo_flow(csv_file, convert=True, sampling=None):
    print("Algo_flow reader")
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

    style = {'Vextra_state': 'k:', 'Pump_nb_heating': '-',
             'Flow_Solar': '--', 'Flow_Heating': '--',
             'Flow_S6_out': '-', 'Flow_S5_out': '-', 'Flow_S4_out': '-',
             'Flow_S1_out': '-', 'Flow_S2_out': '-', 'Flow_S3_out': '-',
             'S6_state': '-', 'S5_state': '-', 'S4_state': '-',
             'S1_state': '-', 'S2_state': '-', 'S3_state': '--'}

    # Adding fig instance
    fig = printer(title="Algo : pump mass flow rate")

    # Create Axes instance to plot in
    ax11 = fig.add_subplot(3, 2, 1)
    ax11.set_title(label="Evolution du débit des pompes solaires",
                   fontdict=font_title)
    # sharex allow to share x axis for all actions like zoom
    ax12 = fig.add_subplot(3, 2, 3, sharex=ax11)
    ax13 = fig.add_subplot(3, 2, 5, sharex=ax11)

    ax21 = fig.add_subplot(3, 2, 2)
    ax21.set_title(label="Evolution du débit des pompes de chauffage",
                   fontdict=font_title)
    ax22 = fig.add_subplot(3, 2, 4, sharex=ax21)
    ax23 = fig.add_subplot(3, 2, 6, sharex=ax21)

    # Add plot in each axes

    # First plot
    pump_algo[['Flow_Solar', 'Vextra_state']].plot(ax=ax11,
                                                   color=('#cb4b16', '#859900'),
                                                   ylim=(0, 120), linewidth=3)
    ax11_bis = ax11.twinx()
    pump_algo['Pump_nb_solar'].plot(ax=ax11_bis, color='#268bd2',
                                    ylim=(0, 6), linewidth=3)
    ax11.legend(loc='upper left')

    ax11_bis.legend(loc='upper right')
    pump_algo[['Flow_Heating', 'Vextra_state']].plot(ax=ax21,
                                                     color=('#cb4b16', '#859900'),
                                                     ylim=(0, 120), linewidth=3)
    ax21_bis = ax21.twinx()
    pump_algo['Pump_nb_heating'].plot(ax=ax21_bis, color='#268bd2',
                                      ylim=(0, 6), linewidth=3)
    ax21.legend(loc='upper left')
    ax21_bis.legend(loc='upper right')

    # Second plot
    pump_algo.ix[:, 'S6_state':'S5_state'].plot(ax=ax12, colormap='Accent',
                                                style=style, ylim=(0, 130),
                                                linewidth=3)
    pump_algo.ix[:, 'S4_state':'S3_state'].plot(ax=ax22, colormap='Accent',
                                                style=style, ylim=(0, 130),
                                                linewidth=3)

    # Third plot
    pump_algo.ix[:, 'Flow_S6_out':'Flow_S5_out'].plot(ax=ax13, colormap='Accent',
                                                      style=style, ylim=(0, 80),
                                                      linewidth=3)
    pump_algo.ix[:, 'Flow_S4_out':'Flow_S3_out'].plot(ax=ax23, colormap='Accent',
                                                      style=style, ylim=(0, 100),
                                                      linewidth=3)

    # Color match between second yaxis and lines
    for ytics in ax11_bis.get_yticklabels():
        ytics.set_color(ax11_bis.lines[0].get_color())
    for ytics in ax21_bis.get_yticklabels():
        ytics.set_color(ax21_bis.lines[0].get_color())

    # Update legend after all modifications
    ax12.legend(loc='best', ncol=2)
    ax22.legend(loc='best', ncol=2)

    # Datetime ticks
    seconds_loc = SecondLocator(10)
    ax11.xaxis.set_minor_locator(seconds_loc)
    ax21.xaxis.set_minor_locator(seconds_loc)
    minutes_formatter = DateFormatter("%M:%S")
    ax11.xaxis.set_major_formatter(minutes_formatter)
    ax21.xaxis.set_major_formatter(minutes_formatter)

    # Adding marks and shapes
    artiste_pump_algo(ax11, ax11_bis, ax12, ax13, ax21, ax21_bis, ax22, ax23, pump_algo)

    # Allow to plot axis labels only in the lower plot
    fig.autofmt_xdate()
    plt.show()


########################
#### Main Program : ####
########################


# Files location
folder_issue = "C:\\Users\\bois\\Documents\\GitHub\\SolarSystem\\Outputs\\Issues"
folder_clean = "C:\\Users\\bois\\Documents\\GitHub\\SolarSystem\\Outputs\\clean"
pump_csv = folder_issue + "\\Algo_flow\\algo_flow_mod_01_clean.csv"
house_csv = folder_clean + "\\olivier_house_read.csv"

# Change font properties
font_base = {'family': 'serif',
             'size': 15}
font_title = {'family': 'serif',
              'size': 20}

# Change default label settings
matplotlib.rc('font', **font_base)  # Overwrite default fonts parameters
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)

# House reader
house(csv_file=house_csv)

# Algo flow reader
algo_flow(csv_file=pump_csv)
