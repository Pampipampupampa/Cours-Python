#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""Main script to plot an view all reader"""


########################################
#### Classes and Methods imported : ####
########################################


# All readers
from Plotters import *
# Reader parameters
from Plotters.parameters import *


########################
#### Main Program : ####
########################


paths = ((FOLDER + "clean\\olivier_house_read.csv",),
         (FOLDER + "Issues\\Algo_flow\\algo_flow_mod_01_clean.csv",),
         (FOLDER + "Issues\\Algo\\S5_algo_clean.csv",
          FOLDER + "Issues\\Algo\\S6_algo_clean.csv",),
         (FOLDER + "Issues\\Algo\\S4_algo_ECS_clean.csv",),
         (FOLDER + "Issues\\Algo\\variables_algo_clean.csv",
          FOLDER + "Issues\\Algo\\backup_algo_clean.csv",),
         (FOLDER + "Issues\\Algo\\Chauff_algo_clean.csv",))

titles = ("Evolution des principaux paramètres caractéristiques du bâtiment",
          "Fonctionnement de l'algorithme de controle du débit des pompes",
          "Algorithme de controle des pompes S6 et S5",
          "Algorithme de controle de la pompe S4",
          "Algorithme déterminant la consigne solaire et le besoin en appoint",
          "Algorithme de controle de la variable Chauff")

# Used as a reader selector
menu = "\nSelect dataframe : \n" + \
       "1 : House data \n" + \
       "2 : Débits algo \n" + \
       "3 : S6_S5 algo\n" + \
       "4 : S4 algo\n" + \
       "5 : variables_backup algo\n" + \
       "6 : Chauff algo \n\n" + \
       "0 : Close application \n"

while True:
    print(menu)
    try:
        choice = int(input("Action : "))
    except ValueError:
        print("Please enter a number inside the list")
        continue
    if choice == 0:
        print("Programme now closing")
        break
    elif choice == 1:
        frames = read_csv(paths[choice-1], convert_index=(convert_to_datetime,))
        frames["olivier_house_read"] = frames["olivier_house_read"][:].resample('60min')
        print(printer_spe(frames))
        house_data.HousePlotter(frames["olivier_house_read"],
                                title=titles[choice-1]).draw()
    elif choice == 2:
        frames = read_csv(paths[choice-1], convert_index=(convert_to_datetime,))
        print(printer_spe(frames))
        pump_algo.PumpAlgoPlot(frames["algo_flow_mod_01_clean"],
                               title=titles[choice-1]).draw()
    elif choice == 3:
        frames = read_csv(paths[choice-1], convert_index=(convert_to_datetime,
                                                          convert_to_datetime),
                          delimiter=(";", ";"), index_col=("Date", "Date"),
                          in_conv_index=(None, None), skiprows=(1, 1))
        print(printer_spe(frames))
        S6_S5.S6S5Plotter(frames,
                          title=titles[choice-1]).draw()
    elif choice == 4:
        frames = read_csv(paths[choice-1], convert_index=(convert_to_datetime,))
        print(printer_spe(frames))
        S4.S4Plotter(frames["S4_algo_ECS_clean"],
                     title=titles[choice-1]).draw()
    elif choice == 5:
        frames = read_csv(paths[choice-1], convert_index=(convert_to_datetime,
                                                          convert_to_datetime),
                          delimiter=(";", ";"), index_col=("Date", "Date"),
                          in_conv_index=(None, None), skiprows=(1, 1))
        # bug issue : bad date formatting and length mismatch
        frames["variables_algo_clean"] = frames["variables_algo_clean"].ix[:-1, :][:]
        frames["backup_algo_clean"].index = frames["variables_algo_clean"].index
        print(printer_spe(frames))
        variable_backup.VarBackPlotter(frames,
                                       title=titles[choice-1]).draw()
    elif choice == 6:
        frames = read_csv(paths[choice-1], convert_index=(convert_to_datetime,))
        print(printer_spe(frames))
        chauff.ChauffPlotter(frames["Chauff_algo_clean"],
                             title=titles[choice-1]).draw()
    else:
        print("Please check menu")
