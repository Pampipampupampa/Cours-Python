#! /usr/bin/env python
# -*- coding:Utf8 -*-

"""
    Used to plot barplot, diag_plot, boxplot, simple plot, ...
    Basic actions can be easily done on annual data like prepare data
    for boxplotting.

    Terminal interface used to print specific plots :
        - positions
        - axes sharing
        - type of plot
        - number of dataframes useds names
        - how to cut file (used after as dict keys)
        - new columns create by existing columns operations
        - temporary renaming (only during script execution)
        - Storing data to json/csv (Energy and working time already implement)

    To use this script with csv files older than 2015 you have to make some change
    to fields, conv_dict and new_fields dictionnary or take a script older commit
    before 2015 (see github repository or git fonctionnality for more details)
"""

# import csv
# import json

# Import internal lib
from Plotters.evaluation import *


def test_index(name, plot):
    """
        Recursive loop to check index value user input.
        Does not yet raise Value
    """
    flag = False
    while not flag:
        try:
            index = tuple(el for el in map(int, input(value).split(' ')))
            if len(index) != 2:
                raise IndexError
            Plot.catch_axes(*index)
            flag = True
        except (IndexError, ValueError) as e:
            print(e)
    return index


def time_info(frame, display=True):
    """
        frame must be an instance of EvalData class.
        if display is True :
          ---> print time informations about the frame simulation result.
        Return a dict of all time informations.
    """
    time_dict = OrdD()
    # Recup solar heating time
    chauff_sol, _ = frame.col_sum_map(frame.frame,
                                      debug=False,
                                      cols_map=['S2_state',
                                                'Vsolar_state',
                                                'Vextra_state'],
                                      match_map=(100, 100, 100),
                                      start_sum=frame.frame.index[0])
    # ##########################################################################
    # ##########################################################################
    # Recup solar time TEST
    sol, _ = frame.col_sum_map_test(frame.frame,
                                    debug=False,
                                    cols_map=["Flow_Collector",
                                              "Vsolar_state"],
                                    start_sum=frame.frame.index[0])
    # ##########################################################################
    # ##########################################################################

    # Recup extra heating time
    chauff_app, _ = frame.col_sum_map(frame.frame,
                                      debug=False,
                                      cols_map=['S2_state',
                                                'Vextra_state'],
                                      match_map=(100, 0),
                                      start_sum=frame.frame.index[0])
    # Populate the time_dict
    time_dict['start_sim'] = frame.frame.index[0]
    time_dict['end_sim'] = frame.frame.index[-1]
    time_dict['heating_time'] = chauff_app + chauff_sol
    time_dict['solar_heating'] = chauff_sol
    time_dict['extra_heating'] = chauff_app
    time_dict['solar_working'] = sol
    if chauff_app > chauff_sol:
        time_dict['Difference'] = chauff_app - chauff_sol
    else:
        time_dict['Difference'] = chauff_sol - chauff_app
    try:
        ratio = 100 * chauff_sol / (chauff_app + chauff_sol)
        time_dict['ratio'] = ratio
    except ZeroDivisionError:
        time_dict['ratio'] = 0
    # Display time informations
    if display is True:
        for key, item in time_dict.items():
            print('\n---> {} : {}'.format(key, item))
    return time_dict


def prepare_export(dico, name):
    """
        Change format to prepare export to csv or json.
    """
    to_seconds = ('heating_time', 'extra_heating', 'solar_heating',
                  'Difference', 'solar_working')
    dico[name][m_]['start_sim'] = str(dico[name][m_]['start_sim'])
    dico[name][m_]['end_sim'] = str(dico[name][m_]['end_sim'])
    for conv in to_seconds:
        dico[name][m_][conv] = dico[name][m_][conv].total_seconds()


########################
#### Main Program : ####
########################

# Select directory
fold = FOLDER / 'clean'

# Bar emphazis
emphs_dict = {'bar_cumA': ['Pertes réseau'],
              'bar_cumC': ['Energie solaire'],
              'bar_supC': ['Energie solaire'],
              'bar_supDispo': []}

