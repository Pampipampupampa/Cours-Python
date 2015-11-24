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

# Select configuration file between projects
from bilan_constants_IGC_AIRvector import *
from bilan_constants_IGC_AIRvector_20151012 import *
fold = FOLDER/'clean'/'IGC'
# from bilan_constants_Solisart_WATERvector import *
# fold = FOLDER/'clean'/'SolisArt'


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


########################
#    Main Program :    #
########################


# Solisart:
# chambery-0p_20150206.csv bordeaux-0p_20150210.csv marseille-0p_20150208.csv strasbourg-0p_20150209.csv lyon-0p_20150218.csv
# chambery-3p_20150206.csv bordeaux-3p_20150208.csv marseille-3p_20150207.csv strasbourg-3p_20150210.csv lyon-3p_20150218.csv
# chambery-6p_20150207.csv bordeaux-6p_20150209.csv marseille-6p_20150208.csv strasbourg-6p_20150211.csv lyon-6p_20150219.csv
# chambery-9p_20150208.csv bordeaux-9p_20150210.csv marseille-9p_20150209.csv strasbourg-9p_20150211.csv lyon-9p_20150219.csv
# chambery300vm-6p_20150218.csv chambery300vp-6p_20150218.csv
# strasbourgLaurent-6p_20150126.csv   ---> Laurent Strasbourg file

# IGC: IGC_airVectorRecyclePassive_solar5 and IGC_airVectorRecyclePassive_solar_MeteoFrance3
# bordeauxAirRecycle-6p_20150606.csv bordeauxAirRecycle-4p_20150605.csv bordeauxAirRecycle-2p_20150605.csv
# bordeauxAirRecycle45Inc-4p_20150607.csv bordeauxAirRecycle60Inc-4p_20150607.csv
# bordeauxAirRecycle45mOrientation-4p_20150607.csv bordeauxAirRecycle45pOrientation-4p_20150607.csv
# bordeauxAirRecycle100vmDHW-4p_20150606.csv bordeauxAirRecycle100vpDHW-4p_20150604.csv bordeauxAirRecycle100vpDHW-6p_20150604.csv
# bordeauxAirRecycle200vpBuffer-4p_20150606.csv bordeauxAirRecycle200vmBuffer-4p_20150606.csv
# bordeauxAirRecyclePuisageReparti-4p_20150620.csv bordeauxAirRecyclePuisageMatin-4p_20150620.csv
# bordeauxAirRecycleM2012-4p_20150609.csv bordeauxAirRecycleM2013-4p_20150609.csv bordeauxAirRecycleM2014-4p_20150610.csv
# bordeauxAirRecycle1er-4p_20150622.csv bordeauxAirRecycle2nd-4p_20150622.csv bordeauxAirRecycle3rd-4p_20150622.csv

# bordeauxAirRecycleCapteurHP-4p_20150612.csv bordeauxAirRecycleCapteurHP-5p_20150612.csv
# Ne pas utiliser sans vérifications et comprendre les limites (voir tableur simulations)
# bordeauxAirRecycle100vpDHWCapteurHP-4p_20150604.csv bordeauxAirRecycleCapteurHP-4p_20150605.csv bordeauxAirRecycleCapteurHP-5p_20150605.csv


