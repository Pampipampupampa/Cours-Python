# -*- coding:Utf8 -*-

"""
    Regroups all constants used inside bilan_reader.
    Can be used for air solar system newer than
    SolarSystem.Models.Systems.IGC_system.System.IGC_airVectorRecyclePassive_solar6.

    Note:
        - Taux de couverture met top en valeur le solaire car une grande partie est
          perdu.
        - Le taux de couverture sur les bar
    Il est plus intéressant de voir comment évolue la part réelle de solaire au cours
    de l’année (voir `Production_solaire\nutile`).
"""

from Plotters.evaluation import *

# Constant
A_COL = {'IDMK25': 2.32, 'Cobralino': 1.926, 'Radco308c': 2.193, 'SkyPro12CPC58': 2.28}  # Collectors area

# Bar emphazis
emphs_dict = {'bar_cumA': ['Pertes_solaires'],
              'bar_cumC': ['Production_solaire\nutile'],
              'bar_supC': ['Production\nsolaire'],
              'bar_supDispo': [],
              'bar_cumD': [],
              'bar_cumH': []}

conv_dict = {'DrawingUp_Energy': 'Besoins_ECS_puisage',
             'SolarHeating_Energy': 'Chauffage_solaire_actif',
             'SolarDrawingUp_Energy': 'ECS_solaire',
             'Collector_Energy': 'Production\nsolaire',
             'CollectorPanel_Energy': 'Energie captable',
             'ElecDHW_Energy': 'Consommation\nElec_ECS',
             'ElecHeating_Energy': 'Chauffage_elec',
             'InternalGains_Energy': 'Gains\ninternes',
             'HDifTil_collector': 'Diffus', 'HDirTil_collector': 'Direct',
             'DHWTankTotalLosses_Energy': 'Ballon_ECS_pertes',
             'DHWTankPassiveGain_Energy': 'Ballon_ECS_gains',
             'StorageTankTotalLosses_Energy': 'Ballon_stockage_pertes',
             'StorageTankPassiveGain_Energy': 'Ballon_stockage_gains',
             'PipesLosses_Energy': 'Pertes réseau'}

# 3 définitons:
#   - Consommation: Représente la demande en énergie
#   - Production: Remplace consommation pour le solaire
#   - Besoins: Représente la demande en chauffage et en ECS nécessaire

