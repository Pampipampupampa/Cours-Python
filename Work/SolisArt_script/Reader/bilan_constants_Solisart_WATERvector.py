# -*- coding:Utf8 -*-

"""
    Regroups all constants used inside bilan_reader.
"""

from Plotters.evaluation import *

# Constant
A_COL = {'IDMK': 2.32, 'Cobralino': 1.926}  # Collector area

# Bar emphazis
emphs_dict = {'bar_cumA': ['Pertes réseau'],
              'bar_cumC': ['Production\nsolaire'],
              'bar_supC': ['Production\nsolaire'],
              'bar_supDispo': []}

# Change data columns names
conv_dict = {'DrawingUp_Energy': 'ECS', 'Radiator_Energy': 'Chauffage',
             'Collector_Energy': 'Production\nsolaire',
             # Must be a comment with csv files older than 2015
             'CollectorPanel_Energy': 'Energie captable',
             # Must be a comment with csv files older than 2015
             'BoilerFuel_Energy': 'Consommation\nappoint',
             # Must be a comment with csv files older than 2015
             'BoilerLosses_Energy': 'Pertes ambiance\nchaudiere',
             'Boiler_Energy': 'Production\nappoint',
             'HDifTil_collector': 'Diffus', 'HDirTil_collector': 'Direct'}

# New fields
new_fields = (('Besoins', 'ECS', 'Chauffage', '+'),
              ('Production', 'Production\nsolaire', 'Production\nappoint', '+'),
              ('Pertes réseau', 'Production', 'Besoins', '-'),
              ('Pertes appoint', 'Consommation\nappoint', 'Production\nappoint', '-'),
              ('Pertes totales', 'Pertes appoint', 'Pertes réseau', '+'),
              ('Taux de couverture', 'Production\nsolaire', 'Production', '/'),
              ('Rendement capteur', 'Production\nsolaire', 'Energie captable', '/'),
              ('Pertes capteur', 'Energie captable', 'Production\nsolaire', '-'))
              # ('Gain\nsolaire', 'SolarPower_absorbed', 'SolarPower_lost', '-'))

# Prepare Taux de couverture (list of formatted datas)
short_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sept', 'Oct',
               'Nov', 'Dec']

# Create list of all values inside conv_dict
conv_value_list = [values for values in conv_dict.values()]

# Fields (to plot new type of graph add new fields here)
fields = {'box_Tbal': ['T3', 'T4', 'T5'],
          'box_Text': ['T9_ext'],
          'box_H': ['Diffus', 'Direct'],
          'box_HDir': ['HDirNor', 'Direct'],
          'box_P': ['Flow_S6', 'Flow_S5', 'Flow_S4'],
          'diag_B': [conv_value_list,
                     ['Chauffage', 'ECS', 'Pertes appoint', 'Pertes réseau']],
          'diag_P': [conv_value_list,
                     ['Pertes capteur', 'Production\nsolaire']],
          'diag_C': [conv_value_list,
                     ['Consommation\nappoint', 'Production\nsolaire']],
          'bar_cumC': [conv_value_list,
                       ['ECS', 'Chauffage', 'Pertes réseau']],
          'bar_cumA': [conv_value_list,
                       ['Production\nsolaire', 'Production\nappoint']],
          'bar_supC': [conv_value_list,
                       ['ECS', 'Chauffage', 'Pertes réseau']],
          'bar_supDispo': [conv_value_list,
                           ['Energie captable', 'Production\nsolaire']],
          'area_E': ['Production\nsolaire', 'Consommation\nappoint'],
          'area_P': ['Production\nsolaire', 'Pertes totales', 'Production\nappoint'],
          'area_EB': ['ECS', 'Chauffage', 'Pertes totales'],
          'line_E': ['ECS', 'Production\nsolaire', 'Production\nappoint', 'Chauffage'],
          'line_ES': ['Production\nsolaire', 'Energie captable'],
          'line_TE': ['T3', 'T4', 'T5', 'T12_house'],
          # 'line_TE': ['T7', 'T8', 'T12_house'],
          'line_T': ['T12_house', 'T10_solarInstruction', 'T9_ext'],
          'line_H': ['Diffus', 'Direct'],
          'line_debA': ['Flow_S6', 'Flow_S5', 'Flow_S4', 'Flow_S2'],
          'line_debS': ['Flow_S6', 'Flow_S5'],
          'line_debC': ['Flow_S4', 'Flow_S2'],
          'line_debSE': ['Flow_Collector', 'Flow_S5',
                         'Flow_ExchStorTank'],
          'line_debCE': ['Flow_S4', 'Flow_Boiler'],
          'line_debSCEbuffer': ['Flow_ExchStorTank', 'Flow_Boiler'],
          'line_debSCE': ['Flow_Collector', 'Flow_Radiator'],
          'line_Drawing': ['Flow_Drawing'],
          'line_Backup': ['Backup_state', 'ECS_state'],
          'line_V3V': ['Vsolar_state', 'Vextra_state']}