# IGC last system:
# bordeauxAirRecycle-4p_20151009.csv  # Ground temperature from weather data file.
# nantesAirRecycle-4p_20151018.csv limogesAirRecycle-4p_20151017.csv
# bordeauxAirRecycle-4p_20151017.csv bordeauxAirRecycleNoOverheat-4p_20151018.csv bordeauxAirRecycle-6p_20151019.csv
# bordeauxAirRecycle200Buffer200DHW-4p_20151020.csv bordeauxAirRecycle200DHW-4p_20151020.csv
# Bordeaux-4panneaux_.csv Bordeaux-6panneaux_.csv


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
                # Debugger
                # import pdb; pdb.set_trace()
    # --------------------------------------------------------------------------
                # # Here we populate the energy_json ().
                # # This part of the script can be moved outside by simply used
                # # JSON_TEMP_FIELDS for all columns ...
                # # Constants define inside bilan_constant file.
                # if 'Dispo' in el:
                #     # Explicit copy
                #     tmp = structs[name][el][0][JSON_ENERGY_FIELDS].copy()
                #     tmp.index = structs[name][el][1].copy()
                #     tmp['Taux de couverture'] = tmp['Taux de couverture'] * 100
                #     tmp['Rendement capteur'] = tmp['Rendement capteur'] * 100
                #     tmp['Taux de couverture\nDHW'] = tmp['Taux de couverture\nDHW'] * 100
                #     tmp['Taux de couverture\nChauffage'] = tmp['Taux de couverture\nChauffage'] * 100
                #     # Temporary ordered dict to keep months in the right order
                #     temp = OrdD()
                #     for mth in tmp.index:
                #         temp[mth] = {para: tmp[para][mth]
                #                      for para in tmp.columns}
                #         # Add mean value for other column not described inside JSON_ENERGY_FIELDS
                #         f_temp = datas[name].frame[JSON_TEMP_FIELDS].resample('1m', how='mean')
                #         f_temp.index = tmp.index
                #         for temperature in f_temp.columns:
                #             temp[mth][temperature] = f_temp[temperature][mth]
                #     # Populate dict with temp ordered dict
                #     energy_json[name] = temp
    # --------------------------------------------------------------------------

            elif 'box' in el:
                structs[name][el] = (datas[name].box_actions(datas[name].frame,
                                                             fields=fields[el],
                                                             diurnal=True))
            elif 'diag' in el:
                structs[name][el] = (datas[name].diag_energy(datas[name].frame,
                                                             new_fields=new_fields,
                                                             fields=fields[el][0]))
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
    # # Write to a json file all energy informations
    # with open('energy.json', 'w', encoding='utf-8') as f:
    #     json.dump(energy_json, f, indent=4)
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
    rows, cols = 1, 2
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
                # Check number of collectors
                print("**********   ", nb_col, "   ***********")
                if 'Dispo' in plot:
                    # Working but ugly, please fix.
                    area_col = A_COL['Cobralino'] if 'HP-' in name else A_COL['IDMK']
                    # Process change for each column except which contains ratio.
                    for column_name in structs[name][plot][0].columns:
                        if any(c in column_name for c in ("Taux de couverture",
                                                          "Rendement capteur")):
                            continue
                        else:
                            structs[name][plot][0][column_name] = structs[name][plot][0][column_name] / (area_col * nb_col)
                            ylabel = "$KWh/m^2$"
                # Data check
                # Need to reduce the number of plots.
                print(structs[name][plot][0])

                if 'cum' in plot:
                    Plot.bar_cum_plot(structs[name][plot][0], legend_dict={'ncol': 2},
                                      emphs=emphs_dict[plot],
                                      pos=pos, fields=fields[plot][1],
                                      loc='center', line_dict={"linewidth": 4},
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
                # Each xticks = short month name +
                if any(c in plot for c in ('C', 'A')):
                    # Taux de couverture de couverture solaire mensuel
                    percents = ['{:.1%}'.format(i)
                                for i in
                                structs[name][plot][0]['Taux de couverture'].values]
                if 'D' in plot:
                    # Taux de couverture de couverture solaire mensuel ECS
                    percents = ['{:.1%}'.format(i)
                                for i in
                                structs[name][plot][0]['Taux de couverture\nDHW'].values]

                if 'H' in plot:
                    # Taux de couverture de couverture solaire mensuel pour le chauffage
                    percents = ['{:.1%}'.format(i)
                                for i in
                                structs[name][plot][0]['Taux de couverture\nChauffage'].values]
                if 'Dispo' in plot:
                    # Taux de couverture de couverture solaire mensuel
                    percents = ['{:.1%}'.format(i)
                                for i in
                                structs[name][plot][0]['Rendement capteur'].values]
                percents = [percent if 'nan' not in percent else '*' for percent in percents]
                Plot.change_xticks_labels([short_names, [' : '] * 12, percents],
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
                Plot.boxes_mult_plot(structs[name][plot], pos=pos, mean=False,
                                     patch_artist=True, loc='center', rot=0,
                                     prop_legend={'ncol': 1},
                                     title=titles[plot] + '\n{}'.format(name_cap))

                # # Remove after publi
                # Plot.boxes_mult_plot(structs[name][plot], pos=pos, mean=False, rot=0,
                #                      patch_artist=True, loc='center', prop_legend={'ncol': 3},
                #                      title='' + '\n{}'.format(name_cap))
                # Plot.catch_axes(*pos).set_ylim(-5, 2500)
                # Plot.catch_axes(*pos).set_ylabel("1/min", fontsize=28, style='italic')

            elif 'diag' in plot:
                Plot.colors = col_dict[plot]
                if "_B" in plot:
                    explode = [0.1, 0.1, 0.1]  # Initial value for explode
                else:
                    explode = [0.1]       # Initial value for explode
                # To have len() matching between explode and fields[plot][1]
                while len(explode) < len(fields[plot][1]):
                    explode.append(0.0)
                # Add specific title for diag_B
                if any(c in plot for c in ('_B', '_P')):
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

    # Adjust plot format (avoid overlaps)
    # Plot.adjust_plots(hspace=0.6, wspace=0.15,
    #                   top=0.85, bottom=0.08,
    #                   left=0.05, right=0.96)
    Plot.tight_layout()
    # Removes empty axes (only last one for now)
    Plot.clean_axes(sum_)
    # # Save plots
    # base_name = "Simulation"
    # if len(datas) == 1:
    #     base_name = name
    # sav_plot(folder="D:\Github\solarsystem\Outputs\Plots_stock",
    #          base_name=base_name, plotter=Plot, facecolor="white", dpi=150)

    # Display plots
    Plot.show()
