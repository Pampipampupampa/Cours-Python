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
    to fields, conv_dict and new_fields dictionnary or take a script of an older commit
    before 2015 (see github repository or git fonctionnality for more details)
"""

# import csv
import json

from path import Path

from bilan_constants_IGC_AIRvector_20161107 import *
fold = Path("D:\Github\Projets\IGC\Etudes\Simulations_Air_Solaire_maisonIndividuelle\PreEtude2\Resultats\Data")

# from bilan_constants_Solisart_WATERvector import *
# fold = FOLDER/'clean'/'SolisArt'


def test_index(name, plot):
    """
        Loop to check index value user input.
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


########################
#    Main Program :    #
########################

# IGC AIR RECYCLE SYSTEM 20160630 (**VERSION16**): DHW 55
# Cities
# bordeauxAir55T6M-4p_20160630.csv marseilleAir55T6M-4p_20160630.csv limogesAir55T6M-4p_20160630.csv toulouseAir55T6M-4p_20160630.csv
# strasbourgAir55T6M-4p_20160630.csv

# Ballon ECS
# bordeauxAir100ECS55T6M-4p_20160630.csv bordeauxAir200ECS55T6M-4p_20160630.csv bordeauxAir400ECS55T6M-4p_20160630.csv

# Ballon stockage
# bordeauxAir100Tampon6M-4p_20160630.csv bordeauxAir200Tampon6M-4p_20160630.csv bordeauxAir400Tampon6M-4p_20160630.csv

# Nbr capteur
# limogesAir55T6M-6p_20160630.csv limogesAir55T6M-8p_20160630.csv

# Inclinaison
# limogesAir60Inc55T6M-4p_20160630.csv limogesAir45Inc55T6M-4p_20160630.csv strasbourgAir60Inc55T6M-4p_20160630.csv

# Orientation
# limogesAiSO55T6M-4p_20160630.csv limogesAiSE55T6M-4p_20160630.csv

# Type capteur
# strasbourgAirSkyProS6M-4p_20160630.csv strasbourgAirRadco308cS6M-4p_20160630.csv

# Puisage
# limogesAirRepartiPuisage55T6M-4p_20160701.csv limogesAirMatinPuisaget55T6M-4p_20160701.csv

# DeltaT
# Sans effet PID
# limogesAir5Delta55T6M-4p_20160701.csv bordeauxAir5Delta55T6M-4p_20160701.csv limogesAir15Delta55T6M-4p_20160701.csv bordeauxAir15Delta55T6M-4p_20160701.csv
# effet PID
# limogesAir5Delta55T6M-4p_20160826.csv bordeauxAir5Delta55T6M-4p_20160826.csv limogesAir15Delta55T6M-4p_20160826.csv bordeauxAi15Deltar55T6M-4p_20160826.csv

# Température ballon
# limogesAir40T6M-4p_20160701.csv bordeauxAir40T6M-4p_20160701.csv

# Année entière 19-18
# marseilleAir55T-4p_20160702.csv limogesAir55T-4p_20160702.csv strasbourgAir55T-4p_20160702.csv toulouseAir55T-4p_20160702.csv bordeauxAir55T-4p_20160702.csv

# Année entière 20-18
# limogesAir55T20R18-4p_20160705.csv bordeauxAir55T20R18-4p_20160705.csv strasbourgAir55T20R18-4p_20160705.csv marseilleAir55T20R18-4p_20160705.csv toulouseAir55T20R18-4p_20160705.csv

# Setpoint
# bordeauxAir55T6M20R18-4p_20160701.csv limogesAir55T6M20R18-4p_20160701.csv

# Surchauffe
# limogesAir55T6MPasSurchauffe-4p_20160701.csv bordeauxAir55T6MPasSurchauffe-4p_20160701.csv strasbourgAir55T6MPasSurchauffe-4p_20160701.csv

