# -*- coding:Utf8 -*-

"""
    Regroups all constants used inside bilan_reader.
"""

from Plotters.evaluation import *

# Constant
A_COL = {'IDMK': 2.32, 'Cobralino': 1.926}  # Collectors area

# Bar emphazis
emphs_dict = {'bar_cumA': ['Pertes réseau'],
              'bar_cumC': ['Production\nsolaire'],
              'bar_supC': ['Production\nsolaire'],
              'bar_supDispo': [],
              'bar_cumD': [],
              'bar_cumH': []}

conv_dict = {'DrawingUp_Energy': 'ECS',
             'SolarHeating_Energy': 'Chauffage_solaire',
             'SolarDrawingUp_Energy': 'ECS_solaire',
             'Collector_Energy': 'Production\nsolaire',
             'CollectorPanel_Energy': 'Energie captable',
             'ElecDHW_Energy': 'Consommation\nElec_ECS',
             'ElecHeating_Energy': 'Consommation\nElec_chauffage',
             'InternalGains_Energy': 'Gains internes',
             'HDifTil_collector': 'Diffus', 'HDirTil_collector': 'Direct'}


new_fields = (('Production\nappoint', 'Consommation\nElec_ECS',
               'Consommation\nElec_chauffage', '+'),
              ('Consommation\nappoint', 'Consommation\nElec_ECS',
               'Consommation\nElec_chauffage', '+'),
              ('Chauffage', 'Consommation\nElec_chauffage',
               'Chauffage_solaire', '+'),
              ('DHW_tank', 'Consommation\nElec_ECS',
               'ECS_solaire', '+'),
              ('DHW_tank_pertes', 'DHW_tank',
               'ECS', '-'),
              ('Besoins', 'ECS', 'Chauffage', '+'),
              ('Production', 'Production\nsolaire', 'Production\nappoint', '+'),
              ('Pertes réseau', 'Production', 'Besoins', '-'),
              ('Taux de couverture', 'Production\nsolaire', 'Production', '/'),
              ('Taux de couverture\nDHW', 'ECS_solaire', 'DHW_tank', '/'),
              ('Taux de couverture\nChauffage', 'Chauffage_solaire', 'Chauffage', '/'),
              ('Rendement capteur', 'Production\nsolaire', 'Energie captable', '/'),
              ('Pertes capteur', 'Energie captable', 'Production\nsolaire', '-'))


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
          'box_S': ['Speed_S6', 'Speed_S5', 'Speed_S2'],
          'diag_B': [conv_value_list,
                     ['Chauffage', 'ECS', 'Pertes réseau']],
          'diag_C': [conv_value_list,
                     ['Consommation\nappoint', 'Production\nsolaire']],
          'bar_cumC': [conv_value_list,
                       ['ECS', 'Chauffage', 'Pertes réseau']],
          'bar_cumA': [conv_value_list,
                       ['Production\nsolaire', 'Production\nappoint']],
          'bar_cumH': [conv_value_list,
                       ['Chauffage_solaire', 'Consommation\nElec_chauffage']],
          'bar_cumD': [conv_value_list,
                       ['ECS_solaire', 'Consommation\nElec_ECS', 'DHW_tank_pertes']],
          'bar_supC': [conv_value_list,
                       ['ECS', 'Chauffage', 'Pertes réseau']],
          'bar_supDispo': [conv_value_list,
                           ['Energie captable', 'Production\nsolaire']],
          # This plot return a cumulative evolution of Taux de couverture and Rendement.
          # We deal with energy not power so we don’t have taux de couverture and Rendement
          # at each time step.
          'area_E': ['Taux de couverture', 'Rendement capteur'],
          'area_P': ['Production\nsolaire', 'Pertes réseau', 'Production\nappoint'],
          'area_EB': ['ECS', 'Chauffage', 'Pertes réseau'],
          'line_E': ['ECS', 'Production\nsolaire', 'Production\nappoint', 'Chauffage'],
          'line_ES': ['Production\nsolaire', 'Energie captable'],
          'line_TE': ['T1', 'T3', 'T5'],
          'line_T': ['T9_ext', "T13_exch_inlet", 'T13_exch_outlet', 'T14_blowing'],
          'line_H': ['Diffus', 'Direct'],
          'line_debA': ['Flow_S6', 'Flow_S5', 'Flow_S2'],
          'line_debSE': ['Flow_Collector', 'Flow_S5',
                         'Flow_ExchStorTank'],
          'line_debSCE': ['Flow_Collector', 'Flow_S2'],
          'line_Drawing': ['Flow_Drawing'],
          'line_V3V': ['Vsolar_state']}

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
            'bar_cumD': {'Consommation\nElec_ECS': '#fdf6e3', 'ECS_solaire': 'orange',
                         'DHW_tank_pertes': '#cb4b16'},
            'bar_cumH': {'Consommation\nElec_chauffage': '#fdf6e3', 'Chauffage_solaire': 'orange'},
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
          'box_S': 'Evolution de la vitesse des pompes',
          'diag_B': 'Taux de couverture',
          'diag_C': 'Répartition de la consommation',
          'bar_cumA': 'Evolution mensuelle des apports',
          'bar_cumC': "Evolution mensuelle de la production d'énergie",
          'bar_cumD': "Evolution mensuelle de la production d'ECS",
          'bar_cumH': "Evolution mensuelle de la production du chauffage",
          'bar_supC': "Evolution mensuelle des apports et de la production d'énergie\n(énergies superposées)",
          'bar_supDispo': "Evolution mensuelle des gains et du rendement solaire\n(énergies superposées)",
          # 'bar_supDispo': "",
          'area_E': 'Evolution des facteurs caractéristiques',
          'area_P': 'Evolution annuelle de la production en énergie',
          'area_EB': 'Evolution annuelle des besoins',
          'line_E': 'Evolution annuelle de la consommation en énergie',
          'line_ES': 'Evolution annuelle de la production solaire',
          'line_TE': 'Evolution des températures du système solaire',
          'line_T': 'Evolution de la température dans le circuit d’air neuf ' +
                    '\net de la température intérieure',
          'line_H': 'Evolution annuelle de la puissance captée',
          'line_debA': 'Evolution des débits solaires et de chauffage',
          'line_debSE': 'Evolution des débits des équipements solaire',
          'line_debSCE': 'Evolution des débits dans le collecteur et radiateur',
          'line_V3V': 'Etat des vannes de régulation',
          'line_Drawing': 'Evolution du débit de puisage'}