# Fields (to plot new type of graph add new fields here)
fields = {'box_Tbal': ['T3', 'T4', 'T5'],
          'box_Tint': ['T9_ext', 'T1', 'T12_house'],
          'box_H': ['Diffus', 'Direct'],
          'box_HDir': ['HDirNor', 'Direct'],
          'box_P': ['Flow_S6', 'Flow_S5', 'Flow_S4'],
          'diag_B': [['Energie solaire', 'Production\nappoint', 'Chauffage', 'ECS',
                      'Energie captable', 'Consommation appoint'],
                     ['Chauffage', 'ECS', 'Pertes appoint', 'Pertes réseau']],
          'diag_P': [['Energie solaire', 'Production\nappoint', 'Chauffage', 'ECS',
                      'Energie captable', 'Consommation appoint'],
                     ['Production\nappoint', 'Energie solaire']],
          'bar_cumC': [['Energie solaire', 'Production\nappoint', 'Chauffage', 'ECS',
                        'Energie captable', 'Consommation appoint'],
                       ['ECS', 'Chauffage', 'Pertes réseau']],
          'bar_cumA': [['Energie solaire', 'Production\nappoint', 'Chauffage', 'ECS',
                        'Energie captable', 'Consommation appoint'],
                       ['Energie solaire', 'Production\nappoint']],
          'bar_supC': [['Energie solaire', 'Production\nappoint', 'Chauffage', 'ECS',
                        'Energie captable', 'Consommation appoint'],
                       ['ECS', 'Chauffage', 'Pertes réseau']],
          'bar_supDispo': [['Energie solaire', 'Production\nappoint', 'Chauffage', 'ECS',
                            'Energie captable', 'Consommation appoint'],
                           ['Energie captable', 'Energie solaire']],
          'area_E': ['ECS', 'Energie solaire', 'Chauffage'],
          'area_EB': ['ECS', 'Chauffage', 'Pertes totales'],
          'line_E': ['ECS', 'Energie solaire', 'Production\nappoint', 'Chauffage'],
          'line_ES': ['Energie solaire', 'Energie captable'],
          'line_TE': ['T3', 'T4', 'T5', 'T12_house'],
          'line_T': ['T12_house', 'T10_solarInstruction', 'T9_ext'],
          'line_H': ['Diffus', 'Direct'],
          'line_debA': ['Flow_S6', 'Flow_S5', 'Flow_S4', 'Flow_S2'],
          'line_debS': ['Flow_S6', 'Flow_S5'],
          'line_debC': ['Flow_S4', 'Flow_S2'],
          'line_debSE': ['Flow_Collector', 'Flow_ExchTank_bot',
                         'Flow_ExchStorTank'],
          'line_debCE': ['Flow_ExchTank_top', 'Flow_Boiler'],
          'line_debSCEbuffer': ['Flow_ExchStorTank', 'Flow_Boiler'],
          'line_debSCE': ['Flow_Collector', 'Flow_Radiator'],
          'line_Drawing': ['Flow_Drawing'],
          'line_Backup': ['Backup_state', 'ECS_state'],
          'line_V3V': ['Vsolar_state', 'Vextra_state']}

col_dict = {'box': (('#268bd2', '#002b36', '#268bd2', '#268bd2', '#268bd2'),
                    ('#586e75', '#002b36', '#586e75', '#586e75', '#268bd2'),
                    ('#859900', '#002b36', '#859900', '#859900', '#268bd2')),
            'diag_B': ['#fdf6e3', '#268bd2', '#cb4b16', '#dc322f'],
            'diag_P': ['#6c71c4', 'orange'],
            'bar_cumA': {'Production\nappoint': '#fdf6e3', 'Energie solaire': 'orange',
                         'Pertes totales': '#cb4b16'},
            'bar_cumC': {'Production\nappoint': '#dc322f', 'Chauffage': '#fdf6e3',
                         'ECS': '#268bd2', 'Energie solaire': 'orange',
                         'Pertes réseau': '#cb4b16'},
            'bar_supDispo': {'Energie solaire': 'orange',
                             'Energie captable': '#859900'},
            'bar_supC': {'Production\nappoint': '#dc322f', 'Chauffage': '#fdf6e3',
                         'ECS': '#268bd2', 'Energie solaire': 'orange',
                         'Pertes réseau': '#cb4b16'},
            'area_E': 'Accent', 'line_E': 'Accent', 'line_TE': 'Accent',
            'line_ES': 'Accent', 'line_H': 'Accent', 'line_debA': 'Accent',
            'line_debS': 'Accent', 'line_debC': 'Accent', 'line_T': 'Accent',
            'line_debSE': 'Accent', 'line_debCE': 'Accent', 'area_EB': 'Accent',
            'line_debSCE': 'Accent', 'line_V3V': 'Accent',
            'line_Drawing': 'Accent', 'line_Backup': 'Accent',
            'line_debSCEbuffer': 'Accent'}

