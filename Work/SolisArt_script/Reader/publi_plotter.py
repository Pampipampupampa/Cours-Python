#! /usr/bin/env python
# -*- coding:Utf8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import json
from collections import OrderedDict as OrdD
from json_decode import iter_nested_json
from Plotters.evaluation import EvalData, MultiPlotter

#######################################
#    Classes, Methods, Functions :    #
#######################################


########################
#    Main Program :    #
########################


# File to load
json_file = "D:\Github\solarsystem\Outputs\Plots_stock\Energy_sav\\dico_test.json"

# Row index for extracted datas
rows = ['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October',
        'November', 'December']
# Font used inside plots
font_base = {'size': 20,
             'family': 'STIXGeneral'}

#
# Extract data from json file
#

# Load json
with open(json_file, 'r', encoding='utf-8') as f:
    datas = json.load(f, object_pairs_hook=OrdD)

# Create structures to plots times
title = "Energy informations"
# Values to extract from json
parameters = ("Production", "Pertes capteur", "Pertes réseau", "Energie captable",
              "Pertes totales", "Production\nsolaire", "Pertes appoint",
              "Rendement capteur", "Besoins", "Taux de couverture",
              "Consommation\nappoint", "Chauffage", "Production\nappoint", "ECS",
              "T1", "T3", "T4", "T5", "T7", "T8", "T9_ext", "T12_house")
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
# Update the last col of ratio and temperatures
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
    for temperature in ["T1", "T3", "T4", "T5", "T7", "T8", "T9_ext", "T12_house"]:
        frames[temperature][col][-1:] = frames[temperature][col][:-1].mean()


#
# Solar fraction and efficiency for the four simulations
#

# Constant to prepare plot
cities = [[['chambery-3p', 'chambery-6p', 'chambery-9p'], ['bordeaux-3p', 'bordeaux-6p', 'bordeaux-9p']],
          [['strasbourg-3p', 'strasbourg-6p', 'strasbourg-9p'],  ['marseille-3p', 'marseille-6p', 'marseille-9p']]]
cities = [[['chambery-3p', 'chambery-6p', 'chambery-9p'], ['chambery-3p', 'chambery-6p', 'chambery-9p']],
          [['chambery-3p', 'chambery-6p', 'chambery-9p'],  ['chambery-3p', 'chambery-6p', 'chambery-9p']]]
xlabel, ylabel = "Months", ["$F_{sav}$ (%)", "$\\eta$ (%)"]
# Create fig and axes instances
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10), sharex='all', sharey='all')
# Twin axes to have two yaxis
axes_bis = [[axe.twinx() for axe in mini] for mini in axes]
# Auto plot on  each axes the right plot (2 rows and 2 cols)
for x in range(2):
    for y in range(2):
        # Concat all simulation
        rendements = pd.concat([frames["Rendement capteur"][capteur] for capteur in cities[x][y]], axis=1)
        covers = pd.concat([frames["Taux de couverture"][capteur] for capteur in cities[x][y]], axis=1)
        # Plot simulations to figure fig
        covers[:-1].plot(ax=axes[x][y], legend=True, linewidth=1, style=['gv-', 'g*-', 'gs-'], rot=30)  # Solar fraction
        rendements[:-1].plot(ax=axes_bis[x][y], legend=True, linewidth=1, style=['bv-', 'b*-', 'bs-'])  # Efficiency
        # Hack to update lines colors due to lack of original option with hex colors
        for line_ in axes[x][y].lines:
            line_.set_color('#268bd2')
        for line_ in axes_bis[x][y].lines:
            line_.set_color('#dc322f')
        # Add correct legend to each lines
        axes[x][y].legend([name for name in cities[x][y]], loc=2)
        axes_bis[x][y].legend([name for name in cities[x][y]], loc=1)
        # Color match between yaxis and lines
        for ytics in axes[x][y].get_yticklabels():
            ytics.set_color(axes[x][y].lines[0].get_color())
        for ytics in axes_bis[x][y].get_yticklabels():
            ytics.set_color(axes_bis[x][y].lines[0].get_color())
        # Redefine the y axis limits for the twins axes (have to define one per one)
        axes_bis[x][y].set_ylim(0, 125)
    # Update ylabels with their corresponding axes lines colors (original axes)
    axes[x][0].set_ylabel(ylabel[0], fontdict=font_base, color=axes[x][0].lines[0].get_color())
    # Hide a specific axis (here y axis for first columns plots)
    axes_bis[x][0].get_yaxis().set_ticks([])  # Same as axes_bis[x][0].get_yaxis().set_visible(False)
    # Update ylabels with their corresponding axes lines colors (twin axes)
    axes_bis[x][1].set_ylabel(ylabel[1], fontdict=font_base, color=axes_bis[x][1].lines[0].get_color())
# Update y axes ticks limits (due to sharing, effect on all axes)
axes[0][0].set_ylim(0, 125)
# Minimize space between each plot elements
plt.tight_layout()
# Draw on screen the figure (fig)
plt.show()


#
# Irradiations on tilted surface
#

cities = ['chambery-6p', 'bordeaux-6p', 'strasbourg-6p', 'marseille-6p']
ylabel = "$KWh/m^2$"
# Concat all simulation
captable = pd.concat([frames['Energie captable'][capteur] for capteur in cities], axis=1) / (6*2.32)
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
captable[:-1].plot(ax=axes, kind='bar', colormap="Accent", rot=30)
axes.legend([name[:-3] for name in cities], loc=0)
axes.set_ylabel(ylabel, fontdict=font_base)
plt.tight_layout()
plt.show()


#
# Mean temperature for each weather
#

cities = ['chambery-6p', 'bordeaux-6p', 'strasbourg-6p', 'marseille-6p']
ylabel = "°C"
# Concat all simulation
captable = pd.concat([frames['T9_ext'][capteur] for capteur in cities], axis=1)
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
captable[:-1].plot(ax=axes, kind='line', colormap="Accent", rot=30, style=['8-', 's-', 'h-', 'D-'])
axes.legend([name[:-3] for name in cities], loc=0)
axes.set_ylabel(ylabel, fontdict=font_base)
plt.tight_layout()
plt.show()
