# -*- coding:Utf8 -*-

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import datetime


def convert_to_datetime(steps, start=datetime.datetime(2014, 1, 1)):
    """
      This parser convert to a real datetime format
    """
    for el in steps:
        yield start + datetime.timedelta(seconds=int(el))


# Font used inside plots
font_legend = {'size': 20,
               'family': 'Source Code Pro'}
font_base = {'size': 30,
             'family': 'Source Code Pro'}
# Change matplotlib default settings
matplotlib.rcParams['backend.qt4'] = "PySide"
matplotlib.rc('font', **font_base)
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)
matplotlib.rc('legend', labelspacing=0.1)

# Load dataframe and structure it.
file_path = "D:\\Github\\Projets\\IGC\\Etudes\\Simulations_Air_Solaire_maisonIndividuelle\\" + \
            "Simulations\\Résultats\\IGC_airVectorRecyclePassive_solar6\\" + \
            "regulation_test_data_clean.csv"
frame = pd.read_csv(file_path, sep=";", encoding="utf-8", index_col="Date", skiprows=1)
frame = frame[:][:2678400]
# Datetime index.
frame.index = [ind for ind in convert_to_datetime(frame.index)]
# Reduce data structure and remove duplicated values
frame = frame.groupby(frame.index).last()
# Change column names.
frame.columns = ["Température de consigne solaire", "Température de consigne",
                 "Température intérieure", "Température de soufflage",
                 "Chauffage électrique autorisé", "Température extérieure", "Chauffage solaire autorisé"]


# Prepare 3 axes and draw on it.
fig, axes = plt.subplots(nrows=3, ncols=1,
                         sharex='all', sharey=False,
                         figsize=(24, 12), facecolor="white",
                         edgecolor="#FFFFFF", frameon=True)
frame[["Température de consigne solaire", "Température de consigne",
       "Température intérieure"]].plot(ax=axes[0], kind="line", legend=True,
                                       color=("orange", "#dc322f", "#268bd2"),
                                       linewidth=4)
axes[0].set_ylabel(ylabel="°C", labelpad=20)
frame[["Chauffage solaire autorisé",
       "Chauffage électrique autorisé"]].plot(ax=axes[1], kind="area", legend=True, color=("orange", "#dc322f"),
                                              linewidth=1, stacked=True)
axes[1].set_ylabel(ylabel="0 == Faux\n1 == Vrai", labelpad=20)
frame[["Température extérieure",
       "Température de soufflage"]].plot(ax=axes[2], legend=True, color=("#073642", "#859900"),
                                         linewidth=4)
axes[2].set_ylabel(ylabel="°C", labelpad=20)

# Change format.
for axe in axes:
    legend = axe.legend(prop=font_legend, loc='best')
    # Set the linewidth of each legend object
    for legobj in legend.legendHandles:
        legobj.set_linewidth(5)
fig.tight_layout()
fig.subplots_adjust(hspace=0.1)

# Save the figure.
# fig.savefig('sankey_diagram.png', facecolor="white",  edgecolor="white", dpi=400,
#             bbox_inches='tight', pad_inches=-0.9)
# fig.savefig('sankey_diagram.svg', facecolor="white",  edgecolor="white", dpi=400,
#             bbox_inches='tight', pad_inches=-0.9)
# fig.savefig('sankey_diagram.pdf', facecolor="white",  edgecolor="white", dpi=400,
#             bbox_inches='tight', pad_inches=-0.9)

# Show it on screen.
plt.show()
