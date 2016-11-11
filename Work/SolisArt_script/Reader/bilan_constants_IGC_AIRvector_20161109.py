# -*- coding:Utf8 -*-

"""
    solarSystem > 21. Tient compte de la consommation des pompes.
"""

from Plotters.evaluation import *


# Collectors area
A_COL = {'IDMK25': 2.32, 'Cobralino': 1.926,
         'Radco308c': 2.193, 'Radco308cS': 2.32,
         'SkyPro12CPC58': 2.28, 'SkyPro': 2.28,
         'SkyProScaled12CPC58': 2.32, 'SkyProS': 2.32}

# Bar emphazis
emphs_dict = {'bar_cumA': ['Solaire_non_valorisée'],
              'bar_cumC': [],
              'bar_supC': ['Production_solaire'],
              'bar_supDispo': [],
              'bar_cumD': ['Apport_ECS\nsolaire'],
              'bar_cumH': []}

# Careful if update conv_dict, you have to update JSON_ENERGY_FIELDS constant too.
conv_dict = {'DrawingUp_Energy': 'Besoins_Puisage',
             'SolarHeating_Energy': 'Chauffage_solaire\nactif',
             'SolarDrawingUp_Energy': 'Apport_ECS\nsolaire',
             'Collector_Energy': 'Production_solaire',
             'CollectorPanel_Energy': 'Énergie captable',
             'ElecDHW_Energy': 'Consommation_appoint\nECS',
             'ElecHeating_Energy': 'Chauffage_appoint\nactif',
             'InternalGains_Energy': 'Gains\ninternes',
             'HDifTil_collector': 'Diffus', 'HDirTil_collector': 'Direct',
             'DHWTankTotalLosses_Energy': 'Ballon_ECS_pertes',
             'DHWTankPassiveGain_Energy': 'Ballon_ECS_gains',
             'StorageTankTotalLosses_Energy': 'Ballon_stockage_pertes',
             'StorageTankPassiveGain_Energy': 'Ballon_stockage_gains',
             'PipesLosses_Energy': 'Pertes\ncanalisations'}

# Attention à bien faire la différence entre consommation et besoins
new_fields = (
              # Consommations
              ('Consommation\nélectrique', 'Consommation_appoint\nECS', 'Chauffage_appoint\nactif', '+'),
              ('Consommation\nélectrique', 'Consommation\nélectrique', 'Pumps_Energy', '+'),
              # Énergie consommée (solaire + appointtrique)
              ('Consommation\nTotale', 'Production_solaire', 'Consommation\nélectrique', '+'),
              # Énergie fournit au ballon sanitaire (Électrique + solaire)
              ('Consommation_ECS', 'Consommation_appoint\nECS', 'Apport_ECS\nsolaire', '+'),
              # Énergie solaire valorisée
              ('Production_solaire\nvalorisée', 'Production_solaire', 'Pertes\ncanalisations', '-'),
              # Energie dans le ballon sanitaire + échangeur pour maintenir la température de consigne de 55°
              ('DeltaT_Energy', 'Consommation_ECS', 'Besoins_Puisage', '-'),          # Temp value
              ('DeltaT_Energy', 'DeltaT_Energy', 'Ballon_ECS_pertes', '-'),   # Final value
              # Répartition des pertes en fonction des consommations
              ('ratio_solaire', 'Apport_ECS\nsolaire', 'Consommation_ECS', '/'),
              ('ratio_elec', 'Consommation_appoint\nECS', 'Consommation_ECS', '/'),
              # Pertes solaires du ballon ECS
              ('Sanitaire\nsolaire_passif', 'Ballon_ECS_pertes', 'ratio_solaire', '*'),
              # Pertes appointtriques du ballon ECS
              ('Chauffage\nelec_passif', 'Ballon_ECS_pertes', 'ratio_elec', '*'),
              # Pertes solaires des ballons (stockage + sanitaire)
              ('Chauffage_solaire\npassif', 'Ballon_stockage_pertes', 'Sanitaire\nsolaire_passif', '+'),
              # Énergie apporté à la maison par le solaire
              ('Chauffage\nsolaire', 'Chauffage_solaire\nactif', 'Chauffage_solaire\npassif', '+'),
              ('Chauffage\nappoint', 'Chauffage_appoint\nactif', 'Chauffage\nelec_passif', '+'),
              # Consommations ACTIF pour le chauffage
              ('Chauffage_actif', 'Chauffage_appoint\nactif', 'Chauffage_solaire\nactif', '+'),
              # Besoin chauffage totaux (appoint passif + appoint actif + solaire passif + solaire actif)
              ('Consommation\nChauffage', 'Chauffage\nappoint', 'Chauffage\nsolaire', '+'),
              # Couverture totale
              ('CouvertureTotale', 'Production_solaire\nvalorisée', 'Consommation\nTotale', '/'),
              # Couverture chauffage
              ('Couverture\nChauffage', 'Chauffage\nsolaire', 'Consommation\nChauffage', '/'),
              # Couverture ECS
              ('Couverture\nECS', 'Apport_ECS\nsolaire', 'Consommation_ECS', '/'),
              ('Rendement capteur', 'Production_solaire', 'Énergie captable', '/'),
              ('Rendement solaire', 'Production_solaire\nvalorisée', 'Énergie captable', '/'),
              # Part_solaire non récupérée par les capteurs solaires.
              ('Solaire_non_capté', 'Énergie captable', 'Production_solaire', '-'),
              # Part de l’énergie solaire sur l’ECS
              ('ECS\nsolaire', 'Apport_ECS\nsolaire', 'Sanitaire\nsolaire_passif', '-'),
              # Part de l’énergie appointtrique sur l’ECS
              ('ECS\nappoint', 'Consommation_appoint\nECS', 'Chauffage\nelec_passif', '-'))