col_dict = {'box': (('#268bd2', '#002b36', '#268bd2', '#268bd2', '#268bd2'),
                    ('#586e75', '#002b36', '#586e75', '#586e75', '#268bd2'),
                    ('#859900', '#002b36', '#859900', '#859900', '#268bd2')),
            'diag_B': ['#fdf6e3', '#268bd2', '#cb4b16', '#dc322f'],
            'diag_P': ['#804040', 'orange'],
            'diag_C': ['#d33682', 'orange'],
            'bar_cumA': {'Production\nappoint': '#fdf6e3', 'Production\nsolaire': 'orange',
                         'Pertes totales': '#cb4b16'},
            'bar_cumC': {'Production\nappoint': '#dc322f', 'Chauffage': '#fdf6e3',
                         'ECS': '#268bd2', 'Production\nsolaire': 'orange',
                         'Pertes réseau': '#cb4b16'},
            'bar_supDispo': {'Production\nsolaire': 'orange',
                             'Energie captable': '#859900'},
            'bar_supC': {'Production\nappoint': '#dc322f', 'Chauffage': '#fdf6e3',
                         'ECS': '#268bd2', 'Production\nsolaire': 'orange',
                         'Pertes réseau': '#cb4b16'},
            'area_E': 'Accent', 'line_E': 'Accent', 'line_TE': 'Accent',
            'line_ES': 'Accent', 'line_H': 'Accent', 'line_debA': 'Accent',
            'line_debS': 'Accent', 'line_debC': 'Accent', 'line_T': 'Accent',
            'line_debSE': 'Accent', 'line_debCE': 'Accent', 'area_EB': 'Accent',
            'line_debSCE': 'Accent', 'line_V3V': 'Accent', 'area_P': 'Accent',
            'line_Drawing': 'Accent', 'line_Backup': 'Accent',
            'line_debSCEbuffer': 'Accent'}

# Titles
titles = {'title': 'Bilan de la simulation',
          'box_Tbal': 'Evolution mensuelle de la variation \n' +
                      'des températures des ballons',
          'box_Text': 'Evolution mensuelle de la variation \n' +
                      'dee la température etérieure',
          'box_H': 'Evolution mensuelle de la variation \n' +
                   'de l’irradiation sur les panneaux',
          'box_HDir': 'Evolution mensuelle de la variation \n' +
                      'du potentiel de l’irradiation directe sur les panneaux',
          'box_P': 'Evolution de l’état des pompes d’appoint et solaires',
          'diag_B': 'Taux de couverture',
          'diag_P': 'Rendement capteur',
          'diag_C': 'Répartition de la consommation',
          'bar_cumA': 'Evolution mensuelle des apports',
          'bar_cumC': "Evolution mensuelle de la production d'énergie",
          # 'bar_cumC': "",
          'bar_supC': "Evolution mensuelle des apports et de la production d'énergie",
          'bar_supDispo': "Evolution mensuelle des gains et du rendement solaire",
          'area_E': 'Evolution annuelle de la consommation en énergie',
          'area_P': 'Evolution annuelle de la production en énergie',
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


def prepare_export(dico, name, mois):
    """
        Change format to prepare export to csv or json.
    """
    to_seconds = ('heating_time', 'extra_heating', 'solar_heating',
                  'Difference', 'solar_working')
    dico[name][mois]['start_sim'] = str(dico[name][mois]['start_sim'])
    dico[name][mois]['end_sim'] = str(dico[name][mois]['end_sim'])
    for conv in to_seconds:
        dico[name][mois][conv] = dico[name][mois][conv].total_seconds()
