#! /usr/bin/env pythona
# -*- coding:Utf8 -*-


"""

    Clean and formate a Dymola output file
    for SolisGraph software and add new fields to it xml stylesheet

# Fields
Time,T1[K],T3[K],T4[K],T5[K],T7[K],T8[K],V3V_solar,V3V_extra,BackupHeater,
boiler_state,S6_state,S5_state,S4_state,S2_state,S6_value,S5_value,S4_value,
S2_value,Thouse[K],Thouse_per_hour[K],Text[K],HDifHor[W/m2],HDirNor[W/m2],
HDifTil_collector[W/m2],HDirTil_collector[W/m2],Drawing_up_need[l],
Drawing_up_evolution[l],mFlow_collector[Kg/s],mFlow_StorageTank_exchanger[Kg/s],
mFlowExtraTank_top[Kg/s],mFlowExtraTank_bottom[Kg/s],mFlow_boiler[Kg/s],
mFlow_radiator[Kg/s]

"""

########################################
#### Classes and Methods imported : ####
########################################

from csv_formatter import *
from xml_parser_add import *

#####################
#### Parmeters : ####
#####################

csv_in = "C:\\Users\\bois\\Documents\\Dymola\\Data\\raw\\" + \
         "feb_SolisConfort_rad.csv"
csv_out = "C:\\Users\\bois\\Documents\\Dymola\\Data\\clean\\" + \
          "feb_SolisConfort_rad.csv"
xml_in = "C:\\Users\\bois\\Documents\\SolisGraph\\SolisGraphDrawingStyles.xml"
xml_out = "C:\\Users\\bois\\Documents\\SolisGraph\\SolisGraphDrawingStyles.xml"

# Start time for meteo file (used to transform time step to date)
year, month, day = 2014, 1, 1
start = datetime.datetime(year, month, day)

# Add a description in the csv file (First row)
title = "Created on {:%B\t%d/%m/%Y %H:%M}".format(datetime.datetime.now())
date = "{:%B\t%d\t%Y at %H:%M}".format(datetime.datetime.today())

# Data Template for xml
TEMPLATE = ("item", "item/first", "item/second")

#######################################
#### Classes, Methods, Functions : ####
#######################################


def parse_and_store(csv_in, csv_out, xml_in, xml_out, template):
    """Format csv file and update xml file with csv fields"""
    print("\n### Csv parameters ###")
    print("Meteo file start at", start)
    print("Input file is : {}".format(csv_in))
    print("Output file is : {}".format(csv_out))
    print("\n### Xml parameters ###")
    print("Input file is : {}".format(xml_in))
    print("Output file is : {}\n\n{}".format(xml_out, "-"*50))
    flag = input("Press <Yes> to continue ... : ")
    # flag = "YES"
    print("-"*50)
    if flag in ("Yes", "Y", "y", "yes", "YES"):
        # Parse and clean CSV file
        print("\n### Start to build {} ###".format(csv_out))
        # Cast to set because update_xml_linestyle accept only set
        fields = set(format_csv_yield11(csv_in, csv_out, start, title))
        # print("Fields are", fields)
        print("\nFields are :\n" + "-"*25)
        for field in fields:
            print(field)
        print("-"*25, "\n")
        print(" ----> File {} \n was generated without errors".format(csv_out))
        # Update XML file
        print("\n### Start to build {} ###".format(xml_out))
        update_xml_linestyle(xml_in, xml_out, template, fields, date)
        print(" ----> File {} was generated without errors\n".format(xml_out))
    else:
        print("\nTreatment of {} \nstopped".format(csv_in))
        print("Treatment of {} \nstopped".format(xml_in))
        print(" ----> Nothing change\n")
        return

########################
#### Main Program : ####
########################

if __name__ == '__main__':
    parse_and_store(csv_in, csv_out, xml_in, xml_out, TEMPLATE)
