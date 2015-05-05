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
json_file = "D:\Github\solarsystem\Outputs\Plots_stock\Energy_sav" + \
            "\\dico_energy_20150219.json"

rows = ['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October',
        'November', 'December']

# Load json
with open(json_file, 'r', encoding='utf-8') as f:
    datas = json.load(f, object_pairs_hook=OrdD)

# Create structures to plots times
title = "Energy informations"
parameters = ("Production", "Pertes capteur", "Pertes réseau", "Energie captable",
              "Pertes totales", "Production\nsolaire", "Pertes appoint",
              "Rendement capteur", "Besoins", "Taux de couverture",
              "Consommation\nappoint", "Chauffage", "Production\nappoint", "ECS")
cols = tuple(el for el in datas)
structs = {ind: el for ind, el in iter_nested_json(datas, parameters,
                                                   rows, cols)}

# Create all dataframes
frames = {}
for val in parameters:
    frames[val] = pd.DataFrame({el: structs[val][el] for el in structs[val]},
                               index=rows)
    # Sum the columns:
    sum_row = {col: frames[val][col].sum() for col in frames[val]}
    # Turn the sums into a DataFrame with one row with an index of 'Annual':
    sum_df = pd.DataFrame(sum_row, index=["Annual"])
    # Now append the row:
    frames[val] = frames[val].append(sum_df)

# Update the last col of "Taux de couverture"
for col in cols:
    # Calculate new ratio
    frames["Taux de couverture"].ix[-1:,
                                    col] = (100 *
                                            frames["Production\nsolaire"].ix[-1:,
                                                                             col] /
                                            frames["Production"].ix[-1:,
                                                                    col])
    # Calculate new ratio
    frames["Rendement capteur"].ix[-1:,
                                   col] = (100 *
                                           frames["Production\nsolaire"].ix[-1:,
                                                                            col] /
                                           frames["Energie captable"].ix[-1:,
                                                                         col])

# Columns to plot
# to_plot = ['January', 'February', 'March', 'April']
# to_plot = ['May', 'June', 'July', 'August']
# to_plot = ['September', 'October', 'November', 'December']

# Add plot
Plot = MultiPlotter({}, nb_cols=2, nb_rows=2, colors=None,
                    title=title, sharex=True, sharey=False)
Plot.font_legend = {'size': 5,
                    'family': 'Anonymous Pro'}
Plot.fig_init(figsize=(24, 12))


couverture = Plot.frame_plot(frames["Taux de couverture"].ix[-1:, :], fields="all",
                             legend=False,
                             title='Couverture solaire', ylim=(-10, 110),
                             loc='left', kind="bar", pos=(0, 1))
rendement = Plot.frame_plot(frames["Rendement capteur"].ix[-1:, :], fields="all",
                            legend=False,
                            title='Rendement des capteurs',
                            loc='left', kind="bar", pos=(1, 1))
solaire = Plot.frame_plot(frames["Production\nsolaire"].ix[-1:, :], fields="all",
                          legend=False,
                          title='Production solaire',
                          loc='left', kind="bar", pos=(0, 0))
appoint = Plot.frame_plot(frames["Production\nappoint"].ix[-1:, :], fields="all",
                          legend=False,
                          title='Production appoint',
                          loc='left', kind="bar", pos=(1, 0))

# Add ylabel to each plots
Plot.set_axes_label('KWh', pos=(0, 0), axe='y')
Plot.set_axes_label('%', pos=(0, 1), axe='y')
Plot.set_axes_label('KWh', pos=(1, 0), axe='y')
Plot.set_axes_label('%', pos=(1, 1), axe='y')
# Change legend alignement
Plot.catch_axes(*(1, 0)).legend(ncol=1, loc=0)

# Only for annual simulations
# Tight plot (left aligned)
Plot.catch_axes(*(1, 0)).set_xlim(-0.255, 0.382)
Plot.catch_axes(*(1, 1)).set_xlim(-0.255, 0.382)
Plot.catch_axes(*(0, 0)).set_xlim(-0.255, 0.382)
Plot.catch_axes(*(0, 1)).set_xlim(-0.255, 0.382)
# Tight plot (vertical limit)
Plot.catch_axes(*(1, 1)).set_ylim(-5, 55)
Plot.catch_axes(*(0, 1)).set_ylim(-5, 100)


# Adjust plot format (avoid overlaps)
Plot.adjust_plots(hspace=0.6, wspace=0.15,
                  top=0.85, bottom=0.08,
                  left=0.05, right=0.96)
Plot.tight_layout()


# sav_plot(folder="D:\Github\solarsystem\Outputs\Plots_stock",
         # base_name="Simulation_energy", plotter=Plot, facecolor="white")

# Display plots
Plot.show()
