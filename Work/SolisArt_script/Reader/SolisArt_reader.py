#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""
    Main script to plot and view readers

    1) You have to had new path, title and plotter class
       inside PATHS, TITLES and DICTCLASS.

    2) Add new plotter inside Plotters.__init__.py

    3) Add a description inside the menu variable to provide help for users

    4) Specifics treatments must be locate inside a :
         - elif choice == number:
             process actions ...
"""


########################################
#### Classes and Methods imported : ####
########################################


# All readers
from Plotters import *
# Reader parameters
from Plotters.parameters import *


#####################
#### Constants : ####
#####################


# Files path
PATHS = ((FOLDER + "clean\\olivier_house_read.csv",),
         (FOLDER + "Issues\\Algo_flow\\algo_flow_mod_01_clean.csv",),
         (FOLDER + "Issues\\Algo\\S5_algo_clean.csv",
          FOLDER + "Issues\\Algo\\S6_algo_clean.csv",),
         (FOLDER + "Issues\\Algo\\S4_algo_ECS_clean.csv",),
         (FOLDER + "Issues\\Algo\\variables_algo_clean.csv",
          FOLDER + "Issues\\Algo\\backup_algo_clean.csv",),
         (FOLDER + "Issues\\Algo\\Chauff_algo_clean.csv",),
         (FOLDER + "Issues\\Algo\\V3Vextra_algo_clean.csv",),
         (FOLDER + "Issues\\Algo\\V3Vsolar_algo_clean.csv",))

# Plots title
TITLES = ("Evolution des principaux paramètres caractéristiques du bâtiment",
          "Fonctionnement de l'algorithme de controle du débit des pompes",
          "Algorithme de controle des pompes S6 et S5",
          "Algorithme de controle de la pompe S4",
          "Algorithme déterminant la consigne solaire et le besoin en appoint",
          "Algorithme de controle de la variable Chauff",
          "Contrôle de la vanne d'appoint",
          "Contrôle de la vanne solaire")

# Dictionnary of dataframes plotter
DICTCLASS = {1: house_data.HousePlotter,
             2: pump_algo.PumpAlgoPlotter,
             3: S6_S5.S6S5Plotter,
             4: S4.S4Plotter,
             5: variable_backup.VarBackPlotter,
             6: chauff.ChauffPlotter,
             7: extra_valve.ExtraValvePlotter,
             8: solar_valve.SolarValvePlotter}

# MENU to choose dataframe (number - 1 = index inside PATHS and TITLES)
MENU = "\n{}\n".format("-"*40) + \
       "Select dataframe : \n" + \
       "1 : Recalage maison olivier \n" + \
       "2 : Contrôle des débits \n" + \
       "3 : Contrôle de S6 et S5\n" + \
       "4 : Contrôle de S4 et d'ECS\n" + \
       "5 : Contrôle DTeco, Températures de consigne et Appoint\n" + \
       "6 : Contrôle de CHAUFF \n" + \
       "7 : Contrôle de la vanne d'appoint \n" + \
       "8 : Contrôle de la vanne solaire \n" + \
       "\n0 : Close application \n"


########################
#### Main Program : ####
########################


assert (len(PATHS) == len(TITLES) == len(DICTCLASS)), "Constants length mismatch" + \
                                                      "\t---->Aborting"
valid_inputs = "".join(str(i) for i in range(1, len(PATHS)+1))

while True:
    print(MENU)

    # Intercept wrong inputs
    try:
        choice = int(input("Choice : "))
    except ValueError:
        print("Please check Menu : {} is not allowed".format(choice))
        continue

    # Close program
    if choice == 0:
        print("Programme now closing")
        break

    # Process actions
    elif str(choice) in valid_inputs:
        # len(PATHS[choice-1]) used to size function arguments
        frames = read_csv(PATHS[choice-1],
                          convert_index=(convert_to_datetime,)*len(PATHS[choice-1]),
                          delimiter=(";",)*len(PATHS[choice-1]),
                          index_col=("Date",)*len(PATHS[choice-1]),
                          in_conv_index=(None,)*len(PATHS[choice-1]),
                          skiprows=(1,)*len(PATHS[choice-1]))
        print(printer_spe(frames))
        if choice == 1:
            # Data reduce to speed up plotter
            frames["olivier_house_read"] = frames["olivier_house_read"][:].resample('60min')
        elif choice == 5:
            # Bug issue : bad date formatting and length mismatch
            frames["variables_algo_clean"] = frames["variables_algo_clean"].ix[:-1, :][:]
            frames["backup_algo_clean"].index = frames["variables_algo_clean"].index

        # Plot frame
        DICTCLASS[choice](frames, title=TITLES[choice-1]).draw()

    # Intercept input outside valid_inputs range
    else:
        print("Please check Menu : {} is not allowed".format(choice))
        continue
