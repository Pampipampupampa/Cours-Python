# -*- coding:Utf8 -*-

# Need to implement the plotter.


"""
    Extract dataframe from a csv file created by acquisition on
    a underground water pipe (See IGC house nb 2).
"""


import pandas as pd
import datetime
import matplotlib
# import matplotlib.pyplot as plt


def to_datetime_minute(date_col, form="%m/%d/%Y %H:%M"):
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
    frame.index = (el for el in to_datetime_minute(frame.index))
    return frame

if __name__ == '__main__':
    FOLDER = "D:\Github\Projets\IGC\Etudes\Etude_expérimentale_PlafinoInnovert\Expérimentations\Data\Fondations\Expérience_0\\20150710_104832071"
    # In the right order from left to right.
    # NEW_COLUMNS = ("101_Tdepart_secondaire", "102_Tretour_secondaire", "105_Tsol_1.6m",
    #                "106_Tfondations_14ml", "107_Tsol_1.2m", "108_Tfondations_5ml",
    #                "109_Tsol_0.6m", "110_Tfondations_26ml", "115_Tdepart_primaire",
    #                "116_Tretour_primaire")

    # Need some verification especialy for 120.
    # 122 in percent (humidity).
    NEW_COLUMNS = ("101_Tdepart_secondaire", "102_Tretour_secondaire", "105_Tsol_1.6m",
                   "106_Tfondations_14ml", "107_Tsol_1.2m", "108_Tfondations_5ml",
                   "109_Tsol_0.6m", "110_Tfondations_26ml", "114_Tplafond_sejour",
                   "115_Tdepart_primaire", "116_Tretour_primaire",
                   "117_Tint_0.1m", "118_Tint_1.1m", "119_Tint_1.7m",
                   "120_Tplafond_cuisine", "122_Humidite")

    # Change matplotlib default settings
    font_base = {'size': 15,
                 'family': 'Source Code Pro'}
    matplotlib.rcParams['backend.qt4'] = "PySide"
    matplotlib.rc('font', **font_base)
    matplotlib.rc('xtick', labelsize=14)
    matplotlib.rc('ytick', labelsize=18)
    matplotlib.rc('legend', labelspacing=0.1)

    frame = main(FOLDER+"\dat00001.csv", not_needed=["Sweep #"], names=NEW_COLUMNS, index="Time")
    print(frame.columns)  # Working
