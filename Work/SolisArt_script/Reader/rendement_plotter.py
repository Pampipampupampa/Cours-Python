#! /usr/bin/env python
# -*- coding:Utf8 -*-

"""
    Minimal script to plot bar plot with collector efficiency performances.
"""

# Import internal lib
from Plotters.evaluation import *

########################
#### Main Program : ####
########################


FOLDER = path("D:\Github\Projets\SolisArt\Faire\SolisArt\RendementActuel")
datas = {"chambery": FOLDER + "\\chambery_exp.csv", "bordeaux": FOLDER + "\\bordeaux_exp.csv",
         "marseille": FOLDER + "\\marseille_exp.csv"}
sep, index_col = ",", "Time"
fields = ["disponible", "captable", "absorbée"]
emphs = ["rendement"]
title = "Evolution du rendement des capteurs au cours de l’année pour \n"
colors = {'captable': '#fdf6e3', 'disponible': '#268bd2', 'absorbée': 'orange'}
short_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sept', 'Oct',
               'Nov', 'Dec']

# Collector specifications
# nb, surf = 6, 2.32

# Extract data
frames = {}
for data in datas:
    frames[data] = pd.read_csv(datas[data], sep=sep, encoding='utf-8',
                               index_col=index_col)
    frames[data].index = [el for el in range(1, 14)]
    # Remove annual datas before plotting
    frames[data] = frames[data].ix[:12, :]

    # KWh/m2 to KWh
    # frames[data][["absorbée", "captable", "disponible"]] = frames[data][["absorbée", "captable", "disponible"]] * (nb*surf)

############################# Plotter initializing #############################
Plot = MultiPlotter({}, nb_cols=2, nb_rows=2, colors=colors,
                    title=title, sharex=False, sharey=True)
Plot.font_legend = {'size': 18,
                    'family': 'Anonymous Pro'}
Plot.fig_init(figsize=(24, 12))

################################### Plotting ###################################
# First
Plot.bar_sup_plot(frames["chambery"], fields=fields, pos=(0, 0), title=title+"chambery",
                  ylabel="KWh", names=short_names)
percents = ['{:.1f} %'.format(i) for i in frames["chambery"]['rendement'].values]
Plot.change_xticks_labels([short_names, [' : '] * 12, percents], pos=(0, 0))

# Second
Plot.bar_sup_plot(frames["bordeaux"], fields=fields, pos=(0, 1), title=title+"bordeaux",
                  ylabel="KWh", names=short_names)
percents = ['{:.1f} %'.format(i) for i in frames["bordeaux"]['rendement'].values]
Plot.change_xticks_labels([short_names, [' : '] * 12, percents], pos=(0, 1))

# Third
Plot.bar_sup_plot(frames["marseille"], fields=fields, pos=(1, 0), title=title+"marseille",
                  ylabel="KWh", names=short_names)
percents = ['{:.1f} %'.format(i) for i in frames["marseille"]['rendement'].values]
Plot.change_xticks_labels([short_names, [' : '] * 12, percents], pos=(1, 0))


# Adjust plot format (avoid overlaps)
Plot.adjust_plots(hspace=0.6, wspace=0.15,
                  top=0.85, bottom=0.08,
                  left=0.05, right=0.96)
Plot.tight_layout()

# Save plotting informations to files
sav_plot(folder=path("D:\Github\Projets\SolisArt\Faire\SolisArt\RendementActuel"),
         base_name="_rendements", plotter=Plot, facecolor="white")

# Display plots
Plot.show()
