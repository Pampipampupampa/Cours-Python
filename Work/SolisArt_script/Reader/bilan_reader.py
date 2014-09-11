#! /usr/bin/env python
# -*- coding:Utf8 -*-

"""
    Used to plot barplot, diag_Bplot, boxplot, simple plot, ...
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

# Bar emphazis
emphs_dict = {'bar_cumA': ["Pertes"],
              'bar_cumC': ["Energie solaire"],
              'bar_sup': ["Energie solaire"]}

# Fields (to plot new type of graph add new fields here)
fields = {'box_T': ['T3', 'T4', 'T5'],
          'box_H': ['Diffus', 'Direct'],
          'diag_B': [["Energie solaire", "Appoint", "Chauffage", "ECS"],
                     ['Chauffage', 'ECS', 'Pertes']],
          'diag_C': [["Energie solaire", "Appoint", "Chauffage", "ECS"],
                     ["Energie solaire", "Appoint"]],
          'bar_cumC': [["Energie solaire", "Appoint", "Chauffage", "ECS"],
                       ["ECS", "Chauffage", "Pertes"]],
          'bar_cumA': [["Energie solaire", "Appoint", "Chauffage", "ECS"],
                       ["Energie solaire", "Appoint"]],
          'bar_sup': [["Energie solaire", "Appoint", "Chauffage", "ECS"],
                      ["ECS", "Chauffage", "Pertes"]],
          'area_E': ["ECS", "Energie solaire", "Chauffage"],
          'line_E': ["ECS", "Energie solaire", "Appoint", "Chauffage"],
          'line_T1': ["T1", "T3", "T4", "T5"],
          'line_T2': ["T12_house", "Text"],
          'line_H': ['Diffus', 'Direct'],
          'line_debA': ["Flow_S6", "Flow_S5", "Flow_S4", "Flow_S2"],
          'line_debS1': ["Flow_S6", "Flow_S5"],
          'line_debC1': ["Flow_S4", "Flow_S2"],
          'line_debS2': ["Flow_Collector", "Flow_ExchTank_bot",
                         "Flow_ExchStorTank"],
          'line_debC2': ["Flow_ExchTank_top", "Flow_Boiler"]}

# Colors
col_dict = {'box': (('#268bd2', '#002b36', '#268bd2', '#268bd2', '#268bd2'),
                    ('#586e75', '#002b36', '#586e75', '#586e75', '#268bd2'),
                    ('#859900', '#002b36', '#859900', '#859900', '#268bd2')),
            'diag_B': ['#fdf6e3', '#268bd2', '#cb4b16'],
            'diag_C': ['#fdf6e3', '#268bd2'],
            'bar_cumA': {"Appoint": "#fdf6e3", "Energie solaire": "orange",
                         "Pertes": "#cb4b16"},
            'bar_cumC': {"Appoint": "#dc322f", "Chauffage": "#fdf6e3",
                         "ECS": "#268bd2", "Energie solaire": "orange",
                         "Pertes": "#cb4b16"},
            'bar_sup': {"Appoint": "#dc322f", "Chauffage": "#fdf6e3",
                        "ECS": "#268bd2", "Energie solaire": "orange",
                        "Pertes": "#cb4b16"},
            'area_E': "Accent", 'line_E': "Accent", 'line_T1': "Accent",
            'line_T2': "Accent", 'line_H': "Accent", 'line_debA': "Accent",
            'line_debS1': "Accent", 'line_debC1': "Accent",
            'line_debS2': "Accent", 'line_debC2': "Accent"}

# Titles
titles = {'title': "Bilan de la simulation",
          'box_T': "Evolution mensuel de la variation \n" +
                   "des températures des ballons",
          'box_H': "Evolution mensuel de la variation \n" +
                   "de la puissance captée",
          'diag_B': "Taux de couverture",
          'diag_C': "Répartition des consommations",
          'bar_cumA': "Evolution mensuel des apports",
          'bar_cumC': "Evolution mensuel des consommations d'énergie",
          'bar_sup': "Evolution mensuel des apports et consommations d'énergie",
          'area_E': "Evolution annuelle de la consommation en énergie",
          'line_E': "Evolution annuelle de la consommation en énergie",
          'line_T1': "Evolution annuelle des températures dans les ballons " +
                    "\net de la température en sortie des panneaux solaires",
          'line_T2': "Evolution annuelle de la température intérieure " +
                    "\net extérieure",
          'line_H': "Evolution annuelle de la puissance captée",
          'line_debA': "Evolution des débits solaires et de chauffage",
          'line_debS1': "Evolution des débits solaires",
          'line_debC1': "Evolution des débits de chauffage",
          'line_debS2': "Evolution des débits des équipements solaire",
          'line_debC2': "Evolution des débits des équipements de chauffage"}


# Change data columns names
conv_dict = {"DrawingUp_Energy": "ECS", "Radiator_Energy": "Chauffage",
             "Collector_Energy": "Energie solaire",
             "Boiler_Energy": "Appoint",
             "HDifTil_collector": "Diffus", "HDirTil_collector": "Direct"}

# New fields
new_fields = (("Besoins", "ECS", "Chauffage", "+"),
              ("Consommations", "Energie solaire", "Appoint", "+"),
              ("Pertes", "Consommations", "Besoins", "-"),
              ("Taux de couverture", "Energie solaire", "Consommations", "/"),
              ("Part solaire", "Energie solaire", "Appoint", "/"))

# Prepare Taux de couverture (list of formatted datas)
short_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sept', 'Oct',
               'Nov', 'Dec']

# Test
# _ chambery_20140630.csv marseille_20140630.csv strasbourg_20140707.csv
# row bar_cumC bar_cumC bar_cumC,bar_sup
# _ chambery3p_20140802.csv chambery_20140825.csv
# chambery9p_20140821.csv chambery12p_20140802.csv chamberyNosun_20140908.csv
# all all box_T box_T box_T box_T
# all all box_H box_H box_H box_H
# none all bar_cumC bar_cumC bar_cumC bar_cumC
# none none diag_B diag_B diag_B diag_B
# all all area_E area_E area_E area_E
# none none box_T,box_H,bar_cumC,area_E,line_E,diag_B
# all none line_debS,line_debC,line_H,line_T1
# all none line_debS1,line_debS2,line_debC1,line_debC2

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
        names = ["_", "chambery_20140825.csv"]
        print("---> Defaults will be used : \n{}".format(names))

    sep = names.pop(0)  # Recup separator value

    # Define how and what to plot
    field_print = " ".join(field_ for field_ in fields.keys())
    welcome = "\nPlease choose kind of plot for each dataframes or default " + \
              "(press enter) :\n" + \
              "({})\n".format(field_print) + \
              "    -" + " space to select next dataframe\n" + \
              "    -" + " comma to asign multiple plot to one dataframe\n" + \
              "    -" + " first/second element used to select correct" + \
              "x/y axis share\n" + \
              "      ('all', 'row', 'col' or 'none')\n"
    # Print plots informations and user input choice
    print("\n", "-"*30, "All plots available :", "-"*30, sep="\n")
    nb_fill = 10
    for plot_disp in sorted(fields.keys()):
        definition = titles[plot_disp].replace("\n", "\n" + " "*(nb_fill+3))
        print("{0:{fill}{align}{nb_fill}} : {1}\n".format(plot_disp, definition,
                                                          fill=" ", align="<",
                                                          nb_fill=nb_fill))
    # Limit plots list to number of dataframe + parameters (axis sharing)
    nb_name = len(names)
    plots = input(welcome).split(" ")[:nb_name + 2]
    # Default instructions
    if plots == [""]:
        plots = ['none', 'none',
                 "box_T,diag_B,box_H,bar_cumC,bar_cumA,diag_C,area_E"]
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
    print("\n---> Template : ")
    print(structs)

    # Read csvs and store values as a dict
    frames = read_csv(dataframes,
                      convert_index=(convert_to_datetime,)*nb_name,
                      delimiter=(";",)*nb_name,
                      index_col=("Date",)*nb_name,
                      in_conv_index=(None,)*nb_name,
                      skiprows=(1,)*nb_name,
                      splitters=(sep,)*nb_name)

    #
    ################## EvalData class : Prepare datas ##################
    #
    # Keep only 2014 datas into the dict
    datas = {name: EvalData(EvalData.keep_year(frames[name])) for name in frames}
    for name in datas:
        # Change columns names
        datas[name].frame.columns = datas[name].change_names(conv_dict)
        print("\n\n", "\t"*7, "*** {} ***".format(name.upper()))
        print("\n---> Csv columns names after treatments")
        print(datas[name].frame.columns)
        print("\n---> index range : ", datas[name].frame.index[0],
              "\tto\t", datas[name].frame.index[-1])
        chauff_sol, _ = datas[name].col_sum_map(datas[name].frame[["S2_state",
                                                                   "Vsolar_state",
                                                                   "Vextra_state"]],
                                                debug=False,
                                                cols_map=["S2_state",
                                                          "Vsolar_state",
                                                          "Vextra_state"],
                                                match_map=(100, 100, 100),
                                                start_sum=datas[name].frame.index[0])
        chauff_app, _ = datas[name].col_sum_map(datas[name].frame[["S2_state",
                                                                   "Vsolar_state",
                                                                   "Vextra_state"]],
                                                debug=False,
                                                cols_map=["S2_state",
                                                          "Vextra_state"],
                                                match_map=(100, 0),
                                                start_sum=datas[name].frame.index[0])
        print("\n---> Chauffage solaire annuel de {} : {}".format(name,
                                                                  chauff_sol))
        print("\n---> Chauffage appoint annuel de {} : {}".format(name,
                                                                  chauff_app))
        # Time soustraction : Be careful^^
        if chauff_app > chauff_sol:
            print("Difference : {}".format(chauff_app - chauff_sol))
        else:
            print("Difference : {}".format(chauff_sol - chauff_app))
        try:
            ratio = 100 * chauff_sol / (chauff_app + chauff_sol)
            print("Ratio : {}".format(ratio))
        except ZeroDivisionError as e:
            print(e, "ratio : 0", sep="\n")

        # Add all plot for each set of datas
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
                                                      sample='30min')
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
            value = "{} plot position: ".format(plot)
            pos = test_index(name, plot)
            print(pos)
            if "bar" in plot:
                Plot.colors = col_dict[plot]
                print(structs[name][plot][0])
                if "cum" in plot:
                    Plot.bar_cum_plot(structs[name][plot][0],
                                      emphs=emphs_dict[plot],
                                      pos=pos, fields=fields[plot][1],
                                      loc='center',
                                      names=structs[name][plot][1],
                                      title=titles[plot]+"\n{}".format(name_cap))
                elif "sup" in plot:
                    Plot.colors = col_dict[plot]
                    print(structs[name][plot][0])
                    Plot.bar_sup_plot(structs[name][plot][0],
                                      emphs=emphs_dict[plot],
                                      pos=pos, fields=fields[plot][1],
                                      loc='center',
                                      names=structs[name][plot][1],
                                      title=titles[plot]+"\n{}".format(name_cap))
                # Each xticks = short month name +
                # Taux de couverture de couverture solaire mensuelle
                percents = ['{:.1%}'.format(i)
                            for i in
                            structs[name][plot][0]['Taux de couverture'].values]
                Plot.change_xticks_labels([short_names, [' : ']*12, percents],
                                          pos=pos)
                # Uncomment to set a y limit for each bar_cum plot
                # Plot.catch_axes(*pos).set_ylim(0, 2500)
            elif "box" in plot:
                Plot.colors = col_dict['box']
                Plot.boxes_mult_plot(structs[name][plot], pos=pos,
                                     patch_artist=True, loc='center',
                                     title=titles[plot]+"\n{}".format(name_cap))
            elif "diag" in plot:
                Plot.colors = col_dict[plot]
                explode = [0.1]  # Initial value for explode
                # To have len() matching between explode and fields[plot][1]
                while len(explode) < len(fields[plot][1]):
                    explode.append(0.0)
                # Add specific title for diag_B
                if "diag_B" in plot:
                    frame = structs[name][plot]
                    columns = frame.columns
                    p_title = "{1} : {0:.2%}".format(frame.get_value(titles[plot],
                                                                     columns[0]),
                                                     titles[plot])
                else:
                    p_title = titles[plot]
                a = fields[plot][1]
                b = (" ({:.0f} KWh)".format(structs[name][plot].ix[el, :1].values[0]) for el in a)
                # Create a list of string composed of a and b
                parts = ["".join(str(i) for i in el) for el in zip(a, b)]
                Plot.diag_plot(structs[name][plot], pos=pos, loc='center',
                               to_diag=fields[plot][1], legend=False,
                               title=p_title, labels=parts,
                               explode=explode)
                label = Plot.catch_axes(*pos).get_title()+"\n{}".format(name_cap)
                Plot.catch_axes(*pos).set_title(label=label,
                                                fontdict=Plot.font_title)
            elif any(c in plot for c in ("area", "line")):
                Plot.frame_plot(structs[name][plot], fields=fields[plot],
                                title=titles[plot]+"\n{}".format(name_cap),
                                pos=pos, loc='center',
                                linewidth=2, kind=plot.split("_")[0])
            else:
                print("Nothing will be show for {}".format(plot))

    # Adjust plot format (avoid overlaps)
    Plot.adjust_plots(hspace=0.6, top=0.85, left=0.05)
    # Removes empty axes (only last one for now)
    Plot.clean_axes(sum_)
    # Display plots
    Plot.show()
