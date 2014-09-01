#! /usr/bin/env python
# -*- coding:Utf8 -*-

"""
    Used to plot barplot, diagplot, boxplot, simple plot, ...
    Basic actions can be easily done on annual data like prepare data
    for boxplotting.

    Terminal interface used to print specific plots :
        - positions
        - axes sharing
        - type of plot
        - number of dataframes useds names
        - how to cut file (used after as dict keys)
"""

# Import objects from evaluation script
from Plotters.evaluation import *


def test_index(name, plot):
    """
        Recursive loop to check index value user input.
        Does not yet raise Value
    """
    flag = False
    while not flag:
        try:
            index = tuple(el for el in map(int, input(value).split(" ")))
            if len(index) != 2:
                raise IndexError
            Plot.catch_axes(*index)
            flag = True
        except (IndexError, ValueError) as e:
            print(e)
    return index

########################
#### Main Program : ####
########################

# Select directory
fold = FOLDER / "clean"

# Fields (to plot new type of graph add new fields here)
fields = {'box_T': ['T3', 'T4', 'T5'],
          'box_H': ['Diffus', 'Direct'],
          'diag': [["Energie solaire", "Appoint", "Chauffage", "ECS"],
                   ['Chauffage', 'ECS', 'Pertes']],
          'bar_cum': [["Energie solaire", "Appoint", "Chauffage", "ECS"],
                      ["ECS", "Chauffage", "Pertes"]],
          'bar_sup': [["Energie solaire", "Appoint", "Chauffage", "ECS"],
                      ["ECS", "Chauffage", "Pertes"]],
          'area_E': ["ECS", "Energie solaire", "Chauffage"],
          'line_E': ["ECS", "Energie solaire", "Appoint", "Chauffage"]}
# Colors
col_dict = {'box': (('#268bd2', '#002b36', '#268bd2', '#268bd2', '#268bd2'),
                    ('#586e75', '#002b36', '#586e75', '#586e75', '#268bd2'),
                    ('#859900', '#002b36', '#859900', '#859900', '#268bd2')),
            'diag': ['#fdf6e3', '#268bd2', '#cb4b16'],
            'bar_cum': {"Appoint": "#dc322f", "Chauffage": "#fdf6e3",
                        "ECS": "#268bd2", "Energie solaire": "orange",
                        "Pertes": "#cb4b16"},
            'bar_sup': {"Appoint": "#dc322f", "Chauffage": "#fdf6e3",
                        "ECS": "#268bd2", "Energie solaire": "orange",
                        "Pertes": "#cb4b16"},
            'area_E': "Accent",
            'line_E': "Accent"}
# Titles
titles = {'title': "Bilan de la simulation",
          'box_T': "Evolution mensuel de la variation des températures des ballons",
          'box_H': "Evolution mensuel de la variation de la puissance captable",
          'diag': "Taux de couverture",
          'bar_cum': "Evolution mensuel des apports et consommations d'énergie",
          'bar_sup': "Evolution mensuel des apports et consommations d'énergie",
          'area_E': "Evolution annuelle de la consommation en énergie",
          'line_E': "Evolution annuelle de la consommation en énergie"}


# Change data columns names
conv_dict = {"DrawingUp_Energy": "ECS", "Radiator_Energy": "Chauffage",
             "Collector_Energy": "Energie solaire",
             "Boiler_Energy": "Appoint",
             "HDifTil_collector": "Diffus", "HDirTil_collector": "Direct"}

# New fields
new_fields = (("Besoins", "ECS", "Chauffage", "+"),
              ("Consommations", "Energie solaire", "Appoint", "+"),
              ("Pertes", "Consommations", "Besoins", "-"),
              ("Taux de couverture", "Energie solaire", "Consommations", "/"))

# Prepare Taux de couverture (list of formatted datas)
short_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sept', 'Oct',
               'Nov', 'Dec']

