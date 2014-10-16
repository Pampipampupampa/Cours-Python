#! /usr/bin/env python
# -*- coding:Utf8 -*-


# Import objects from evaluation script
from Plotters.evaluation import *

# Keep trace of all plots with time
from datetime import datetime as dt

import os
import json

from json_decode import extract_nested_json2

########################
#### Main Program : ####
########################

# File to load
json_file = "D:\Github\solarsystem\Outputs\Plots_stock\Energy_sav" + \
            "\\dico_energy.json"

rows = ['January', 'February', 'March', 'April', 'May',
        'June', 'July', 'August', 'September', 'October',
        'November', 'December']

# Load json
with open(json_file, 'r', encoding='utf-8') as f:
    datas = json.load(f, object_pairs_hook=OrdD)

# Create structures to plots times
title = "Energy informations"
parameters = ("Appoint", "Besoins", "Pertes", "ECS", "Taux de couverture",
              "Consommations", "Energie solaire", "Chauffage")
cols = tuple(el for el in datas)
structs = {ind: el for ind, el in extract_nested_json2(datas, parameters,
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

# Update the last row of "Taux de couverture"
for col in cols:
    # Calculate new ratio
    frames["Taux de couverture"].ix[-1:,
                                    col] = (100 *
                                            frames["Energie solaire"].ix[-1:,
                                                                         col] /
                                            frames["Consommations"].ix[-1:,
                                                                       col])


# Add plot
Plot = MultiPlotter({}, nb_cols=2, nb_rows=2, colors=None,
                    title=title, sharex=True, sharey=False)
Plot.font_legend = {'size': 5,
                    'family': 'Anonymous Pro'}
Plot.fig_init(figsize=(24, 12))

Consommations = Plot.frame_plot(frames["Consommations"].ix[-1:, :], fields="all",
                                legend=False,
                                title='Consommations',
                                loc='left', kind="bar", pos=(0, 0))
couverture = Plot.frame_plot(frames["Taux de couverture"].ix[-1:, :], fields="all",
                             legend=False,
                             title='Couverture', ylim=(-10, 110),
                             loc='left', kind="bar", pos=(0, 1))
solaire = Plot.frame_plot(frames["Energie solaire"].ix[-1:, :], fields="all",
                          legend=False,
                          title='Energie solaire',
                          loc='left', kind="bar", pos=(1, 0))
appoint = Plot.frame_plot(frames["Appoint"].ix[-1:, :], fields="all",
                          legend=False,
                          title='Energie appoint',
                          loc='left', kind="bar", pos=(1, 1))

# Add ylabel to each plots
Plot.set_axes_label('KWh', pos=(0, 0), axe='y')
Plot.set_axes_label('%', pos=(0, 1), axe='y')
Plot.set_axes_label('KWh', pos=(1, 0), axe='y')
Plot.set_axes_label('KWh', pos=(1, 1), axe='y')
# Change legend alignement
Plot.catch_axes(*(1, 0)).legend(ncol=3)

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

simulation = "Simulation_energy"

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
