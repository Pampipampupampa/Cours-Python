#! /usr/bin/env python
# -*- coding:Utf8 -*-

import json

# Import internal lib
from Plotters.evaluation import *
from json_decode import iter_nested_json


########################
#    Main Program :    #
########################


# File to load
json_file = "D:\Github\solarsystem\Outputs\Plots_stock\Time_sav" + \
            "\\heating_time_20150204.json"
# Load json
with open(json_file, 'r', encoding='utf-8') as f:
    datas = json.load(f, object_pairs_hook=OrdD)

# Create structures to plots times
title = "Heating time informations"
parameters = ("heating_time", "solar_heating", "extra_heating",
              "Difference", "ratio", "solar_working")
cols = tuple(el for el in datas)
rows = tuple(mths for mths in datas['chambery-0p'])
# rows = rows[:-1]  # Keep only months (comment to take all)
rows = rows[-1:]  # Keep only annuel (comment to take all)

structs = {ind: el for ind, el in iter_nested_json(datas, parameters,
                                                   rows, cols)}
# Create all dataframes
frames = {}
for val in parameters:
    frames[val] = pd.DataFrame({el: structs[val][el] for el in structs[val]},
                               index=rows)
    # Cast seconds to days
    if val != 'ratio':
        frames[val] = frames[val] / (3600*24)
# Add plot
Plot = MultiPlotter({}, nb_cols=2, nb_rows=2, colors=None,
                    title=title, sharex=True, sharey=False)
Plot.font_legend = {'size': 5,
                    'family': 'Anonymous Pro'}
Plot.fig_init(figsize=(24, 12))

heat = Plot.frame_plot(frames["heating_time"], fields="all", legend=False,
                       title='Temps de chauffage',
                       loc='left', kind="bar", pos=(1, 0))
solar_w = Plot.frame_plot(frames["solar_working"], fields="all", legend=False,
                          title='Temps de fonctionnement des capteurs solaires',
                          loc='left', kind="bar", pos=(0, 0), ylim=(-10, 110))
solar_h = Plot.frame_plot(frames["solar_heating"], fields="all", legend=True,
                          title='Temps de chauffage en solaire direct',
                          loc='left', kind="bar", pos=(0, 1))
extra_h = Plot.frame_plot(frames["extra_heating"], fields="all", legend=False,
                          title='Temps de chauffage par l’appoint',
                          loc='left', kind="bar", pos=(1, 1))

# Add ylabel to each plots
Plot.set_axes_label('Jours', pos=(0, 0), axe='y')
Plot.set_axes_label('Jours', pos=(0, 1), axe='y')
Plot.set_axes_label('Jours', pos=(1, 0), axe='y')
Plot.set_axes_label('Jours', pos=(1, 1), axe='y')
# Change legend alignement
Plot.catch_axes(*(1, 0)).legend(ncol=1)

# Only for annual simulations
# Tight plot (left aligned)
Plot.catch_axes(*(1, 0)).set_xlim(-0.255, 0.382)
Plot.catch_axes(*(1, 1)).set_xlim(-0.255, 0.382)
Plot.catch_axes(*(0, 0)).set_xlim(-0.255, 0.382)
Plot.catch_axes(*(0, 1)).set_xlim(-0.255, 0.382)
# Tight plot (vertical limit)
Plot.catch_axes(*(0, 0)).set_ylim(-5, 140)
Plot.catch_axes(*(1, 0)).set_ylim(-5, 120)

# Adjust plot format (avoid overlaps)
Plot.adjust_plots(hspace=0.6, wspace=0.15,
                  top=0.85, bottom=0.08,
                  left=0.05, right=0.96)
Plot.tight_layout()

sav_plot(folder="D:\Github\solarsystem\Outputs\Plots_stock",
         base_name="Simulation_time", plotter=Plot, facecolor="white")

# Display plots
Plot.show()