# Field used as output for json energy file (check conv_dict to get correct names)
# Already monthly values when script create json structure.
# Careful if update conv_dict, you have to update this constant too.
JSON_ENERGY_FIELDS = ['Gains internes', 'Chauffage_solaire',
                      'Consommation\nElec_chauffage',
                      'Energie captable', 'ECS_solaire',
                      'Consommation\nElec_ECS',
                      'Production\nsolaire', 'ECS'] + [field[0] for field in new_fields]

# Field used as output for json energy file (check conv_dict to get correct names)
# These fields will be resampling before.
JSON_TEMP_FIELDS = ['T1', 'T3', 'T4', 'T5', 'T7', 'T8', 'T9_ext',
                    'T12_house', 'T14_blowing']


# Air system
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
                                      cols_map=['S2_state'],
                                      match_map=(100, ),
                                      start_sum=frame.frame.index[0])
    # Recup solar time TEST
    sol, _ = frame.col_sum_map_test(frame.frame,
                                    debug=False,
                                    cols_map=["Flow_Collector",
                                              "Vsolar_state"],
                                    start_sum=frame.frame.index[0])

    # Recup extra heating time with ugly function hack.
    chauff_app, _ = frame.col_sum_map_test(frame.frame,
                                           debug=False, second=False,
                                           cols_map=['ElecHeating_power'],
                                           start_sum=frame.frame.index[0])
    # Populate the time_dict
    time_dict['start_sim'] = frame.frame.index[0]
    time_dict['end_sim'] = frame.frame.index[-1]
    time_dict['solar_heating'] = chauff_sol
    time_dict['extra_heating'] = chauff_app
    time_dict['solar_working'] = sol
    if chauff_app > chauff_sol:
        time_dict['Difference'] = chauff_app - chauff_sol
    else:
        time_dict['Difference'] = chauff_sol - chauff_app
    # Display time informations
    if display is True:
        for key, item in time_dict.items():
            print('\n---> {} : {}'.format(key, item))
    return time_dict


def prepare_export(dico, name, mois):
    """
        Change format to prepare export to csv or json.
    """
    to_seconds = ('extra_heating', 'solar_heating',
                  'Difference', 'solar_working')
    dico[name][mois]['start_sim'] = str(dico[name][mois]['start_sim'])
    dico[name][mois]['end_sim'] = str(dico[name][mois]['end_sim'])
    for conv in to_seconds:
        dico[name][mois][conv] = dico[name][mois][conv].total_seconds()
