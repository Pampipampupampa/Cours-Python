# -*- coding:Utf8 -*-

"""
    Bar plot with modifiable data for. Each parameter can be fit with a specific field from
    json data file:
        - Bar width
        - Bar Height
        - Bar color
        - Bar top width label
    Bars sorted according to field define using color
"""

import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap, ColorConverter
from matplotlib.lines import Line2D
from matplotlib import ticker
from path import Path


def json_to_df(data_d, simulations, fields, month="Annual"):
    """
    Extract from *data_d* each field of *fields* for each simulation of
    *simulations* only for the *month* parameter.
    Return a `pandas.DataFrame` object where row index match *simulations* and **columns**
    match *fields*.

    :param data_d: A nested dict like object from where we want to extract data
    :param simulations: Name of simulation to extract
                        (must be in data_p.keys())
    :param fields: Fields to extract for each simulation
                   (must be in data_p[simulation][month].keys())
    :param month: Name of the month to extract
                  (must be in data_p[simulation].keys())
    """
    return pd.DataFrame({field: pd.Series(tuple((data_d[sim][month][field] for sim in simulations)),
                                          index=simulations)
                         for field in fields})


def interpolate(df_ref, label, thickness_variation=(0.25, 0.95)):
    """Function that interpolates linearly between hmin and hmax.

    :pram df_ref: A reference to the dataframe.
    :param label: The column to interpolate
    """
    hmin, hmax = thickness_variation
    xmin, xmax = min(df[label]), max(df[label])
    return [hmin + (hmax - hmin) * (x - xmin) / (xmax - xmin) for x in df[label]]


def create_gradiant(nbr_color, first=(0, 0, 0), last=(255, 255, 255)):
    """Linear extrapolation *nbr_color* from *first* to *last* color parameter
    to create a diverging colormap."""
    # Normalize color from RGB values
    first = [el / 255 for el in first]
    last = [el / 255 for el in last]
    return [tuple(f + (l - f) / nbr_color * el for (f, l) in zip(first, last)) for el in range(nbr_color)]


def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return LinearSegmentedColormap('CustomMap', cdict)


def diverge_map(high=(0.565, 0.392, 0.173), low=(0.094, 0.310, 0.635)):
    """
    Low and high are colors that will be used for the two
    ends of the spectrum.

    :param high: RGB color value
    :param low: RGB color value
    """
    c = ColorConverter().to_rgb
    return make_colormap([low, c('white'), 0.5, c('white'), high])


def month_mapper(month):
    """A hash table which return the corresponding value using *month* as item"""
    month = month.strip().lower()
    hash_table = {"jan": "Janvier", "feb": "Février", "mar": "Mars", "apr": "Avril",
                  "may": "Mai", "jun": "Juin", "jul": "Juillet", "aug": "Août",
                  "sept": "Septembre", "oct": "Octobre", "nov": "Novembre",
                  "dec": "Décembre", "annual": "Annuel", "heating season": "Octobre --> Mars"}
    return hash_table[month]


#
# LOAD DATA --------------------------------------------------------------------
#
# Folder to store plots
FOLDER = Path("D:/Github/solarsystem/Outputs/Plots_stock/No_automations/")
# File to load
json_file = Path("D:/Github/Projets/IGC/Etudes/Simulations_Air_Solaire_maisonIndividuelle/PreEtude2/Resultats/energy.json")
# Fields to extract
fields = ("Consommation\nappoint",          # Conso électrique
          "Production\nsolaire",            # Production solaire
          "Production_solaire\nvalorisée",  # Production solaire utile (sans les pertes)
          "Pertes réseau",                  # Pertes solaire
          "Couverture\nChauffage",        # Couverture chauffage
          "Couverture\nECS",              # Couverture ECS
          "Rendement solaire")              # Rapport absorbée / captable