# Prepare Taux de couverture (list of formatted datas)
short_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sept', 'Oct',
               'Nov', 'Dec']


# Create list of all values inside conv_dict
not_energy_but_rename = ("Diffus", "Direct")  # Used to avoid useless aggregations
conv_value_list = [value for value in conv_dict.values() if value not in (not_energy_but_rename)]

# Fields (to plot new type of graph add new fields here)
fields = {'box_Tbal': ['T3', 'T4', 'T5'],
          'box_Text': ['T9_ext'],
          'box_H': ['Diffus', 'Direct'],
          'box_HDir': ['HDirNor', 'Direct'],
          'box_S': ['Speed_S6', 'Speed_S5', 'Speed_S2'],
          'diag_A': [conv_value_list,
                     ['Pertes\ncanalisations', 'Chauffage\nappoint',
                      'Chauffage\nsolaire',
                      'Besoins_Puisage', 'DeltaT_Energy']],
          'diag_B': [conv_value_list,
                     ['Pertes\ncanalisations', 'Chauffage\nappoint',
                      'Chauffage_solaire\nactif', 'Chauffage_solaire\npassif',
                      'ECS\nsolaire', 'ECS\nappoint']],
          'diag_C': [conv_value_list,
                     ['Pertes\ncanalisations', 'Production_solaire\nvalorisée', 'Consommation\nélectrique', 'Gains\ninternes']],
          'bar_cumC': [conv_value_list,
                       ['Production_solaire\nvalorisée', 'Consommation\nélectrique', 'Pertes\ncanalisations']],
          'bar_cumH': [conv_value_list,
                       ['Chauffage_appoint\nactif', 'Chauffage\nelec_passif',
                        'Chauffage_solaire\nactif', 'Chauffage_solaire\npassif']],
          'bar_cumD': [conv_value_list,
                       ['Besoins_Puisage', 'DeltaT_Energy', 'Ballon_ECS_pertes']],
          'bar_supDispo': [conv_value_list,
                           ['Énergie captable', 'Production_solaire', 'Production_solaire\nvalorisée']],
          # 'area_P': ['Production_solaire', 'Solaire_non_valorisée', 'Consommation\nélectrique'],
          # 'area_EB': ['Consommation_ECS', 'Consommation\nChauffage', 'Solaire_non_valorisée'],
          # 'line_E': ['Consommation_ECS', 'Production_solaire', 'Consommation\nélectrique', 'Consommation\nChauffage'],
          # 'line_ES': ['Production_solaire', 'Énergie captable'],
          # 'line_TE': ['T1', 'T3', 'T5'],
          # 'line_Tint': ['T12_house'],
          # 'line_T': ['T9_ext', "T13_exch_inlet", 'T13_exch_outlet', 'T14_blowing'],
          # 'line_H': ['Diffus', 'Direct'],
          # 'line_debA': ['Flow_S6', 'Flow_S5', 'Flow_S2'],
          # 'line_debSE': ['Flow_Collector', 'Flow_S5',
          #                'Flow_ExchStorTank'],
          # 'line_debSCE': ['Flow_Collector', 'Flow_S2'],
          # 'line_Drawing': ['Flow_Drawing'],
          # 'line_V3V': ['Vsolar_state']
          }