# Tempo Élec
# limogesAir240TempoElec55T6M-4p_20160701.csv limogesAir120TempoElec55T6M-4p_20160701.csv

# Tempo débit
# limogesAir900TempoDebit55T6M-4p_20160701.csv limogesAir300TempoDebit55T6M-4p_20160701.csv

# Ventilation
# limogesAir55T6M90V90-4p_20160705.csv bordeauxAir55T6M90V90-4p_20160705.csv

# Drawing volume
# limogesAir55T6M220L-4p_20160720.csv bordeauxAir55T6M220L-4p_20160720.csv strasbourgAir55T6M220L-4p_20160720.csv


# IGC AIR RECYCLE SYSTEM 20160630 (**VERSION17**): DHW 55
# Variation débit
# limogesAir2040Debit55T6M-4p_20160722.csv limogesAir2020Debit55T6M-4p_20160722.csv limogesAir7070Debit55T6M-4p_20160722.csv limogesAir4040Debit55T6M-4p_20160722.csv



# Debugger
# import pdb; pdb.set_trace()

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
##############
# EVALUATION #
##############
    # Keep only 2014 datas into the dict
    # datas = {name: EvalData(EvalData.keep_year(frames[name])) for name in frames}

    # Remove first months row if not complete (Remove initialization from results)
    # Integration are still false yet ...
    for name in frames:
        # Check first month length
        length_first_month = len(frames[name][frames[name].index.month == frames[name].index[0].month].resample("D"))
        if length_first_month < 27:
            # Start dataframe at first row of next month
            start_value = frames[name][frames[name].index.month == (frames[name].index[0].month + 1)].index[0]
            frames[name] = frames[name][:][start_value:]
            print("Removing data from first month of {} (used by initialization)".format(name))

    # Wrap all frames in a EvalData structure
    datas = {name: EvalData(frames[name]) for name in frames}

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

    for name in datas:
        # Change columns names
        datas[name].frame.columns = datas[name].change_names(conv_dict)
        print('\n\n', '\t' * 7, '*** {} ***'.format(name.upper()))
        # Add new fields to each datas
        for new in new_fields:
            # Create new columns
            datas[name].frame.loc[:, new[0]] = datas[name].add_column(datas[name].frame,
                                                                      used_cols=(new[1],
                                                                                 new[2]),
                                                                      operator=new[3])
        # Display columns names
        print('\n---> Csv columns names after adding new fields')
        print(datas[name].frame.columns)

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
        #     prepare_export(dico=time_json, name=name, mois=m_)
    # --------------------------------------------------------------------------
        # Add all plot for each set of datas
        for el in structs[name]:
            if 'bar' in el:
                structs[name][el] = (datas[name].bar_energy(datas[name].frame,
                                                            new_fields=new_fields,
                                                            fields=fields[el][0]))


    # # --------------------------------------------------------------------------
    #             # Here we populate the energy_json ().
    #             # JSON_TEMP_FIELDS constant define inside bilan_constant file.
    #             if 'Dispo' in el:
    #                 # Explicit copy
    #                 tmp = structs[name][el][0][JSON_ENERGY_FIELDS].copy()
    #                 tmp.index = structs[name][el][1].copy()
    #                 tmp['CouvertureTotale'] = tmp['CouvertureTotale'] * 100
    #                 tmp['Rendement capteur'] = tmp['Rendement capteur'] * 100
    #                 tmp['Couverture\nECS'] = tmp['Couverture\nECS'] * 100
    #                 tmp['Couverture\nChauffage'] = tmp['Couverture\nChauffage'] * 100
    #                 for mth in tmp.index:
    #                     energy_json.setdefault(name, {})[mth] = {para: tmp[para][mth]
    #                                                              for para in tmp.columns}
    #                     # Add mean value for other column not described inside JSON_ENERGY_FIELDS
    #                     f_temp = datas[name].frame[JSON_TEMP_FIELDS].copy()
    #                     # Explication: meth:`evaluation.EvalData.bar_energy`
    #                     if f_temp[:][-1:].index.is_month_end:
    #                         f_temp = f_temp.resample('M', "mean")
    #                     else:
    #                         f_temp = f_temp.resample('M', "mean")[:-1]
    #                     f_temp.index = tmp.index
    #                     for temperature in f_temp.columns:
    #                         energy_json.setdefault(name, {})[mth][temperature] = f_temp[temperature][mth]

    # # --------------------------------------------------------------------------

            elif 'box' in el:
                structs[name][el] = (datas[name].box_actions(datas[name].frame,
                                                             fields=fields[el],
                                                             diurnal=True))
            elif 'diag' in el:
                structs[name][el] = (datas[name].diag_energy(datas[name].frame,
                                                             new_fields=new_fields,
                                                             fields=fields[el][0]))
                # Here we populate the energy_json ().
                # JSON_TEMP_FIELDS constant define inside bilan_constant file.
                # Only energy fields have valuable informations
                # Temperature an Power must be sum from month values if needed
                if "_B" in el:
                    # Explicit copy
                    tmp = structs[name][el].copy()
                    tmp = pd.Series(tmp.ix[:, 0], tmp.index)
                    if "6M" in name:
                        tmp.name = "Heating season"
                    else:
                        tmp.name = "Annual"
                    tmp = tmp[JSON_ENERGY_FIELDS]
                    tmp['CouvertureTotale'] = tmp['CouvertureTotale'] * 100
                    tmp['Rendement capteur'] = tmp['Rendement capteur'] * 100
                    tmp['Couverture\nECS'] = tmp['Couverture\nECS'] * 100
                    tmp['Couverture\nChauffage'] = tmp['Couverture\nChauffage'] * 100
                    # Populate json dict with Series values
                    energy_json.setdefault(name, {})[tmp.name] = {ind: tmp[ind] for ind in tmp.index}

            elif any(c in el for c in ('area', 'line')):

                # # Just to see Temperature of drawing up variation
                # chunk = datas[name].frame.copy()
                # flag = 'Flow_Drawing'
                # chunk['RealT'] = chunk['T11_Drawing_up'][:]
                # chunk['RealT'].where(chunk[flag] > 0.12,  -1, inplace=True)
                # print('TdrawingUp = ',
                #       chunk[chunk["RealT"] != -1]['RealT'].mean())

                # Data which can be reduce to a 1 hour step size
                structs[name][el] = EvalData.resample(frame=datas[name].frame,
                                                      sample='1h',
                                                      interpolate=True)
                # structs[name][el] = datas[name].frame