# Month to extract (or annual values)
month = "Heating season"
# Load json file
with open(json_file, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Simulation to extract
# Capteurs
# simulations = ("limogesAir60Inc55T6M-4p", "limogesAir45Inc55T6M-4p", "strasbourgAir60Inc55T6M-4p",
#                "limogesAiSO55T6M-4p", "limogesAiSE55T6M-4p",
#                "limogesAir55T6M-6p", "limogesAir55T6M-8p", "limogesAir55T6M-4p",
#                "strasbourgAir55T6M-4p", "strasbourgAirSkyProS6M-4p", "strasbourgAirRadco308cS6M-4p")

# # Modification algorithm
# simulations = ("limogesAir240TempoElec55T6M-4p", "limogesAir120TempoElec55T6M-4p", "limogesAir55T6M-4p",
#                "limogesAir900TempoDebit55T6M-4p", "limogesAir300TempoDebit55T6M-4p", "limogesAir5Delta55T6M-4p",
#                "limogesAir15Delta55T6M-4p", "limogesAir55T6M90V90-4p", "limogesAir55T6MPasSurchauffe-4p")

# # Tank size variations
# simulations = ("bordeauxAir100ECS55T6M-4p", "bordeauxAir200ECS55T6M-4p", "bordeauxAir400ECS55T6M-4p",
#                "bordeauxAir100Tampon6M-4p", "bordeauxAir200Tampon6M-4p", "bordeauxAir400Tampon6M-4p",
#                "bordeauxAir55T6M-4p")

# # Inclinaison / Orientation
# simulations = ("limogesAiSO55T6M-4p", "limogesAiSE55T6M-4p",
#                "limogesAir60Inc55T6M-4p", "limogesAir45Inc55T6M-4p", "strasbourgAir60Inc55T6M-4p",
#                "strasbourgAirSkyProS6M-4p", "strasbourgAirRadco308cS6M-4p",
#                "limogesAir55T6M-4p", "strasbourgAir55T6M-4p")

# Load json into a dataframe
df = json_to_df(data_d=data, simulations=simulations, fields=fields, month=month)


#
# PREPARE DATA -----------------------------------------------------------------
#
# first_color, last_color = (238, 232, 213), (7, 54, 66)
first_color, last_color = (220, 200, 0), (211, 54, 130)
customcmap = create_gradiant(len(df), last_color, first_color)
alpha_value, alpha_text, alpha_box = 0.7, 0.9, 0.5
width_color, text_color = customcmap[len(customcmap) // 2], "#002b36"
top_bar_box_color = "#268bd2"
# Define all labels
title = 'Couverture ECS et Chauffage ({}) du système solaire en fonction des pertes'
title = title.format(month_mapper(month))
label_color_data = "Rendement des capteurs solaires [%]"
label_length_data = "Couverture ECS [%]"
label_width_data = "Couverture chauffage [%]"
label_top_bar_data = "(Production solaire valorisée / Consommation électrique) [kWh]"
# Define data location
length_data = "Couverture\nECS"
width_data = "Couverture\nChauffage"
color_data = "Rendement solaire"
top_bar_data = ("Production_solaire\nvalorisée", "Consommation\nappoint")
# Sort rows according to color_data (from lower to upper value)
df = df.sort_values(by=color_data, ascending=False)


#
# CREATE FIGURE AND POPULATE AXES ----------------------------------------------
#
# Bar height
h_min, h_mean, h_max = 12, 25, 38
# Create a figure of given size
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111)
fig.patch.set_facecolor("#eee8d5")
# Remove things ...
ax.grid(False)
ax.set_frame_on(False)
# Customize title, set position, allow space on top of plot for title
plt.subplots_adjust(top=0.8, left=0.16, right=1.025)
# Set x ticks ticker and labels on top
ticker_instance = ticker.MaxNLocator(10, integer=True)
ax.xaxis.set_major_locator(ticker_instance)
ax.xaxis.tick_top()
ax.xaxis.set_label_coords(0, 1.1)
ax.set_xlabel(label_length_data, fontsize=20, alpha=alpha_text, ha='left', color=text_color)
ax.xaxis.set_ticks_position('none')
# Customize y tick labels
yticks = [item.get_text() for item in ax.get_yticklabels()]
ax.set_yticklabels(yticks, fontsize=16, alpha=alpha_text, color=text_color)
ax.yaxis.set_tick_params(pad=12)
ax.yaxis.set_ticks_position('none')
# Add title
fig.suptitle(title, fontsize=26, color=text_color)
# Populate axes
df[length_data].plot(kind='barh', ax=ax, alpha=alpha_value, legend=False,
                     color=customcmap,
                     edgecolor='#eee8d5', xlim=(0, 100))
# Add lines to each xticks to help visualisation
# Must be call after plot to access ticks
ax.xaxis.grid(True)
for line in ax.xaxis.get_gridlines():
    line.set_color(text_color)
    line.set_linestyle('--')
    line.set_alpha(alpha_value / 4)
# Add specific height for each bar and top label of width data label
lengths = interpolate(df, label=width_data)
for container in ax.containers:
    # Each bar has a Rectangle element as child
    for i, rect in enumerate(container.get_children()):
        # Reset the lower left point of each bar so that bar is centered vertically
        rect.set_y(rect.get_y() - 0.125 + 0.5 - lengths[i] / 3)
        # Attribute height to each Recatangle according to heating cover
        plt.setp(rect, height=lengths[i])
        # Add aditionnal infos on the top of each bar
        text_inst2 = ax.text(rect.get_x() + rect.get_width() * (31 / 30),
                             rect.get_y() + rect.get_height() / 3,
                             "({:d} / {:d})".format(int(df[top_bar_data[0]][i]), int(df[top_bar_data[1]][i])),
                             color=text_color, fontsize=13)
        text_inst2.set_bbox(dict(facecolor=top_bar_box_color, alpha=alpha_box,
                                 edgecolor="none", boxstyle="round"))
        text_inst2.set_alpha(alpha_text)

# Add fake legend to understand the meaning of the height
l1 = Line2D([], [], linewidth=h_min, color=width_color, alpha=alpha_value)
l2 = Line2D([], [], linewidth=h_mean, color=width_color, alpha=alpha_value)
l3 = Line2D([], [], linewidth=h_max, color=width_color, alpha=alpha_value)
# Set three legend labels to be min, mean and max of heating coverage
zip_labels = zip(("min", "moy", "max"), (np.min(df[width_data]),
                                         np.average(df[width_data]),
                                         np.max(df[width_data])))
labels = ["{1:>4d}\n({0})".format(info, int(l)) for (info, l) in zip_labels]
# Position legend in lower right part
# Set ncol=3 for horizontally expanding legend
leg_right = ax.legend([l1, l2, l3], labels, ncol=3, frameon=False, fontsize=16,
                      bbox_to_anchor=[1.1, -0.01], handlelength=2, labelspacing=0.5,
                      handletextpad=2, columnspacing=4, title=label_width_data)
# Legend for bar top info
text_legend = ax.text(0, 0, label_top_bar_data, style='italic',
                      fontsize=16, alpha=alpha_text, horizontalalignment='center',
                      verticalalignment='center', transform=ax.transAxes,
                      bbox=dict(facecolor=top_bar_box_color, alpha=alpha_box,
                                edgecolor="none", boxstyle="round"))
text_legend.set_x(text_legend.get_position()[0] + 0.1)
text_legend.set_y(text_legend.get_position()[1] - 0.1)
# Change text color
for text in leg_right.get_texts():
    text.set_color(width_color)
    text.set_alpha(alpha_text)
# Customize legend title
# Set position to increase space between legend and labels
plt.setp(leg_right.get_title(), fontsize=20, alpha=alpha_text, color=width_color)
leg_right.get_title().set_position((0, 10))
# Customize transparency for legend labels
(plt.setp(label, alpha=alpha_text) for label in leg_right.get_texts())

# Create a fake reversed colorbar to go from few losses to a lot of losses (Hack)
# ctb = LinearSegmentedColormap.from_list('custombar', customcmap[-2:1:-1], N=1000)
ctb = LinearSegmentedColormap.from_list('custombar', customcmap[::-1], N=1000)
# Trick from http://stackoverflow.com/questions/8342549/
# matplotlib-add-colorbar-to-a-sequence-of-line-plots
min_losses, max_losses = np.min(df[color_data]), np.max(df[color_data])
sm = plt.cm.ScalarMappable(cmap=ctb, norm=plt.Normalize(vmin=min_losses, vmax=max_losses))
# Fake up the array of the scalar mappable
sm._A = []
# Set colorbar, aspect ratio
cbar = plt.colorbar(sm, alpha=alpha_value, shrink=0.6, pad=0.03, orientation="vertical")
cbar.solids.set_edgecolor("face")
cbar.outline.set_visible(False)    # Remove colorbar container frame
cbar.ax.tick_params(labelsize=16)  # Fontsize for colorbar ticklabels
# Colorbar label, customize fontsize and distance to colorbar
cbar.set_label(label_color_data, alpha=alpha_text, color=text_color,
               rotation=270, fontsize=20, labelpad=40)
cbar.ax.invert_yaxis()             # Reversed y ticks
cbar_yticks = [item.get_text() for item in cbar.ax.get_yticklabels()]
cbar.ax.set_yticklabels(cbar_yticks, color=text_color)
# Remove bar ticks from colorbars
cbarytks = plt.getp(cbar.ax.axes, 'yticklines')
plt.setp(cbarytks, visible=False)
# Draw on the screen
plt.show(block=True)