# Titles
titles = {'title': 'Bilan de la simulation',
          'box_Tbal': 'Evolution mensuelle de la variation \n' +
                      'des températures des ballons',
          'box_Tint': 'Evolution mensuelle de la variation \n' +
                      'des températures capteurs, extérieure et intérieure',
          'box_H': 'Evolution mensuelle de la variation \n' +
                   'de l’irradiation sur les panneaux',
          'box_HDir': 'Evolution mensuelle de la variation \n' +
                      'du potentiel de l’irradiation directe sur les panneaux',
          'box_P': 'Evolution de l’état des pompes d’appoint et solaires',
          'diag_B': 'Taux de couverture',
          'diag_P': 'Répartition de la production',
          'bar_cumA': 'Evolution mensuelle des apports',
          'bar_cumC': "Evolution mensuelle de la production d'énergie",
          'bar_supC': "Evolution mensuelle des apports et de la production d'énergie",
          'bar_supDispo': "Evolution mensuelle des gains et du rendement solaire",
          'area_E': 'Evolution annuelle de la consommation en énergie',
          'area_EB': 'Evolution annuelle des besoins',
          'line_E': 'Evolution annuelle de la consommation en énergie',
          'line_ES': 'Evolution annuelle de la production solaire',
          'line_TE': 'Evolution annuelle des températures dans les ballons',
          'line_T': 'Evolution annuelle de la température intérieure ' +
                    '\net extérieure',
          'line_H': 'Evolution annuelle de la puissance captée',
          'line_debA': 'Evolution des débits solaires et de chauffage',
          'line_debS': 'Evolution des débits solaires',
          'line_debC': 'Evolution des débits de chauffage',
          'line_debSE': 'Evolution des débits des équipements solaire',
          'line_debCE': 'Evolution des débits des équipements de chauffage',
          'line_debSCE': 'Evolution des débits dans le collecteur et radiateur',
          'line_debSCEbuffer': 'Evolution des débits dans la chaudière \n ' +
                               'et le tampon',
          'line_V3V': 'Etat des vannes de régulation',
          'line_Drawing': 'Evolution du débit de puisage',
          'line_Backup': 'Evolution de l’état de l’appoint et de ECS'}


# Change data columns names
conv_dict = {'DrawingUp_Energy': 'ECS', 'Radiator_Energy': 'Chauffage',
             'Collector_Energy': 'Energie solaire',
             # Must be a comment with csv files older than 2015
             'CollectorPanel_Energy': 'Energie captable',
             # Must be a comment with csv files older than 2015
             'BoilerFuel_Energy': 'Consommation appoint',
             # Must be a comment with csv files older than 2015
             'BoilerLosses_Energy': 'Pertes ambiance\nchaudiere',
             'Boiler_Energy': 'Production\nappoint',
             'HDifTil_collector': 'Diffus', 'HDirTil_collector': 'Direct'}

# New fields
new_fields = (('Besoins', 'ECS', 'Chauffage', '+'),
              ('Production', 'Energie solaire', 'Production\nappoint', '+'),
              ('Pertes réseau', 'Production', 'Besoins', '-'),
              ('Pertes appoint', 'Consommation appoint', 'Production\nappoint', '-'),
              ('Pertes totales', 'Pertes appoint', 'Pertes réseau', '+'),
              ('Taux de couverture', 'Energie solaire', 'Production', '/'),
              ('Rendement capteur', 'Energie solaire', 'Energie captable', '/'))