col_dict = {'box': (('#268bd2', '#002b36', '#268bd2', '#268bd2', '#268bd2'),
                    ('#586e75', '#002b36', '#586e75', '#586e75', '#268bd2'),
                    ('#859900', '#002b36', '#859900', '#859900', '#268bd2')),
            'diag_A': ['#cb4b16', '#fdf6e3',
                       'orange',
                       '#268bd2', '#2664d2'],
            'diag_B': ['#cb4b16', '#fdf6e3',
                       'orange', '#ffde00',
                       '#268bd2', '#2664d2'],
            'diag_C': ['#cb4b16', 'orange', '#fdf6e3', '#859900'],
            'bar_cumC': {'Consommation\nélectrique': '#fdf6e3', 'Production_solaire\nvalorisée': 'orange',
                         'Pertes\ncanalisations': '#cb4b16'},
            'bar_cumD': {'Ballon_ECS_pertes': '#cb4b16', 'DeltaT_Energy': '#2664d2',
                         'Besoins_Puisage': '#268bd2', 'Apport_ECS\nsolaire': 'orange'},
            'bar_cumH': {'Chauffage_appoint\nactif': '#fdf6e3', 'Chauffage\nelec_passif': '#f0f0f0',
                         'Chauffage_solaire\nactif': 'orange', 'Chauffage_solaire\npassif': '#ffde00'},
            'bar_supDispo': {'Production_solaire': 'orange',
                             'Énergie captable': '#ef946e',
                             'Production_solaire\nvalorisée': '#859900'},
            'area_E': 'Accent', 'line_E': 'Accent', 'line_TE': 'Accent',
            'line_ES': 'Accent', 'line_Tint': 'Accent', 'line_H': 'Accent', 'line_debA': 'Accent',
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
          'diag_A': 'CouvertureTotale',
          'diag_B': 'CouvertureTotale',
          'diag_C': 'Répartition de la production d’énergie',
          'bar_cumC': "Evolution mensuelle de la production d'énergie\n(énergies cumulées)",
          'bar_cumD': "Evolution mensuelle de la production d'ECS\n(énergies cumulées)",
          'bar_cumH': "Evolution mensuelle de la production du chauffage\n(énergies cumulées)",
          'bar_supDispo': "Evolution mensuelle des gains et du rendement solaire\n(énergies superposées)",
          # 'area_P': 'Evolution annuelle de la production en énergie',
          # 'area_EB': 'Evolution annuelle des besoins',
          # 'line_E': 'Evolution annuelle de la consommation en énergie',
          # 'line_ES': 'Evolution annuelle de la production solaire',
          # 'line_TE': 'Evolution des températures du système solaire',
          # 'line_Tint': 'Evolution de la température intérieure',
          # 'line_T': 'Evolution de la température dans le circuit d’air neuf ' +
          #           '\net de la température intérieure',
          # 'line_H': 'Evolution annuelle de la puissance captée',
          # 'line_debA': 'Evolution des débits solaires et de chauffage',
          # 'line_debSE': 'Evolution des débits des équipements solaire',
          # 'line_debSCE': 'Evolution des débits dans le collecteur et radiateur',
          # 'line_V3V': 'Etat des vannes de régulation',
          # 'line_Drawing': 'Evolution du débit de puisage'
          }


# Field used as output for json energy file (check conv_dict to get correct names)
# Already monthly values when script create json structure.
# Careful if update conv_dict, you have to update this constant too.
# IF ADDED FIELD ALREADY IN `new_fields` REMOVE IT !!
JSON_ENERGY_FIELDS = list(set(['Gains\ninternes', 'Chauffage_solaire\nactif',
                               'Chauffage_appoint\nactif',
                               'Énergie captable', 'Apport_ECS\nsolaire',
                               'Consommation_appoint\nECS',
                               'Pertes\ncanalisations',
                               'Production_solaire'] + [field[0] for field in new_fields]))

# Field used as output for json energy file (check conv_dict to get correct names)
# These fields will be resampling before.
JSON_TEMP_FIELDS = ['T1', 'T3', 'T4', 'T5', 'T7', 'T8', 'T9_ext',
                    'T12_house', 'T14_blowing']


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
