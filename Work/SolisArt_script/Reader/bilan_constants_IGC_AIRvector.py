# -*- coding:Utf8 -*-

"""
    Regroups all constants used inside bilan_reader.
"""

# Constant
A_COL = 2.32  # Collector area

# Bar emphazis
emphs_dict = {'bar_cumA': ['Pertes réseau'],
              'bar_cumC': ['Production\nsolaire'],
              'bar_supC': ['Production\nsolaire'],
              'bar_supDispo': []}

# Fields (to plot new type of graph add new fields here)
fields = {'box_Tbal': ['T3', 'T4', 'T5'],
          'box_Text': ['T9_ext'],
          'box_H': ['Diffus', 'Direct'],
          'box_HDir': ['HDirNor', 'Direct'],
          'box_S': ['Speed_S6', 'Speed_S5', 'Speed_S2'],
          'diag_B': [['Production\nsolaire', 'Production\nappoint', 'Chauffage', 'ECS',
                      'Energie captable', 'Consommation\nappoint'],
                     ['Chauffage', 'ECS', 'Pertes appoint', 'Pertes réseau']],
          'diag_P': [['Production\nsolaire', 'Production\nappoint', 'Chauffage', 'ECS',
                      'Energie captable', 'Consommation\nappoint'],
                     ['Pertes capteur', 'Production\nsolaire']],
          'diag_C': [['Production\nsolaire', 'Production\nappoint', 'Chauffage', 'ECS',
                      'Energie captable', 'Consommation\nappoint'],
                     ['Consommation\nappoint', 'Production\nsolaire']],
          'bar_cumC': [['Production\nsolaire', 'Production\nappoint', 'Chauffage', 'ECS',
                        'Energie captable', 'Consommation\nappoint'],
                       ['ECS', 'Chauffage', 'Pertes réseau']],
          'bar_cumA': [['Production\nsolaire', 'Production\nappoint', 'Chauffage', 'ECS',
                        'Energie captable', 'Consommation\nappoint'],
                       ['Production\nsolaire', 'Production\nappoint']],
          'bar_supC': [['Production\nsolaire', 'Production\nappoint', 'Chauffage', 'ECS',
                        'Energie captable', 'Consommation\nappoint'],
                       ['ECS', 'Chauffage', 'Pertes réseau']],
          'bar_supDispo': [['Production\nsolaire', 'Production\nappoint', 'Chauffage', 'ECS',
                            'Energie captable', 'Consommation\nappoint'],
                           ['Energie captable', 'Production\nsolaire']],
          'area_E': ['Taux de couverture', 'Rendement capteur'],
          'area_P': ['Production\nsolaire', 'Pertes totales', 'Production\nappoint'],
          'area_EB': ['ECS', 'Chauffage', 'Pertes totales'],
          'line_E': ['ECS', 'Production\nsolaire', 'Production\nappoint', 'Chauffage'],
          'line_ES': ['Production\nsolaire', 'Energie captable'],
          'line_TE': ['T1', 'T3', 'T4', 'T5'],
          'line_T': ['T12_house', 'T9_ext', 'T13_exch_outlet', 'T14_blowing'],
          'line_H': ['Diffus', 'Direct'],
          'line_debA': ['Flow_S6', 'Flow_S5', 'Flow_S4', 'Flow_S2'],
          'line_debS': ['Flow_S6', 'Flow_S5'],
          'line_debC': ['Flow_S4', 'Flow_S2'],
          'line_debSE': ['Flow_Collector', 'Flow_S5',
                         'Flow_ExchStorTank'],
          'line_debCE': ['Flow_S4', 'Flow_Boiler'],
          'line_debSCEbuffer': ['Flow_ExchStorTank', 'Flow_Boiler'],
          'line_debSCE': ['Flow_Collector', 'Flow_S2'],
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
          'box_S': 'Evolution de la vitesse des pompes',
          'diag_B': 'Taux de couverture',
          'diag_P': 'Rendement capteur',
          'diag_C': 'Répartition de la consommation',
          'bar_cumA': 'Evolution mensuelle des apports',
          'bar_cumC': "Evolution mensuelle de la production d'énergie",
          'bar_supC': "Evolution mensuelle des apports et de la production d'énergie",
          'bar_supDispo': "Evolution mensuelle des gains et du rendement solaire",
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

conv_dict = {'DrawingUp_Energy': 'ECS',
             'SolarHeating_Energy': 'Chauffage solaire',
             'Collector_Energy': 'Production\nsolaire',
             'CollectorPanel_Energy': 'Energie captable',
             'ElectricalDHW_Energy': 'Consommation\nElectrique_ECS',
             'ElectricalHeating_Energy': 'Consommation\nElectrique_chauffage',
             'InternalGains_Energy': 'Gains internes',
             'HDifTil_collector': 'Diffus', 'HDirTil_collector': 'Direct'}


new_fields = (('Production\nappoint', 'Consommation\nElectrique_ECS',
               'Consommation\nElectrique_chauffage', '+'),
              ('Besoins chauffage', 'Consommation\nElectrique_chauffage',
               'Chauffage solaire', '+'),
              ('Besoins', 'ECS', 'Besoins chauffage', '+'),
              ('Production', 'Production\nsolaire', 'Production\nappoint', '+'),
              ('Pertes réseau', 'Production', 'Besoins', '-'),
              ('Taux de couverture', 'Production\nsolaire', 'Production', '/'),
              ('Rendement capteur', 'Production\nsolaire', 'Energie captable', '/'),
              ('Pertes capteur', 'Energie captable', 'Production\nsolaire', '-'))

# Prepare Taux de couverture (list of formatted datas)
short_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
               'Jun', 'Jul', 'Aug', 'Sept', 'Oct',
               'Nov', 'Dec']