# Prepare Taux de couverture (list of formatted datas)
short_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sept', 'Oct',
               'Nov', 'Dec']

# Test
# _ chambery3p_20140802.csv chambery_20140825.csv chambery9p_20140821.csv
# chambery12p_20140802.csv lyon_20140920.csv
# marseille_20140630.csv strasbourg_20140707.csv bordeaux_20140715.csv
# chambery17KWh_20140910.csv chambery17KWh200plus_20140905.csv
# chamberyNosun_20140908.csv chambery17KWhNosun_20140911.csv
# marseilleNosun_20141009.csv
# chambery100plus_20140808.csv chambery100moins_20140811.csv
# chambery3padapt_20141020.csv chambery9padapt_20141001.csv
# chambery12padapt_20141006.csv
# marseille5KWh_20141013.csv
# none none

if __name__ == '__main__':
    # Dynamic selection of multiple csv with specific separator
    dataframes = []
    # Define dataframe to load
    welcome = 'Please choose csv files name inside this folder or default ' + \
              '(press enter) :\nFolder = {} '.format(fold) + \
              '(first element must be the separator)\n'
    names = input(welcome).split(' ')

    # Default instructions
    if names == ['']:
        names = ['_', 'chambery_20140825.csv']
        print('---> Defaults will be used : \n{}'.format(names))

    sep = names.pop(0)  # Recup separator value

    # Define how and what to plot
    welcome = '\nPlease choose kind of plot for each dataframes or default ' + \
              '(press enter) :\n' + \
              '    -' + ' space to select next dataframe\n' + \
              '    -' + ' comma to asign multiple plot to one dataframe\n' + \
              '    -' + ' first/second element used to select correct' + \
              ' x/y axis share\n' + \
              '      ("all", "row", "col" or "none")\n'
    # Print plots informations and user input choice
    print('\n', '-' * 30, 'All plots available :', '-' * 30, sep='\n')
    nb_fill = 10
    for plot_disp in sorted(fields.keys()):
        definition = titles[plot_disp].replace('\n', '\n' + ' ' * (nb_fill + 3))
        print('{0:{fill}{align}{nb_fill}} : {1}\n'.format(plot_disp, definition,
                                                          fill=' ', align='<',
                                                          nb_fill=nb_fill))
    # Limit plots list to number of dataframe + parameters (axis sharing)
    nb_name = len(names)
    plots = input(welcome).split(' ')[:nb_name + 2]
    # Default instructions
    if plots == ['']:
        plots = ['none', 'none',
                 'diag_P,diag_B,bar_cumA,bar_cumC']
        print('---> Defaults will be used : \n{}'.format(plots))
    share_x = plots.pop(0)  # Recup sharex flag
    share_y = plots.pop(0)  # Recup sharey flag
    for plot in range(len(plots)):
        plots[plot] = plots[plot].split(',')

    # Extract flags used inside dicts
    for ind, name in enumerate(names):
        dataframes.append(fold / name)
        names[ind] = name.split(sep)[0]
    structs = dict(zip(names, plots))
    # Split plot for each dataframes
    for el in structs:
        structs[el] = dict(zip(structs[el], [None] * len(structs[el])))
    # Dict of dict used to setup graphs
    print('\n---> Template : ')
    print(structs)

    # Read csvs and store values as a dict
    frames = read_csv(dataframes,
                      convert_index=(convert_to_datetime,) * nb_name,
                      delimiter=(';',) * nb_name,
                      index_col=('Date',) * nb_name,
                      in_conv_index=(None,) * nb_name,
                      skiprows=(1,) * nb_name,
                      splitters=(sep,) * nb_name)

    #
    ################## EvalData class : Prepare datas ##################
    #
    # Keep only 2014 datas into the dict
    datas = {name: EvalData(EvalData.keep_year(frames[name])) for name in frames}

    # Prepare structure for time_json (later populate with time heating infos)
    # Time per month
    months = ('January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November',
              'December', 'Annual')
    # OrderedDict used as input for month field inside time_info
    all_months = OrdD(zip(months[:-1], (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)))
    # Comprehension used to avoid reference errors because a list is mutable
    OrdD_list = [OrdD() for i in range(len(months))]
    # Create OrderedDict in comprehension
    time_json = {name: OrdD(zip(months, OrdD_list)) for name in frames}

    # Initialize a simple dictionnary to put inside energy informations
    energy_json = {}

    # # Initialize csv structure and add file head
    # time_csv = []
    # time_csv.append(["Data", "Month", "start_sim", "end_sim", "heating_time",
    #                  "solar_heating", "extra_heating", "Difference", "ratio"])

    for name in datas:
        # Change columns names
        datas[name].frame.columns = datas[name].change_names(conv_dict)
        print('\n\n', '\t' * 7, '*** {} ***'.format(name.upper()))
        # Display columns names
        print('\n---> Csv columns names after treatments')
        print(datas[name].frame.columns)
        # Add new fields to each datas
        for new in new_fields:
            # Create new columns
            datas[name].frame[new[0]] = datas[name].add_column(datas[name].frame,
                                                               used_cols=(new[1],
                                                                          new[2]),
                                                               operator=new[3])
    # --------------------------------------------------------------------------
        # # Display annual time informations
        # time_json[name]['Annual'] = time_info(frame=datas[name])
        # for m_ in months:
        #     if m_ != 'Annual':
        #         print("\n", m_)
        #         chunk = EvalData.only_month(frame=datas[name].frame,
        #                                     month=all_months[m_])
        #         time_json[name][m_] = time_info(frame=chunk)
        #     # Prepare time data to export
        #     prepare_export(dico=time_json, name=name)
            # # Create csv structure
            # time_csv.append([name, m_] +
            #                 [el for el in time_json[name][m_].values()])
    # --    ------------------------------------------------------------------------
        # Add all plot for each set of datas
        for el in structs[name]:
            if 'bar' in el:
                structs[name][el] = (datas[name].bar_energy(datas[name].frame,
                                                            new_fields=new_fields,
                                                            fields=fields[el][0]))
                # Here we populate the energy_json
                if 'Dispo' in el:
                    # Explicit copy
                    tmp = structs[name][el][0].copy()
                    tmp.index = structs[name][el][1]
                    tmp['Taux de couverture'] = tmp['Taux de couverture'] * 100
                    tmp['Rendement capteur'] = tmp['Rendement capteur'] * 100
                    # Temporary ordered dict to keep months in the right order
                    temp = OrdD()
                    for mth in tmp.index:
                        temp[mth] = {para: tmp[para][mth]
                                     for para in tmp.columns}
                    # Populate dict with temp ordered dict
                    energy_json[name] = temp

            elif 'box' in el:
                # structs[name][el] = (datas[name].box_actions(datas[name].frame,
                #                                              fields=fields[el],
                #                                              diurnal=False))
                structs[name][el] = (datas[name].box_actions(datas[name].frame,
                                                             fields=fields[el],
                                                             diurnal=True))
            elif 'diag' in el:
                structs[name][el] = (datas[name].diag_energy(datas[name].frame,
                                                             new_fields=new_fields,
                                                             fields=fields[el][0]))
            elif any(c in el for c in ('area', 'line')):

                # Just to see Temperature of drawing up variation
                chunk = datas[name].frame.copy()
                flag = 'Flow_Drawing'
                chunk['RealT'] = chunk['T11_Drawing_up'][:]
                chunk['RealT'].where(chunk[flag] > 0.12,  -1, inplace=True)
                print('TdrawingUp = ',
                      chunk[chunk["RealT"] != -1]['RealT'].mean())

                # Data which can be reduce to a 30min step size
                structs[name][el] = EvalData.resample(frame=datas[name].frame,
                                                      sample='30min',
                                                      interpolate=True)
                structs[name][el] = datas[name].frame

    # # Write to a json file all energy informations
    # with open('energy.json', 'w', encoding='utf-8') as f:
    #     json.dump(energy_json, f, indent=4)
    # # Write to a json file all heating time informations
    # with open('heating_time.json', 'w', encoding='utf-8') as f:
    #     json.dump(time_json, f, indent=4)

    # Write to a csv file all time informations
    # with open('Simulation_timedata.csv', 'w', newline='',
    #           encoding='utf-8') as csvfile:
    #     spamwriter = csv.writer(csvfile, delimiter=';')
    #     for row in time_csv:
    #         spamwriter.writerow(row)

    # Only display to have a pretty interface
    print('\n|\n|\n|--> Class creation now finish, plotting datas\n')

    #
    ################## MultiPlotter class : Plot datas ##################
    #
    add = ' -- '.join(data for data in datas)
    title = titles['title'] + ' pour les données de ' + add

    # Checks axes number and print map position
    sum_ = len([x for i in plots for x in i])
    print('Number of plots : {}'.format(sum_))
    rows, cols = to_table(sum_)
    # If we want a specific size for the axes map
    # rows, cols = 2, 2
    print('columns : {}\t rows : {}'.format(cols, rows))
    print('-' * 30, 'Mapping of positions coordinates:', '-' * 30, sep='\n')
    for row in range(rows):
        print('\n')
        for col in range(cols):
            print('({}, {})'.format(row, col), end=' ')
    print('\n')

    Plot = MultiPlotter({}, nb_cols=cols, nb_rows=rows, colors=None,
                        title=title, sharex=share_x, sharey=share_y)
    Plot.fig_init()

    # Flag on ---> add dataframe name, flag off ---> add nothing
    if len(set(names)) > 1:
        flag = True
    else:
        # Add nothing
        flag = False
        name_cap = ''
    for name in names:
        if flag:
            name_cap = name.capitalize()
        for plot in structs[name]:
            print('\n' + '-' * 30)
            print('{} datas.\n{}'.format(name.capitalize(), '-' * 30))
            value = '{} plot position: '.format(plot)
            pos = test_index(name, plot)
            print(pos)
            if 'bar' in plot:
                Plot.colors = col_dict[plot]
                print(structs[name][plot][0])
                if 'cum' in plot:
                    Plot.bar_cum_plot(structs[name][plot][0],
                                      emphs=emphs_dict[plot],
                                      pos=pos, fields=fields[plot][1],
                                      loc='center', line_dict={"linewidth": 4},
                                      names=structs[name][plot][1],
                                      title=titles[plot] + '\n{}'.format(name_cap))
                    print(structs[name][plot][1])
                elif 'sup' in plot:
                    Plot.colors = col_dict[plot]
                    print(structs[name][plot][0])
                    Plot.bar_sup_plot(structs[name][plot][0],
                                      emphs=emphs_dict[plot],
                                      pos=pos, fields=fields[plot][1],
                                      loc='center',
                                      names=structs[name][plot][1],
                                      title=titles[plot] + '\n{}'.format(name_cap))
                # Each xticks = short month name +
                if any(c in plot for c in ('C', 'A')):
                    # Taux de couverture de couverture solaire mensuel
                    percents = ['{:.1%}'.format(i)
                                for i in
                                structs[name][plot][0]['Taux de couverture'].values]
                    Plot.change_xticks_labels([short_names, [' : '] * 12, percents],
                                              pos=pos)
                if 'Dispo' in plot:
                    # Taux de couverture de couverture solaire mensuel
                    percents = ['{:.1%}'.format(i)
                                for i in
                                structs[name][plot][0]['Rendement capteur'].values]
                    Plot.change_xticks_labels([short_names, [' : '] * 12, percents],
                                              pos=pos)
                # Uncomment to set a y limit for each bar_cum plot
                # Plot.catch_axes(*pos).set_ylim(0, 2500)
            elif 'box' in plot:
                Plot.colors = col_dict['box']
                Plot.boxes_mult_plot(structs[name][plot], pos=pos, mean=False,
                                     patch_artist=True, loc='center',
                                     title=titles[plot] + '\n{}'.format(name_cap))
            elif 'diag' in plot:
                Plot.colors = col_dict[plot]
                if "_B" in plot:
                    explode = [0.1, 0.1]  # Initial value for explode
                else:
                    explode = [0.1]       # Initial value for explode
                # To have len() matching between explode and fields[plot][1]
                while len(explode) < len(fields[plot][1]):
                    explode.append(0.0)
                # Add specific title for diag_B
                if 'diag_B' in plot:
                    frame = structs[name][plot]
                    columns = frame.columns
                    p_title = '{1} : {0:.2%}'.format(frame.get_value(titles[plot],
                                                                     columns[0]),
                                                     titles[plot])
                else:
                    p_title = titles[plot]
                a = fields[plot][1]
                f = structs[name][plot]
                b = (' ({:.0f} KWh)'.format(f.ix[el, :1].values[0]) for el in a)
                # Create a list of string composed of a and b
                parts = [''.join(str(i) for i in el) for el in zip(a, b)]
                Plot.diag_plot(structs[name][plot], pos=pos, loc='center',
                               to_diag=fields[plot][1], legend=False,
                               title=p_title, labels=parts,
                               explode=explode)
                label = Plot.catch_axes(*pos).get_title() + '\n{}'.format(name_cap)
                Plot.catch_axes(*pos).set_title(label=label,
                                                fontdict=Plot.font_title)
            elif any(c in plot for c in ('area', 'line')):
                if 'V3V' in plot:
                    # All datas
                    Plot.frame_plot(structs[name][plot],
                                    fields=fields[plot],
                                    title=titles[plot] + '\n{}'.format(name_cap),
                                    pos=pos, loc='center',
                                    colormap=col_dict[plot],
                                    linewidth=2, kind=plot.split('_')[0],
                                    ylim=[-10, 110])
                    # Specific month
                    # Plot.frame_plot(EvalData.keep_month(structs[name][plot],
                    #                                     month=5),
                    #                 fields=fields[plot],
                    #                 title=titles[plot]+'\n{}'.format(name_cap),
                    #                 pos=pos, loc='center',
                    #                 color=col_dict[plot],
                    #                 linewidth=2, kind=plot.split('_')[0],
                    #                 ylim=[-10, 110])
                elif 'area' in plot:
                    # All datas
                    Plot.frame_plot(structs[name][plot], fields=fields[plot],
                                    title=titles[plot] + '\n{}'.format(name_cap),
                                    pos=pos, loc='center', stacked=True,
                                    colormap=col_dict[plot],
                                    linewidth=2, kind=plot.split('_')[0])
                    # Specific month
                    # Plot.frame_plot(EvalData.keep_month(structs[name][plot],
                    #                                     month=5),
                    #                 fields=fields[plot],
                    #                 title=titles[plot]+'\n{}'.format(name_cap),
                    #                 pos=pos, loc='center',
                    #                 color=col_dict[plot],
                    #                 linewidth=2, kind=plot.split('_')[0])
                else:
                    # All datas
                    Plot.frame_plot(structs[name][plot], fields=fields[plot],
                                    title=titles[plot] + '\n{}'.format(name_cap),
                                    pos=pos, loc='center',
                                    colormap=col_dict[plot],
                                    linewidth=2, kind=plot.split('_')[0])
                    # Specific month
                    # Plot.frame_plot(EvalData.keep_month(structs[name][plot],
                    #                                     month=5),
                    #                 fields=fields[plot],
                    #                 title=titles[plot]+'\n{}'.format(name_cap),
                    #                 pos=pos, loc='center',
                    #                 color=col_dict[plot],
                    #                 linewidth=2, kind=plot.split('_')[0])
            else:
                print('Nothing will be show for {}'.format(plot))

    # Adjust plot format (avoid overlaps)
    Plot.adjust_plots(hspace=0.6, wspace=0.15,
                      top=0.85, bottom=0.08,
                      left=0.05, right=0.96)
    Plot.tight_layout()
    # Removes empty axes (only last one for now)
    Plot.clean_axes(sum_)
    # Save plots
    base_name = "Simulation"
    if len(datas) == 1:
        base_name = name
    sav_plot(folder="D:\Github\solarsystem\Outputs\Plots_stock",
             base_name=base_name, plotter=Plot, facecolor="white")

    # Display plots
    Plot.show()