# Test
# _ chambery_30062014.csv marseille_30062014.csv strasbourg_07072014.csv
# row bar_cum bar_cum bar_cum,bar_sup
# _ chambery3p_02082014.csv chambery_25082014.csv chambery9p_21082014.csv chambery12p_02082014.csv
# all all box_T box_T box_T box_T
# all all box_H box_H box_H box_H
# none none bar_cum bar_cum bar_cum bar_cum
# none none diag diag diag diag
# all all area_E area_E area_E area_E
# none none box_T,box_H,bar_cum,area_E,line_E,diag

if __name__ == '__main__':
    # Dynamic selection of multiple csv with specific separator
    dataframes = []
    # Define dataframe to load
    welcome = "Please choose csv files name inside this folder or default " + \
              "(press enter) :\nFolder = {} ".format(fold) + \
              "(first element must be the separator)\n"
    names = input(welcome).split(" ")

    # Default instructions
    if names == [""]:
        names = ["_", "strasbourg_07072014.csv"]
        print("---> Defaults will be used : \n{}".format(names))

    sep = names.pop(0)  # Recup separator value

    # Define how and what to plot
    field_print = " ".join(field_ for field_ in fields.keys())
    welcome = "\nPlease choose kind of plot for each dataframes or default " + \
              "(press enter) :\n" + \
              "({})\n".format(field_print) + \
              "    -" + " space pass to next dataframe\n" + \
              "    -" + " comma to asign multiple plot to one dataframe\n" + \
              "    -" + " first/second element used to select correct x/y axis share\n" + \
              "      ('all', 'row', 'col' or 'none')\n"
    plots = input(welcome).split(" ")

    # Default instructions
    if plots == [""]:
        plots = ['none', 'none', "box_T,diag,box_H,bar_cum"]
        print("---> Defaults will be used : \n{}".format(plots))
    share_x = plots.pop(0)  # Recup sharex flag
    share_y = plots.pop(0)  # Recup sharey flag
    for plot in range(len(plots)):
        plots[plot] = plots[plot].split(",")

    # Extract flags used inside dicts
    for ind, name in enumerate(names):
        dataframes.append(fold / name)
        names[ind] = name.split(sep)[0]
    structs = dict(zip(names, plots))
    # Split plot for each dataframes
    for el in structs:
        structs[el] = dict(zip(structs[el], [None]*len(structs[el])))
    # Dict of dict used to setup graphs
    print(structs)

    # Read csvs and store values as a dict
    frames = read_csv(dataframes,
                      convert_index=(convert_to_datetime,)*10,
                      delimiter=(";",)*10,
                      index_col=("Date",)*10,
                      in_conv_index=(None,)*10,
                      skiprows=(1,)*10,
                      splitters=(sep,)*10)

    #
    ################## EvalData class : Prepare datas ##################
    #

    # Memo
    # Check here if wrong data order (mix between dicts : frames and structs)
    datas = {name: EvalData(frames[name]) for name in frames}

    print("\n---Csv columns names after treatments---"),
    for name in datas:
        # Change columns names
        datas[name].frame.columns = datas[name].change_names(conv_dict)
        print("{} :\n ---> ".format(name), datas[name].frame.columns)
        # Add all plot for each set of datas
        # Multiple plot
        for el in structs[name]:
            if "bar" in el:
                structs[name][el] = (datas[name].bar_energy_actions(datas[name].frame,
                                                                    new_fields=new_fields,
                                                                    fields=fields[el][0]))
            elif "box" in el:
                structs[name][el] = (datas[name].box_actions(datas[name].frame,
                                                             fields=fields[el]))
            elif "diag" in el:
                structs[name][el] = (datas[name].diag_energy_actions(datas[name].frame,
                                                                     new_fields=new_fields,
                                                                     fields=fields[el][0]))
            elif any(c in el for c in ("area", "line")):
                structs[name][el] = EvalData.resample(frame=datas[name].frame,
                                                      sample='6h')
    # Only display to have a pretty interface
    print("\n|\n|\n|--> Class creation now finish, plotting datas\n")

    #
    ################## MultiPlotter class : Plot datas ##################
    #
    add = " -- ".join(data for data in datas)
    title = titles['title'] + " pour les données de\n" + add

    # Checks axes number and print map position
    sum_ = len([x for i in plots for x in i])
    print("Number of plots : {}".format(sum_))
    rows, cols = to_table(sum_)
    print("columns : {}\t rows : {}".format(cols, rows))
    print("-"*30, "Mapping of positions coordinates:", "-"*30, sep="\n")
    for row in range(rows):
        print("\n")
        for col in range(cols):
            print("({}, {})".format(row, col), end=" ")
    print("\n")

    Plot = MultiPlotter({}, nb_cols=cols, nb_rows=rows, colors=None,
                        title=title, sharex=share_x, sharey=share_y)
    Plot.fig_init()
    Plot.figure_title()

    # Flag on ---> add dataframe name, flag off ---> add nothing
    if len(set(names)) > 1:
        flag = True
    else:
        # Add nothing
        flag = False
        name_cap = ""
    for name in names:
        if flag:
            name_cap = name.capitalize()
        for plot in structs[name]:
            print("\n" + "-"*30)
            print("{} datas.\n{}".format(name.capitalize(), "-"*30))
            value = "{} plot position: ".format(plot.capitalize())
            pos = test_index(name, plot)
            print(pos)
            if "bar_cum" in plot:
                Plot.colors = col_dict["bar_cum"]
                print(structs[name][plot][0])
                Plot.bar_cum_plot(structs[name][plot][0], emphs=['Energie solaire'],
                                  pos=pos, fields=fields[plot][1], loc='center',
                                  names=structs[name][plot][1],
                                  title=titles[plot]+"\n{}".format(name_cap))
                # Each xticks = short month name + Taux de couverture de couverture solaire mensuelle
                percents = ['{:.1%}'.format(i) for i in structs[name][plot][0]['Taux de couverture'].values]
                Plot.change_xticks_labels([short_names, [' : ']*12, percents],
                                          pos=pos)

                # # Uncomment to set a y limit for each bar_cum plot
                # Plot.catch_axes(*pos).set_ylim(0, 2500)

            elif "bar_sup" in plot:
                Plot.colors = col_dict["bar_sup"]
                print(structs[name][plot][0])
                Plot.bar_sup_plot(structs[name][plot][0], emphs=['Energie solaire'],
                                  pos=pos, fields=fields[plot][1], loc='center',
                                  names=structs[name][plot][1],
                                  title=titles[plot]+"\n{}".format(name_cap))

                # Each xticks = short month name + Taux de couverture de couverture solaire mensuelle
                percents = ['{:.1%}'.format(i) for i in structs[name][plot][0]['Taux de couverture'].values]
                Plot.change_xticks_labels([short_names, [' : ']*12, percents],
                                          pos=pos)
            elif "box" in plot:
                Plot.colors = col_dict["box"]
                Plot.boxes_mult_plot(structs[name][plot], pos=pos,
                                     patch_artist=True, loc='center',
                                     title=titles[plot]+"\n{}".format(name_cap))
            elif "diag" in plot:
                Plot.colors = col_dict["diag"]
                a = fields[plot][1]
                b = (" ({:.0f}KWh)".format(structs[name][plot].ix[el, :1].values[0]) for el in a)
                # Create a list of string composed of a and b
                parts = ["".join(str(i) for i in el) for el in zip(a, b)]
                Plot.diag_plot(structs[name][plot], pos=pos, loc='center',
                               to_diag=fields[plot][1], legend=False,
                               title=titles[plot], labels=parts)
                label = Plot.catch_axes(*pos).get_title()+"\n{}".format(name_cap)
                Plot.catch_axes(*pos).set_title(label=label,
                                                fontdict=Plot.font_title)
            elif any(c in plot for c in ("area", "line")):
                Plot.frame_plot(structs[name][plot], fields=fields[plot],
                                title=titles[plot], pos=pos, loc='center',
                                linewidth=2, kind=plot.split("_")[0])
            else:
                print("Nothing will be show for {}".format(plot))

    # Adjust plot format
    Plot.adjust_plots(hspace=0.3, top=0.85, left=0.05)
    # Removes empty axes (only last one for now)
    Plot.clean_axes(sum_)
    # Display plots
    Plot.show()
