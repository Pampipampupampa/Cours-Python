# -*- coding:Utf8 -*-


"""
# Memo:
A sankey diagram is simply a weighted graph. Each node represent a head of a branch.
Each edge represent branches. Weight on each edge represent size of branch.

# Matplotlib integration:
    Draw a Sankey diagram of flows for Solar combi-system.
        :param flows: Scale each legs of diagram.
        :param labels: Add text to branches.
        :param label: Add a legend for diagram.
        :param patchlabel: Add a title on diagram.
        :param orientations: Choose position of branches.
        :param pathlengths: Size branches.
        :param trunklength: Size lenght of trunk of branches.
        :param prior: Choose another diagram to connect.
        :param connect: Choose where to connect both diagram (prior and current).

# How to:
Process to create a Sankey diagram.
Initialize an empty window with an axe (different from `axis`).
Create a Sankey instance.
Add sankey diagram with sankey.add method.
Used sankey.finish method to complete the diagram.
Define format.
Plot graph.
"""


import matplotlib.pyplot as plt
import matplotlib
from matplotlib.sankey import Sankey

# Configure matplotlib
font_base = {'size': 20,
             'family': 'Source Code Pro'}
font_title = {'size': 30,
              'family': 'Source Code Pro',
              'weight': 'bold'}
matplotlib.rcParams['backend.qt4'] = "PySide"
matplotlib.rc('font', **font_base)
matplotlib.rc('legend', fontsize=20)
matplotlib.rc('legend', labelspacing=0.5)

# Instanciate a sankey diagram without anything in it.
fig = plt.figure(figsize=(24, 12), facecolor="white",
                 edgecolor="#FFFFFF", frameon=True)
ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[])
# ax.set_title(label="Representation des flux du systeme solaire modelise.",
#              fontdict=font_title, loc='center')
sankey = Sankey(ax=ax, unit=None, head_angle=90, offset=0.25, shoulder=0.1)


# [0]
# Solar combi system part.
flows_system = [0.8, 0.2, -0.1, -0.1, -0.1, -0.4, -0.3, 0.1]
labels_system = ["Production\nsolaire", "Appoint\nElectrique", "Pertes\nechangeur", "Pertes\nlineiques",
                 "", "Production de chauffage", "Production\nECS", ""]
orientations_system = [0, 0, 1, 1, -1, 0, -1, 1]
pathlengths_system = [0.5, 0.5, 0.1, 0.6, 0.5, 0.3, 0.5, 0.5]
sankey.add(flows=flows_system, label='Systeme solaire', labels=labels_system, fc='orange',
           orientations=orientations_system, pathlengths=pathlengths_system,
           patchlabel="Systeme solaire\ncombine")


# [1]
# House part.
flows_house = [0.4, 0.3, 0.1, 0.1, 0.1, 0.1, -0.8, -0.1, -0.1]
labels_house = ["", "Gains\nSolaires", "", "Equipements", "Occupants", "Eclairage",
                "Besoins thermiques", "Surplus", ""]
orientations_house = [0, 1, -1, 1, 1, 1, 0, 1, -1]
pathlengths_house = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.2, 0.5, 0.5]
sankey.add(flows=flows_house, label='Maison', labels=labels_house, pathlengths=pathlengths_house,
           orientations=orientations_house, prior=0, connect=(5, 0), fc='#fdf6e3',
           patchlabel="Maison")

# [2]
# Stockage recuperation part.
labels_recup = ["Pertes\nStockage", "Apports\nStockage"]
sankey.add(flows=[0.1, -0.1], fc='#cb4b16', pathlengths=[0.5, 0.5], trunklength=2.15,
           orientations=[1, 1], prior=0, connect=(4, 0), labels=labels_recup,
           patchlabel="Recuperation")

# Recuperation of house air to reduce needed energy from solar and electrical prodction.
# Must used 2 diagram to be able to connect together house and system.
# 3 Used here to have more arrows.
# [3]
# Connection of [5] to system.
labels_recup = ["", "Recuperation sur\nair interieur"]
sankey.add(flows=[0.1, -0.1], fc='#cb4b16', pathlengths=[0.05, 0.5],
           trunklength=0.6,
           orientations=[0, -1], prior=0, connect=(7, 1), labels=labels_recup)
# [4]
# Connection of [0] to [5]
labels_recup = ["Recuperation sur\nair interieur", "Recuperation   "]
sankey.add(flows=[0.1, -0.10], fc='#cb4b16', pathlengths=[0.5, 2.9],
           orientations=[0, -1], prior=1, connect=(8, 0), labels=labels_recup)
# [5]
# Used to be able to draw recuperation air flow from house to system.
labels_recup = ["", ""]
sankey.add(flows=[0.1, -0.1], fc='#cb4b16', pathlengths=[3, 0.5],
           trunklength=3.65,
           orientations=[-1, -1], prior=3, connect=(0, 1), labels=labels_recup)


# Formatting.
diagrams = sankey.finish()
for diagram in diagrams:
    diagram.text.set_fontweight('bold')
    diagram.text.set_fontsize(30)
    for diag_text in diagram.texts:
        diag_text.set_color('black')

# Change color for recuperation.
diagrams[2].text.set_color('white')
diagrams[4].texts[1].set_color('white')
diagrams[4].texts[1].set_fontsize(30)
diagrams[4].texts[1].set_fontweight('bold')

# Plot diagram.
# Adjust plot format (avoid overlaps)
fig.subplots_adjust(hspace=0, wspace=0,
                    top=0.95, bottom=0,
                    left=0, right=1)
# fig.legend(loc='best')
fig.tight_layout()

# Save the figure.
fig.savefig('sankey_diagram.png', facecolor="white",  edgecolor="white", dpi=400,
            bbox_inches='tight', pad_inches=-0.9)
fig.savefig('sankey_diagram.svg', facecolor="white",  edgecolor="white", dpi=400,
            bbox_inches='tight', pad_inches=-0.9)
fig.savefig('sankey_diagram.pdf', facecolor="white",  edgecolor="white", dpi=400,
            bbox_inches='tight', pad_inches=-0.9)

# Show it on screen.
plt.show()
