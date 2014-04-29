#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""

    Clean and formate a Dymola output file
    for SolisGraph software and add new fields to it xml stylesheet

"""


########################################
#### Classes and Methods imported : ####
########################################

from csv_formatter import *
from xml_parser import *
# import profile

#####################
#### Parmeters : ####
#####################

csv_in = "C:\\Users\\bois\\Documents\\GitHub\\SolarSystem\\Outputs\\raw\\" + \
         "olivier_house.csv"
csv_out = "C:\\Users\\bois\\Documents\\GitHub\\SolarSystem\\Outputs\\clean\\" + \
          "olivier_house_read.csv"
xml_in = "C:\\Users\\bois\\Documents\\SolisGraph\\SolisGraphDrawingStyles.xml"
xml_out = "C:\\Users\\bois\\Documents\\SolisGraph\\SolisGraphDrawingStyles.xml"

# Start time for timestep
start = datetime.datetime(year=2014, month=1, day=1)

# Add a description in the csv file (First row)
title = "Created on {:%B\t%d/%m/%Y %H:%M}".format(datetime.datetime.now())
units = "Temperature [°C] -- Flow [l/min]" +\
        " -- Radiation [W/m2] -- Drawing_up [l] -- State [0 or 100]"
head = title + "\t\t" + units + "\n"

date = "{:%B\t%d\t%Y at %H:%M}".format(datetime.datetime.today())

unit_converter = {"celsius": (re.compile("\AT\d+"), to_celsius),
                  "kWh": (re.compile("[A-Z]([a-z A-Z])*_Energy"), to_kwh),
                  "l_min": (re.compile("\Z\AS\d+" "|\AFlow_[A-Z]+"), to_l_min),
                  "mult_100": (re.compile("(\S+)_state"), to_100)}

# Data Template for xml
TEMPLATE = ("item", "item/first", "item/second")


#######################################
#### Classes, Methods, Functions : ####
#######################################

def parse_and_store(csv_in, csv_out, xml_in, xml_out, template):
    """
        Format csv file and update xml file with csv fields
    """

    print("\n### Csv parameters ###")
    print("Meteo file start at", start)
    print("Input file is : {}".format(csv_in))
    print("Output file is : {}".format(csv_out))
    print("\n### Xml parameters ###")
    print("Input file is : {}".format(xml_in))
    print("Output file is : {}\n\n{}".format(xml_out, "-"*50))
    flag = input("Press <Yes> to continue ... : ")
    print("-"*50)
    if flag in ("Yes", "Y", "y", "yes", "YES"):
        # Parse and clean CSV file
        print("\n### Start to build {} ###".format(csv_out))
        # Cast to set because update_xml_linestyle accept only set
        fields = set(process_actions(csv_in, csv_out, start, debug=False,
                                     D_type="real", nrows=None, head=head,
                                     convert_dicts=(field_converter,
                                                    unit_converter)))
        print("\n" + "-"*25 + "\nFields are :\n")
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
    # profile.run("parse_and_store(csv_in, csv_out, xml_in, xml_out, TEMPLATE)")
    parse_and_store(csv_in, csv_out, xml_in, xml_out, TEMPLATE)
