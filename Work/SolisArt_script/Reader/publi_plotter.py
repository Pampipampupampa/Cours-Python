#! /usr/bin/env python
# -*- coding:Utf8 -*-

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import json
from collections import OrderedDict as OrdD
from json_decode import iter_nested_json
# from Plotters.evaluation import EvalData, MultiPlotter, sav_plot

#######################################
#    Classes, Methods, Functions :    #
#######################################


########################
#    Main Program :    #
########################

# Folder to store plots
FOLDER = "D:\\Github\\solarsystem\\Outputs\\Plots_stock\\No_automations\\"

# File to load
json_file = "D:\Github\solarsystem\Outputs\Plots_stock\Energy_sav\\dico_energy.json"

# Row index for extracted datas
rows = ['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October',
        'November', 'December']


#
# Extract data from json file and map values into dictionnary of frames
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

# Font used inside plots
font_title = {'size': 20,
              'family': 'Source Code Pro'}
font_legend = {'size': 15,
               'family': 'Source Code Pro'}
font_base = {'size': 15,
             'family': 'Source Code Pro'}
font_tex = {'size': 28,
            'family': 'Source Code Pro'}
# Change matplotlib default settings
matplotlib.rcParams['backend.qt4'] = "PySide"
matplotlib.rc('font', **font_base)
matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=18)
matplotlib.rc('legend', labelspacing=0.1)

# Constant to prepare plot
cities = [[['chambery-3p', 'chambery-6p', 'chambery-9p'], ['bordeaux-3p', 'bordeaux-6p', 'bordeaux-9p']],
          [['strasbourg-3p', 'strasbourg-6p', 'strasbourg-9p'],  ['marseille-3p', 'marseille-6p', 'marseille-9p']]]
xlabel, ylabel = "Months", ["$F_{Sav}$ (%)", "$\\eta$ (%)"]
# Create fig and axes instances
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(23, 13), sharex='all', sharey='all')
# Twin axes to have two yaxis
axes_bis = [[axe.twinx() for axe in mini] for mini in axes]
# Auto plot on  each axes the right plot (2 rows and 2 cols)
for x in range(2):
    for y in range(2):
        # Concat all simulation
        rendements = pd.concat([frames["Rendement capteur"][capteur] for capteur in cities[x][y]], axis=1)
        covers = pd.concat([frames["Taux de couverture"][capteur] for capteur in cities[x][y]], axis=1)
        # Plot simulations to figure fig
        covers[:-1].plot(ax=axes[x][y], legend=False, linewidth=2, style=['gv--', 'g*--', 'gs--'], rot=30, markersize=10)  # Solar fraction
        rendements[:-1].plot(ax=axes_bis[x][y], legend=False, linewidth=1, style=['bv-', 'b*-', 'bs-'], markersize=10)     # Efficiency
        # Hack to update lines colors due to lack of original option with hex colors
        for line_ in axes[x][y].lines:
            line_.set_color('#859900')
            line_.set_markeredgecolor('#859900')
            # Allow to change marker edge width
            # line_.set_markeredgewidth(4)
        for line_ in axes_bis[x][y].lines:
            line_.set_color('#268bd2')
            line_.set_markeredgecolor('#268bd2')
            # Allow to change marker edge width
            # line_.set_markeredgewidth(4)
        # Add correct legend to each lines and title
        if y % 2:
            axes_bis[x][y].legend([number+' collectors' for number in ['3', '6', '9']], loc=1, prop=font_legend, ncol=1)
        else:
            axes[x][y].legend([number+' collectors' for number in ['3', '6', '9']], loc=2, prop=font_legend, ncol=1)
        # Add title to each plot
        axes[x][y].set_title(label=cities[x][y][0][:-3].capitalize(), loc='center', fontdict=font_title)
        # Color match between yaxis and lines
        for ytics in axes[x][y].get_yticklabels():
            ytics.set_color(axes[x][y].lines[0].get_color())
        for ytics in axes_bis[x][y].get_yticklabels():
            ytics.set_color(axes_bis[x][y].lines[0].get_color())
        # Redefine the y axis limits for the twins axes (have to define one per one)
        axes_bis[x][y].set_ylim(0, 125)
    # Update ylabels with their corresponding axes lines colors (original axes)
    axes[x][0].set_ylabel(ylabel[0], color=axes[x][0].lines[0].get_color(), fontsize=font_tex['size'])
    # Hide a specific axis (here y axis for first columns plots)
    axes_bis[x][0].get_yaxis().set_ticks([])  # Same as axes_bis[x][0].get_yaxis().set_visible(False)
    # Update ylabels with their corresponding axes lines colors (twin axes)
    axes_bis[x][1].set_ylabel(ylabel[1], color=axes_bis[x][1].lines[0].get_color(), fontsize=font_tex['size'])
# Update y axes ticks limits (due to sharing, effect on all axes)
axes[0][0].set_ylim(0, 125)
# Minimize space between each plot elements
plt.tight_layout()
# Save plot to file
fig.savefig(filename=FOLDER+'Fsav_Rendement.png', dpi=300, transparent=False, orientation='landscape')
# Draw on screen the figure (fig)
plt.show()


#
# Irradiations on tilted surface
#

# Font used inside plots
font_title = {'size': 20,
              'family': 'Source Code Pro'}
font_legend = {'size': 24,
               'family': 'Source Code Pro'}
font_base = {'size': 26,
             'family': 'Source Code Pro'}
font_tex = {'size': 35,
            'family': 'Source Code Pro'}
# Change matplotlib default settings
matplotlib.rcParams['backend.qt4'] = "PySide"
matplotlib.rc('font', **font_base)
matplotlib.rc('xtick', labelsize=26)
matplotlib.rc('ytick', labelsize=26)
matplotlib.rc('legend', labelspacing=0.2)

cities = ['chambery-6p', 'bordeaux-6p', 'strasbourg-6p', 'marseille-6p']
ylabel = "$kWh/m^2$"
# Concat all simulation
captable = pd.concat([frames['Energie captable'][capteur] for capteur in cities], axis=1) / (6*2.32)
captable.columns = ['chambery', 'bordeaux', 'strasbourg', 'marseille']
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
captable[:-1].plot(ax=axes, kind='bar', colormap="Accent", rot=30)
axes.set_ylim(0, 230)
axes.set_ylabel(ylabel, fontdict=font_tex)
# Minimize space between each plot elements
plt.tight_layout()
# Save plot to file
fig.savefig(filename=FOLDER+'Irradiations_Tilt.png', dpi=300, transparent=False, orientation='landscape')
# Draw on screen the figure (fig)
plt.show()


# #
# # Mean temperature for each weather
# #

# cities = ['chambery-6p', 'bordeaux-6p', 'strasbourg-6p', 'marseille-6p']
# ylabel = "°C"
# # Concat all simulation
# captable = pd.concat([frames['T9_ext'][capteur] for capteur in cities], axis=1)
# fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
# captable[:-1].plot(ax=axes, kind='line', colormap="Accent", rot=30, style=['8-', 's-', 'h-', 'D-'])
# axes.legend([name[:-3] for name in cities], loc=0)
# axes.set_ylabel(ylabel, fontdict=font_base)
# # Minimize space between each plot elements
# plt.tight_layout()
# # Save plot to file
# # fig.savefig(filename=FOLDER+'Irradiations_Tilt.png', dpi=300, transparent=False, orientation='landscape')
# # Draw on screen the figure (fig)
# plt.show()