# Avant de tracer un graphe il faut vérifier que le bilan donné est le bon (correspond à ce que on veut montrer).
new_fields = (
              # Consommations.
              ('Consommation\nappoint', 'Consommation\nElec_ECS',
               'Chauffage_elec', '+'),
              ('Énergie\nnécessaire', 'Production\nsolaire', 'Consommation\nappoint', '+'),
              ('ECS_elec', 'Consommation\nElec_ECS', 'ECS_solaire', '+'),
              # Pertes réelles (les pertes des ballons utiles à l’ambiance ne sont pas considérées)
              ('Stockage_pertes', 'Ballon_stockage_pertes', 'Ballon_stockage_gains', '-'),
              ('Sanitaire_pertes', 'Ballon_ECS_pertes', 'Ballon_ECS_gains', '-'),
              ('Ballons_pertes', 'Stockage_pertes', 'Sanitaire_pertes', '+'),
              ('Pertes_solaires', 'Ballons_pertes', 'Pertes réseau', '+'),
              # Productions solaires utiles
              ('Production_solaire\nutile', 'Production\nsolaire', 'Pertes_solaires', '-'),
              ('Chauffage_solaire_passif', 'Ballon_ECS_gains', 'Ballon_stockage_gains', '+'),
              ('Chauffage_solaire', 'Chauffage_solaire_actif', 'Chauffage_solaire_passif', '+'),
              # Besoins
              ('Chauffage_direct', 'Chauffage_elec', 'Chauffage_solaire_actif', '+'),  # Besoin hors apports par les ballons.
              ('Besoins\nChauffage', 'Chauffage_elec', 'Chauffage_solaire', '+'),   # Besoin ECS, Chauffage, gains par ballons.
              ('Besoins_ECS', 'Énergie\nnécessaire', 'Besoins\nChauffage', '-'),  # On soustrait le chauffage (ballons passif et actif) puis
              ('Besoins_ECS', 'Besoins_ECS', 'Pertes_solaires', '-'),             # on soustrait les pertes (ballons passif et réseaux)
              ('Besoins', 'Besoins_ECS', 'Besoins\nChauffage', '+'),
              # Rendements
              ('Taux de couverture', 'Production\nsolaire', 'Énergie\nnécessaire', '/'),
              ('Taux de couverture\nChauffage', 'Chauffage_solaire', 'Besoins\nChauffage', '/'),
              ('Taux de couverture\nDHW', 'ECS_solaire', 'ECS_elec', '/'),
              ('Rendement capteur', 'Production\nsolaire', 'Energie captable', '/'),
              ('Rendement solaire', 'Production_solaire\nutile', 'Energie captable', '/'),
              # Part solaire non récupérée par les capteurs solaires.
              ('Solaire_non_capté', 'Energie captable', 'Production\nsolaire', '-'))


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
                     ['Besoins\nChauffage', 'Besoins_ECS', 'Pertes_solaires', 'Gains\ninternes']],
          'diag_C': [conv_value_list,
                     ['Consommation\nappoint', 'Production_solaire\nutile', 'Pertes_solaires']],
          'bar_cumC': [conv_value_list,
                       ['Besoins_ECS', 'Besoins\nChauffage', 'Pertes_solaires']],
          'bar_cumA': [conv_value_list,
                       ['Production\nsolaire', 'Consommation\nappoint']],
          'bar_cumH': [conv_value_list,
                       ['Chauffage_solaire', 'Chauffage_elec', 'Stockage_pertes']],
          'bar_cumD': [conv_value_list,
                       ['ECS_solaire', 'Consommation\nElec_ECS', 'Sanitaire_pertes']],
          'bar_supC': [conv_value_list,
                       ['Besoins_ECS', 'Besoins\nChauffage', 'Pertes_solaires']],
          'bar_supDispo': [conv_value_list,
                           ['Energie captable', 'Production\nsolaire', 'Production_solaire\nutile']],
          # This plot return a cumulative evolution of Taux de couverture and Rendement.
          # We deal with energy not power so we don’t have taux de couverture and Rendement
          # at each time step.
          'area_E': ['Taux de couverture', 'Rendement capteur'],
          'area_P': ['Production\nsolaire', 'Pertes_solaires', 'Consommation\nappoint'],
          'area_EB': ['Besoins_ECS', 'Besoins\nChauffage', 'Pertes_solaires'],
          'line_E': ['Besoins_ECS', 'Production\nsolaire', 'Consommation\nappoint', 'Besoins\nChauffage'],
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
            'diag_B': ['#fdf6e3', '#268bd2', '#cb4b16', '#859900'],
            'diag_P': ['#804040', 'orange'],
            'diag_C': ['#d33682', 'orange', '#cb4b16'],
            'bar_cumA': {'Consommation\nappoint': '#fdf6e3', 'Production\nsolaire': 'orange',
                         'Pertes totales': '#cb4b16'},
            'bar_cumC': {'Consommation\nappoint': '#dc322f', 'Besoins\nChauffage': '#fdf6e3',
                         'Besoins_ECS': '#268bd2', 'Production_solaire\nutile': 'orange',
                         'Pertes_solaires': '#cb4b16'},
            'bar_cumD': {'Consommation\nElec_ECS': '#fdf6e3', 'ECS_solaire': 'orange',
                         'Sanitaire_pertes': '#cb4b16'},
            'bar_cumH': {'Chauffage_elec': '#fdf6e3', 'Chauffage_solaire': 'orange',
                         'Stockage_pertes': '#cb4b16'},
            'bar_supDispo': {'Production\nsolaire': 'orange',
                             'Energie captable': '#fdf6e3',
                             'Production_solaire\nutile': '#859900'},
            'bar_supC': {'Consommation\nappoint': '#dc322f', 'Besoins\nChauffage': '#fdf6e3',
                         'Besoins_ECS': '#268bd2', 'Production\nsolaire': 'orange',
                         'Pertes_solaires': '#cb4b16'},
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
          'bar_cumC': "Evolution mensuelle de la production d'énergie\n(énergies cumulées)",
          'bar_cumD': "Evolution mensuelle de la production d'ECS\n(énergies cumulées)",
          'bar_cumH': "Evolution mensuelle de la production du chauffage\n(énergies cumulées)",
          'bar_supC': "Evolution mensuelle des apports et de la production d'énergie\n(énergies superposées)",
          'bar_supDispo': "Evolution mensuelle des gains et du rendement solaire\n(énergies superposées)",
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
JSON_ENERGY_FIELDS = ['Gains\ninternes', 'Chauffage_solaire_actif',
                      'Chauffage_elec',
                      'Energie captable', 'ECS_solaire',
                      'Consommation\nElec_ECS',
                      'Production\nsolaire', 'Besoins_ECS'] + [field[0] for field in new_fields]

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


