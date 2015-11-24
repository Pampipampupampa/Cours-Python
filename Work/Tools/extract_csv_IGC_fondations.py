# -*- coding:Utf8 -*-

# Need to implement the plotter.


"""
    Extract dataframe from a csv file created by acquisition on
    a underground water pipe (See IGC house nb 2).
"""


import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt

from some_tools import (fields_converter, plus_x, datetime_to_timestep,
                        integrate_simpson, resample)


def to_datetime_string(date_col, form="%m/%d/%Y %H:%M"):
    """
      This parser convert to a real datetime format a string according to

    """
    for date in date_col:
        # Does not keep seconds and micro-seconds.
        yield datetime.datetime.strptime(date[:-7], form)


def main(file_name, not_needed, names, index):
    # Get dataframe from file.
    frame = pd.read_csv(file_name, delimiter=",", encoding='utf-8', index_col=index)
    # Remove useless columns.
    for col in not_needed:
        del frame[col]
    # Rename usefull columns.
    frame.columns = names
    # Update index as a real datetime.
    frame.index = (el for el in to_datetime_string(frame.index))
    return frame


if __name__ == '__main__':
    # Folder for each experimentation.
    # FOLDER = "D:\\Github\\Projets\\IGC\\Etudes\\Etude_experimentale_PlafinoInnovert\\Experimentations\\Data\\Fondations" + \
             # "\\Experience_1\\20150710_112912668"
             # "\\Experience_4\\20150724_123823654"  # Charge
             # "\\Experience_4\\20150729_145312942"  # Décharge 1
             # "\\Experience_4\\20150803_111339216"  # Décharge 2

             # "\\Experience_3-2\\20150721_105450105"
             # "\\Experience_3-3\\20150722_110342075"
             # "\\Experience_3-1\\20150720_110253083"
             # "\\Experience_2\\20150713_160048642"

    FOLDER = "D:\\Github\\Projets\\IGC\\Etudes\\Etude_experimentale_PlafinoInnovert\\Experimentations\\Data\\Fondations" + \
             "\\Experience_3\\"
             # "\\Experience_4\\"
             # "\\Experience_3-3\\"
             # "\\Experience_3-2\\"
             # "\\Experience_3-1\\"
             # "\\Experience_1\\"

    # In the right order from left to right.
    NEW_COLUMNS = ("101_Tdepart_secondaire", "102_Tretour_secondaire", "105_Tsol_1.6m",
                   "106_Tfondations_14ml", "107_Tsol_1.2m", "108_Tfondations_5ml",
                   "109_Tsol_0.6m", "110_Tfondations_26ml", "115_Tdepart_primaire",
                   "116_Tretour_primaire")

    # Need some verification especialy for 120.
    # 122 in percent (humidity).
    # NEW_COLUMNS = ("101_Tdepart_secondaire", "102_Tretour_secondaire", "105_Tsol_1.6m",
    #                "106_Tfondations_14ml", "107_Tsol_1.2m", "108_Tfondations_5ml",
    #                "109_Tsol_0.6m", "110_Tfondations_26ml", "114_Tplafond_sejour",
    #                "115_Tdepart_primaire", "116_Tretour_primaire",
    #                "117_Tint_0.1m", "118_Tint_1.1m", "119_Tint_1.7m",
    #                "120_Tplafond_cuisine", "122_Humidite")

    # Change matplotlib default settings.
    font_base = {'size': 15,
                 'family': 'Source Code Pro'}
    matplotlib.rcParams['backend.qt4'] = "PySide"
    matplotlib.rc('font', **font_base)
    matplotlib.rc('xtick', labelsize=14)
    matplotlib.rc('ytick', labelsize=18)
    matplotlib.rc('legend', labelspacing=0.1)

    # frame = main(FOLDER+"\dat00001.csv", not_needed=["Sweep #"], names=NEW_COLUMNS, index="Time")
    frame = main(FOLDER+"full_exp.csv", not_needed=["Sweep #"], names=NEW_COLUMNS, index="Time")
    print("\nListe de l’ensemble des paramètres disponibles pour ce jeu de données.")
    print(frame.columns)

    # Default behavior.
    datashift_enable = False
    title = "Données originales"
    datashift_enable = input("Shift data to more realistic behavior ?" +
                             "\n--> Oui ou Non: ")
    if datashift_enable in ("OUI", "Oui", "oui", "1"):
        # Data shift.
        print("\nCompute data shifting.")
        shifts = {"105_Tsol_1.6m": [{"x": -2.606}, plus_x],
                  "106_Tfondations_14ml": [{"x": -2.540}, plus_x],
                  "107_Tsol_1.2m": [{"x": -0.562}, plus_x],
                  "108_Tfondations_5ml": [{"x": -2.606}, plus_x],
                  "110_Tfondations_26ml": [{"x": -2.318}, plus_x]}
        fields_converter(frame, shifts)
        title = "Données recalées sur la base de l’expérience 4"

    mass_flow = float(input("\nValeur du débit en [l/h]: "))
    mass_flow = mass_flow / 3600  # Conversion to Kg/s
    # Add power evolution.
    print("\nCompute Power.")
    frame["Puissance_fondations"] = mass_flow * 4180 * (frame["101_Tdepart_secondaire"] - frame["102_Tretour_secondaire"])

    # Get energy [J]
    print("Compute Energy.")
    frame = resample(frame, '1min')  # Used for reconstructed data with missing values.
    frame_index = frame.index.copy()
    frame.index = (el for el in datetime_to_timestep(iter(frame.index)))
    energy = integrate_simpson(frame, "Puissance_fondations")
    frame.index = frame_index
    print("L’énergie cumulée est de: {:d} Wh".format(int(energy / 3600)))

    # Prepare Plot
    print("\nPlotting data.")
    # # Grid plot
    # nrows, ncols = 2, 2
    # sharex, sharey = True, False
    # fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey,
    #                          figsize=(24, 12), facecolor="white",
    #                          edgecolor="#FFFFFF", frameon=True)

    # # Plot
    # frame[["101_Tdepart_secondaire",
    #        "102_Tretour_secondaire"]].plot(ax=axes[0][0], kind="line", legend=True,
    #                                        linewidth=3, stacked=False,
    #                                        colormap="Set1")
    # frame[["108_Tfondations_5ml",
    #        "106_Tfondations_14ml",
    #        "110_Tfondations_26ml",
    #        "102_Tretour_secondaire"]].plot(ax=axes[1][1], kind="line", legend=True,
    #                                        linewidth=3, stacked=False,
    #                                        colormap="Set1")
    # frame[["105_Tsol_1.6m",
    #        "107_Tsol_1.2m",
    #        "109_Tsol_0.6m"]].plot(ax=axes[1][0], kind="line", legend=True,
    #                               linewidth=3, stacked=False,
    #                               colormap="Set1")
    # frame[["Puissance_fondations"]].plot(ax=axes[0][1], kind="area", legend=True,
    #                                      linewidth=3, stacked=False,
    #                                      colormap="Set1")

    # rows plot
    # nrows, ncols = 2, 1
    # sharex, sharey = True, False
    # fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey,
    #                          figsize=(24, 12), facecolor="white",
    #                          edgecolor="#FFFFFF", frameon=True)

    # # Plot
    # frame[["101_Tdepart_secondaire",
    #        "102_Tretour_secondaire",
    #        "108_Tfondations_5ml",
    #        "110_Tfondations_26ml"]].plot(ax=axes[0], kind="line", legend=True,
    #                                      linewidth=3, stacked=False,
    #                                      colormap="Set1")

    # frame[["Puissance_fondations"]].plot(ax=axes[1], kind="area", legend=True,
    #                                      linewidth=3, stacked=False,
    #                                      colormap="Set1")

    # frame[["101_Tdepart_secondaire",
    #        "102_Tretour_secondaire",
    #        "108_Tfondations_5ml",
    #        "106_Tfondations_14ml",
    #        "110_Tfondations_26ml"]].plot(ax=axes[0], kind="line", legend=True,
    #                                      linewidth=3, stacked=False,
    #                                      colormap="Set1")
    # frame[["105_Tsol_1.6m",
    #        "107_Tsol_1.2m",
    #        "109_Tsol_0.6m"]].plot(ax=axes[1], kind="line", legend=True,
    #                               linewidth=3, stacked=False,
    #                               colormap="Set1")

    # nrows, ncols = 1, 1
    # sharex, sharey = True, False
    # fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey,
    #                          figsize=(24, 12), facecolor="white",
    #                          edgecolor="#FFFFFF", frameon=True)

    # frame[["101_Tdepart_secondaire",
    #        "102_Tretour_secondaire",
    #        "108_Tfondations_5ml",
    #        "106_Tfondations_14ml",
    #        "110_Tfondations_26ml"]].plot(ax=axes, kind="line", legend=True,
    #                                      linewidth=3, stacked=False,
    #                                      colormap="Set1")
    # frame[["105_Tsol_1.6m",
    #        "107_Tsol_1.2m",
    #        "109_Tsol_0.6m"]].plot(ax=axes, kind="line", legend=True,
    #                               linewidth=3, stacked=False,
    #                               colormap="Set1")
    nrows, ncols = 3, 1
    sharex, sharey = True, False
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey,
                             figsize=(24, 12), facecolor="white",
                             edgecolor="#FFFFFF", frameon=True)

    # # Plot
    frame[["101_Tdepart_secondaire",
           "102_Tretour_secondaire",
           "108_Tfondations_5ml",
           "106_Tfondations_14ml",
           "110_Tfondations_26ml"]].plot(ax=axes[0], kind="line", legend=True,
                                         linewidth=3, stacked=False,
                                         colormap="Set1")
    frame[["105_Tsol_1.6m",
           "107_Tsol_1.2m",
           "109_Tsol_0.6m"]].plot(ax=axes[1], kind="line", legend=True,
                                  linewidth=3, stacked=False,
                                  colormap="Set1")

    frame[["Puissance_fondations"]].plot(ax=axes[2], kind="area", legend=True,
                                         linewidth=3, stacked=False,
                                         colormap="Set1")

    # plt.figtext(0.35, 0.95, title)
    # Display graph
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.15)
    plt.show()