# --------------------------------------------------------------------------
    # Write to a json file all energy informations
    with open('energy.json', 'w', encoding='utf-8') as f:
        json.dump(energy_json, f, indent=4, ensure_ascii=False)
    # # Write to a json file all heating time informations
    # with open('heating_time.json', 'w', encoding='utf-8') as f:
    #     json.dump(time_json, f, indent=4)
# --------------------------------------------------------------------------

    # Only display to have a pretty interface
    print('\n|\n|\n|--> Class creation now finish, plotting datas\n')


###########
# PLOTTER #
###########
    add = ' -- '.join(data for data in datas)
    title = titles['title'] + ' pour les données de ' + add

    # Checks axes number and print map position
    sum_ = len([x for i in plots for x in i])
    print('Number of plots : {}'.format(sum_))
    rows, cols = to_table(sum_)
    # If we want a specific size for the axes map
    # rows, cols = 1, 2
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
                ylabel = "$KWh$"
                Plot.colors = col_dict[plot]
                # KWh to KWh/m2 (Careful collector area extract from name)
                nb_col = int(name.split("-")[1][:1])
                if 'Dispo' in plot:
                    find = False
                    # Dict defines in `bilan_constants_IGC_AIRvector_20151201`
                    for collector in A_COL:
                        if collector in name:
                            area_col = A_COL[collector]
                            find = True
                            break
                    if not find:
                        area_col = A_COL['IDMK25']
                    # Check number and size of collectors
                    print("**********   ", nb_col, area_col, "   ***********")
                    for column_name in structs[name][plot][0].columns:
                        if any(c in column_name for c in ("CouvertureTotale",
                                                          "Rendement capteur",
                                                          "Rendement solaire")):
                            continue
                        else:
                            structs[name][plot][0][column_name] = structs[name][plot][0][column_name] / (area_col * nb_col)
                            ylabel = "$KWh/m^2$"
                # Data check
                # Need to reduce the number of plots.
                print(structs[name][plot][0][fields[plot][1] + emphs_dict[plot]])

                if 'cum' in plot:
                    Plot.bar_cum_plot(structs[name][plot][0], legend_dict={'ncol': 2},
                                      emphs=emphs_dict[plot],
                                      pos=pos, fields=fields[plot][1],
                                      loc='center', line_dict={"linewidth": 6},
                                      names=structs[name][plot][1], ylabel=ylabel,
                                      title=titles[plot] + '\n{}'.format(name_cap))
                    # Uncomment to set a y limit for each bar_cum plot
                    # Plot.catch_axes(*pos).set_ylim(0, 2500)
                elif 'sup' in plot:
                    Plot.colors = col_dict[plot]
                    Plot.bar_sup_plot(structs[name][plot][0],
                                      emphs=emphs_dict[plot],
                                      pos=pos, fields=fields[plot][1],
                                      loc='center', ylabel=ylabel,
                                      names=structs[name][plot][1],
                                      title=titles[plot] + '\n{}'.format(name_cap))
                    # Uncomment to set a y limit for each bar_cum plot
                    # Plot.catch_axes(*pos).set_ylim(0, 2500)
                # Change xticks labels to add solar efficiency
                if any(c in plot for c in ('C', 'A')):
                    # Taux de couverture de couverture solaire mensuel
                    percents = ['{:.0%}'.format(i)
                                for i in
                                structs[name][plot][0]['CouvertureTotale'].values]
                if 'D' in plot:
                    # Taux de couverture de couverture solaire mensuel ECS
                    percents = ['{:.0%}'.format(i)
                                for i in
                                structs[name][plot][0]['Couverture\nECS'].values]

                if 'H' in plot:
                    # Taux de couverture de couverture solaire mensuel pour le chauffage
                    percents = ['{:.0%}'.format(i)
                                for i in
                                structs[name][plot][0]['Couverture\nChauffage'].values]
                if 'Dispo' in plot:
                    # Taux de couverture de couverture solaire mensuel
                    percents = ['\n{:.0%}\n{:.0%}'.format(i, j)
                                for (i, j) in
                                zip(structs[name][plot][0]['Rendement capteur'].values,
                                    structs[name][plot][0]['Rendement solaire'].values)]
                used_percents = [percent if 'nan' not in percent else '*' for percent in percents]
                Plot.change_xticks_labels([structs[name][plot][1], [' : '] * len(structs[name][plot][1]),
                                           used_percents],
                                          pos=pos)
                # Uncomment to set a y limit for each bar_cum plot
                # Plot.catch_axes(*pos).set_ylim(0, 2250)

                # # Change labels inside legend
                # Plot.font_legend = {'size': 20,
                #                     'family': 'Source Code Pro'}
                # new_labels = ['Available solar energy', 'Solar production']
                # new_labels = ['DHW', 'Space heating', 'Losses', 'Solar fraction']
                # Plot.catch_axes(*pos).legend(labels=new_labels, loc="best",
                #                              prop=Plot.font_legend)
            elif 'box' in plot:
                Plot.colors = col_dict['box']
                names = [short_names[month_nb - 1] for month_nb in structs[name][plot][1]]
                Plot.boxes_mult_plot(structs[name][plot][0], pos=pos, mean=False,
                                     patch_artist=True, loc='center', rot=0,
                                     prop_legend={'ncol': 1, 'names': names},
                                     title=titles[plot] + '\n{}'.format(name_cap),
                                     notch=True)

                # # Remove after publi
                # Plot.boxes_mult_plot(structs[name][plot], pos=pos, mean=False, rot=0,
                #                      patch_artist=True, loc='center', prop_legend={'ncol': 3},
                #                      title='' + '\n{}'.format(name_cap))
                # Plot.catch_axes(*pos).set_ylim(-5, 2500)
                # Plot.catch_axes(*pos).set_ylabel("1/min", fontsize=28, style='italic')

            elif 'diag' in plot:
                Plot.colors = col_dict[plot]
                if "_B" in plot:
                    explode = [0.1, 0.1, 0.0, 0.0, 0.1, 0.1]  # Initial value for explode
                elif "_A" in plot:
                    explode = [0.0, 0.0, 0.0, 0.0, 0.0]  # Initial value for explode
                else:
                    explode = [0.0, 0.0, 0.1, 0.1]       # Initial value for explode
                # To have len() matching between explode and fields[plot][1]
                while len(explode) < len(fields[plot][1]):
                    explode.append(0.0)
                # Add specific title for diag_B
                if any(c in plot for c in ('_B', '_H', '_D')):
                    frame = structs[name][plot]
                    columns = frame.columns
                    p_title = '{1} : {0:.1%}'.format(frame.get_value(titles[plot],
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
                stacked = False
                ylim = (None, None)
                if 'V3V' in plot:
                    ylim = [-10, 110]
                elif 'area' in plot:
                    stacked = False  # Default True in area plot inside plotter.
                # All datas
                Plot.frame_plot(structs[name][plot], fields=fields[plot],
                                title=titles[plot] + '\n{}'.format(name_cap),
                                pos=pos, loc='center', stacked=stacked,
                                colormap=col_dict[plot], ylim=ylim,
                                linewidth=2, kind=plot.split('_')[0])

                # # Specific month
                # Plot.frame_plot(EvalData.keep_month(structs[name][plot],
                #                                     month=2),
                #                 fields=fields[plot],
                #                 title=titles[plot]+'\n{}'.format(name_cap),
                #                 pos=pos, loc='center', stacked=stacked
                #                 colormap=col_dict[plot], ylim=ylim
                #                 linewidth=2, kind=plot.split('_')[0])

                # # Remove after publi
                # Plot.frame_plot(structs[name][plot], fields=fields[plot],
                #                 title='' + '\n{}'.format(name_cap),
                #                 pos=pos, loc='center', stacked=stacked
                #                 colormap=col_dict[plot], ylim=ylim
                #                 linewidth=2, kind=plot.split('_')[0])
                # Plot.catch_axes(*pos).set_ylabel("°C", fontsize=28, style='italic')
                # Plot.catch_axes(*pos).legend(['T3', 'T4', 'T5', 'T_house'], loc=1,
                #                              prop={'size': 24,
                #                                    'family': 'Source Code Pro'},
                #                              ncol=1)

            else:
                print('Nothing will be show for {}'.format(plot))

    # # Adjust plot format (avoid overlaps)
    # Plot.adjust_plots(hspace=0.6, wspace=0.15,
    #                   top=0.85, bottom=0.08,
    #                   left=0.07, right=0.96)
    Plot.tight_layout()
    # Removes empty axes (only last one for now)
    Plot.clean_axes(sum_)
    # Save plots
    base_name = "Simulation"
    if len(datas) == 1:
        base_name = name
    # sav_plot(folder="D:\Github\solarsystem\Outputs\Plots_stock",
    #          base_name=base_name, plotter=Plot, facecolor="white", dpi=300)

    # Display plots
    Plot.show()
