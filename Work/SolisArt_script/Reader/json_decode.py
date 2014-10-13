#! /usr/bin/env python
# -*- coding:Utf8 -*-


# Import objects from evaluation script
from Plotters.evaluation import *

import json

# Keep trace of all plots with time
from datetime import datetime as dt
import os

#######################################
#### Classes, Methods, Functions : ####
#######################################


def extract_nested_json1(datas, parameter, rows, cols):
    """
        Extract a third level nested json dict according to the parameter value.
            datas : dict
            parameter : integer or string
                        dict last level key extracted
            rows : list or tuple
                   dict second level keys (all keys we want to extract)
            cols : list or tuple
                   dict first level keys (all keys we want to extract)
        structure must be like this one : {first_level: {second_level: {last_level: value_of_last_level}}}
        Return a prepare dict for create a dataframe with it.

        example : datas = {"chambery":
                                      {"January":
                                                   {"solar_heating": 1,
                                                    "extra_heating": 2},
                                       "February":
                                                   {"solar_heating": 3,
                                                    "extra_heating": 4}
                                      },
                           "bordeaux":
                                      {"January":
                                                   {"solar_heating": 11,
                                                    "extra_heating": 22},
                                       "February":
                                                   {"solar_heating": 33,
                                                    "extra_heating": 44}
                                      }
                          }
                  parameter can be "solar_heating"
                  rows can be ["January", "February"]
                  cols can be ["chambery", "bordeaux"]

                  return {'bordeaux': [11, 33], 'chambery': [1, 3]}
    """
    return {col: [datas[col][row][parameter] for row in rows] for col in cols}


def extract_nested_json2(datas, parameters, rows, cols):
    """
        Extract a third level nested json dict according to the parameter value.
            datas : dict
            parameter : integer or string
                        dict last level key extracted
            rows : list or tuple
                   dict second level keys (all keys we want to extract)
            cols : list or tuple
                   dict first level keys (all keys we want to extract)
        structure must be like this one : {first_level: {second_level: {last_level: value_of_last_level}}}
        Return a prepare dict for create a dataframe with it.

        example : datas = {"chambery":
                                      {"January":
                                                   {"solar_heating": 1,
                                                    "extra_heating": 2},
                                       "February":
                                                   {"solar_heating": 3,
                                                    "extra_heating": 4}
                                      },
                           "bordeaux":
                                      {"January":
                                                   {"solar_heating": 11,
                                                    "extra_heating": 22},
                                       "February":
                                                   {"solar_heating": 33,
                                                    "extra_heating": 44}
                                      }
                          }
                  parameter = ("solar_heating", "extra_heating")
                  rows      = ["January", "February"]
                  cols      = ["chambery", "bordeaux"]

                  yield     ("solar_heating",
                             {'bordeaux': [11, 33], 'chambery': [1, 3]})
                            ("extra_heating",
                             {'bordeaux': [22, 44], 'chambery': [2, 4]})

    """
    for val in parameters:
        yield val, {col: [datas[col][row][val] for row in rows] for col in cols}


########################
#### Main Program : ####
########################


if __name__ == '__main__':
    # File to load
    json_file = "D:\Github\solarsystem\Outputs\Plots_stock\Time_sav" + \
                "\\allSimulation_timedata.json"
    # Load json
    with open(json_file, 'r', encoding='utf-8') as f:
        datas = json.load(f, object_pairs_hook=OrdD)

    # Create structures to plots times
    title = "Heating time informations"
    parameters = ("heating_time", "solar_heating", "extra_heating", "Difference")
    cols = tuple(el for el in datas)
    rows = tuple(mths for mths in datas['chambery'])
    rows = rows[:-1]  # Keep only months (comment to take all)
    # rows = rows[-1:]  # Keep only annuel (comment to take all)

    structs = {ind: el for ind, el in extract_nested_json2(datas, parameters,
                                                           rows, cols)}
    # Create all dataframes
    frames = {}
    for val in parameters:
        frames[val] = pd.DataFrame({el: structs[val][el] for el in structs[val]},
                                   index=rows)
        # Cast seconds to days
        frames[val] = frames[val] / (3600*24)
    # Add plot
    Plot = MultiPlotter({}, nb_cols=2, nb_rows=2, colors=None,
                        title=title, sharex=True, sharey=False)
    Plot.font_legend = {'size': 5,
                        'family': 'Anonymous Pro'}
    Plot.fig_init(figsize=(24, 12))

    heat = Plot.frame_plot(frames["heating_time"], fields="all", legend=False,
                           title='Heating time',
                           loc='left', kind="bar", pos=(0, 0))
    diff = Plot.frame_plot(frames["Difference"], fields="all", legend=False,
                           title='Différences entre solaire et appoint',
                           loc='left', kind="bar", pos=(0, 1))
    solar = Plot.frame_plot(frames["solar_heating"], fields="all", legend=True,
                            title='Temps de chauffage solaire',
                            loc='left', kind="bar", pos=(1, 0))
    extra = Plot.frame_plot(frames["extra_heating"], fields="all", legend=False,
                            title='Temps de chauffage par l’appoint',
                            loc='left', kind="bar", pos=(1, 1))
    # Add ylabel to each plots
    Plot.set_axes_label('Jours', pos=(0, 0), axe='y')
    Plot.set_axes_label('Jours', pos=(0, 1), axe='y')
    Plot.set_axes_label('Jours', pos=(1, 0), axe='y')
    Plot.set_axes_label('Jours', pos=(1, 1), axe='y')

    # Adjust plot format (avoid overlaps)
    Plot.adjust_plots(hspace=0.6, wspace=0.15,
                      top=0.85, bottom=0.08,
                      left=0.05, right=0.96)
    Plot.tight_layout()

    # Recup current time
    now = dt.now()

    # Check and create a folder per month
    FOLDER = "D:\Github\solarsystem\Outputs\Plots_stock"
    destination = {"base": FOLDER + '\\' + dt.strftime(now, "%Y_%m"),
                   "pdf": FOLDER + '\\' + dt.strftime(now, "%Y_%m") + "\\pdf",
                   "png": FOLDER + '\\' + dt.strftime(now, "%Y_%m") + "\\png",
                   "svg": FOLDER + '\\' + dt.strftime(now, "%Y_%m") + "\\svg"}
    if not os.path.exists(destination["base"]):
        os.makedirs(destination["base"])
        os.makedirs(destination["pdf"])
        os.makedirs(destination["png"])
        os.makedirs(destination["svg"])

    simulation = "Simulation_time"

    unique = dt.strftime(now, "%Y%m%d-%Hh%Mm%Ss")  # Unique indentity
    # Save as pdf
    name = '{0}\{2}{1}.pdf'.format(destination["pdf"], simulation, unique)
    Plot.fig.savefig(name, dpi=150, transparent=False,
                     facecolor=Plot.background_color)
    # Save as png
    name = '{0}\{2}{1}.png'.format(destination["png"], simulation, unique)
    Plot.fig.savefig(name, dpi=150, transparent=False,
                     facecolor=Plot.background_color)
    # Save as svg
    name = '{0}\{2}{1}.svg'.format(destination["svg"], simulation, unique)
    Plot.fig.savefig(name, dpi=150, transparent=False,
                     facecolor=Plot.background_color)

    # Display plots
    Plot.show()
