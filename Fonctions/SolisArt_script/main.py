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
from xml_parser_add import *

#####################
#### Parmeters : ####
#####################

csv_file = "bad.csv"
csv_out = "clean.csv"
xml_file = "SolisGraphDrawingStyles.xml"
xml_out = "output.xml"

# Start time for meteo file (used to transform time step to date)
year, month, day = 2014, 1, 1
start = datetime.datetime(year, month, day)

# Add a description in the csv file (First row)
title = ["Created on {:%B\t%d/%m/%Y %H:%M}".format(datetime.datetime.now())]
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
    print("-"*50)
    if flag in ("Yes", "Y", "y", "yes", "YES"):
        # Parse and clean CSV file
        print("\n### Start to build {} ###".format(csv_out))
        # Cast to set because update_xml_linestyle accept only set
        fields = set(format_csv(csv_in, csv_out, title, start))
        print("Fields are", fields)
        print(" ----> File {} was generated without errors".format(csv_out))
        # Update XML file
        print("\n### Start to build {} ###".format(xml_out))
        update_xml_linestyle(xml_in, xml_out, template, fields, date)
        print(" ----> File {} was generated without errors\n".format(xml_out))
    else:
        print("\nTreatment of {} stopped".format(csv_in))
        print("Treatment of {} stopped".format(xml_in))
        print("Nothing change\n")
        return

########################
#### Main Program : ####
########################

if __name__ == '__main__':
    parse_and_store(csv_file, csv_out, xml_file, xml_out, TEMPLATE)
