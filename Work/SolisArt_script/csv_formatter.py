#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""

    Clean and formate a Dymola output file
    for SolisGraph software.

"""

########################################
#### Classes and Methods imported : ####
########################################


import pandas as pd
import re        # Regex
import datetime  # Datetime parser

from functools import wraps  # Keep trace of decorated functions arguments


######################
#### Parameters : ####
######################

# Fields converters
field_converter = {"T0.T": "T1_statique[°C]", "pump_algo.T1": "T1",
                   "T2.T": "T2", "T3.T": "T3", "pump_algo.T3": "T3",
                   "T4.T": "T4", "pump_algo.T4": "T4",
                   "T5.T": "T5", "pump_algo.T5": "T5",
                   "pump_algo.T7": "T7", "pump_algo.T8": "T8",
                   "algo.Text": "T9_ext", "TRooAir.T": "T12_house",
                   "pump_algo.pumps_state[1]": "S6_state",
                   "pump_algo.pumps_state[2]": "S5_state",
                   "pump_algo.pumps_state[3]": "S4_state",
                   "pump_algo.pumps_state[4]": "S2_state",
                   "pump_algo.S6_outter": "Flow_S6",
                   "pump_algo.S5_outter": "Flow_S5",
                   "pump_algo.S4_outter": "Flow_S4",
                   "pump_algo.Sj_outter[1]": "Flow_S2",
                   "algo.V3V_solar_outter": "Vsolar_state",
                   "algo.V3V_extra_outter": "Vextra_state",
                   "algo.backupHeater_mod.CHAUFF": "CHAUFF_state",
                   "algo.backupHeater_mod.ECS": "ECS_state",
                   "algo.BackupHeater_outter": "Backup_algo_state",
                   "boi.y": "Backup_state",
                   "solarPanel_ISO.m_flow": "Flow_Collector",
                   "Solar_tank.port_a1.m_flow": "Flow_ExchTank_bot",
                   "Solar_tank.port_a2.m_flow": "Flow_ExchTank_top",
                   "Storage_tank.port_a1.m_flow": "Flow_ExchStorTank",
                   "mFlow_boiler.m_flow": "Flow_Boiler",
                   "boi.m_flow": "Flow_Boiler",
                   "weaBus.HDifHor": "HDifHor",
                   "weaBus.HDirNor": "HDirNor",
                   "solarPanel_ISO.HDifTilIso.H": "HDifTil_collector",
                   "solarPanel_ISO.HDirTil.H": "HDirTil_collector",
                   "integrator_collector.Energy": "Collector_Energy",
                   "integrator_boiler.Energy": "Boiler_Energy",
                   "integrator_radiator.Energy": "Radiator_Energy",
                   "integrator_drawingUp.Energy": "DrawingUp_Energy",
                   "TRooHou1.y": "T12_hour", "roo.heaPorRad.T": "T12_rad_house",
                   "TRooDay.y": "T12_day", "roo.radTem.TRad": "T12_rad_house",
                   "PHea.y": "House_Power", "product.y": "Flow_Extraction",
                   "EHea.y": "House_Energy", "miniAverage.TminOfDay": "T9_mini",
                   "miniAverage.TmoyOfDay": "T9_moy",
                   "weaDat.weaBus.TDryBul": "T9_ext"
                   }

#######################################
#### Classes, Methods, Functions : ####
#######################################


def benchmark(func):
    """
        Time function
    """
    import time

    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.process_time()
        res = func(*args, **kwargs)
        print("{} has spent {} sec to finish".format(func.__name__,
                                                     time.process_time()-t))
        return res
    return wrapper


def convert_to_datetimestring(step, start):
    """
        This parser convert into a solisart software format
    """
    for el in step:
        yield datetime.datetime.strftime(start +
                                         datetime.timedelta(seconds=int(el)),
                                         "%d/%m/%Y %H:%M")


def to_celsius(struct, column):
    """
        Kelvin temperature into Celsius inside struct[column].
          - struct is a panda dataFrame
          - column is a panda dataFrame column name
    """
    struct[column] -= 273.15


def to_l_min(struct, column):
    """
        Kg/s mass flow rate into a l/min flow rate inside struct[column].
        Constant density used : 1000 Kg/m3.
          - struct is a panda dataFrame
          - column is a panda dataFrame column name
    """
    struct[column] *= 60


def to_100(struct, column):
    """
        Multiply per 100 values inside struct[column].
          - struct is a panda dataFrame
          - column is a panda dataFrame column name
    """
    struct[column] *= 100


def to_kwh(struct, column):
    """
        Joules into KWh inside struct[column].
          - struct is a panda dataFrame
          - column is a panda dataFrame column name
    """
    struct[column] /= (1000.*3600.)


def change_fields(struct, convert_dico):
    """
        Change all fields according to convert_dico.
          - struct is a panda dataFrame
          - convert_dico must be a dict
    """
    # Change columns names
    for field in struct.columns:
        try:
            # Try to change columns fields
            yield convert_dico[field]

        except KeyError:
            # Catch exception if a field is not inside the convert_dico dict
            # Allows to change only needed fields
            print("No < {} > key inside convert_dict, ".format(field) +
                  "value pass without changing")
            yield field


def cast_columns(struct, convert_dico, debug=False):
    """
        Cast all values inside each columns according to a converter
        and a regular expression.
          - struct is a panda dataFrame
          - convert_dico must be a dict
          - debug add a convert_dico key printer
    """
    for column in struct.columns:
        for key in convert_dico.keys():
            if re.match(convert_dico[key][0], column):
                convert_dico[key][1](struct, column)
                if debug:
                    print(key)
                # Cut loop to avoid wasting time with other match testing
                break


def remove_duplicate(struct):
    """
        Removes all duplicated rows according to index column
          - struct is a panda dataFrame
    """
    print("\nRemoves Duplicated rows from <{}> column".format(struct.index.name))
    before = len(struct.index)
    struct = struct.groupby(struct.index).last()
    after = len(struct.index)
    # Forces the field to be right-aligned within the available space
    print("Before treatment : {0:{fill}{align}6} rows".format(before,
                                                              fill=" ",
                                                              align=">"))
    print("After treatment  : {0:{fill}{align}6} rows".format(after,
                                                              fill=" ",
                                                              align=">"))
    print("-"*10 + ">" + " "*7 +
          " {0:{fill}{align}6} removed\n".format(before-after,
                                                 fill=" ",
                                                 align=">"))
    # Return reorganized struct
    return struct


@benchmark
def process_actions(in_file, out_file, start_time, seps=(",", ";"),
                    csv_index="Time", skiprows=None, nrows=None,
                    convert_dicts=({}, {}), head=None, index_name="Date",
                    float_format="%.2f", debug=False):
    """
        Load and format the csv file.
        Return all fields except the index one.
          - in_file is the input csv file
          - out_file is the output csv file
          - seps is a tuple or list of in and out file
          - csv_index is the column name to convert into index column
          - skiprows allows to start read the in_file after <x> rows
          - nrows allows to read the in_file during <x> rows
          - convert_dicts contains two dicts :
                    field converter : to convert columns names
                    data converter : to change columns data value
          - head used to add some text before structure inside out_file
          - index_name is the new name of out_file index column
          - float_format is the float format of outputs
          - debug add a convert_dico key printer
    """
    # Open csv
    new_csv = pd.read_csv(in_file, nrows=nrows, delimiter=seps[0],
                          skiprows=skiprows, index_col=csv_index)

    # Change all fields names
    new_csv.columns = [field for field in change_fields(new_csv,
                                                        convert_dicts[0])]

    # Remove all duplicated rows and keep only last one
    new_csv = remove_duplicate(new_csv)

    # Procceed to conversions
    cast_columns(new_csv, convert_dico=convert_dicts[1], debug=debug)
    new_csv.index = [ind for ind in convert_to_datetimestring(new_csv.index,
                                                              start_time)]
    new_csv.index.name = index_name

    # Write new_csv to out_file
    with open(out_file, "w") as f:
        f.write(head)
    new_csv.to_csv(out_file, sep=seps[1], mode="a",
                   index=True, float_format=float_format)

    # Return all fields names except first one
    return new_csv.columns
    # return new_csv


########################
#### Main Program : ####
########################


if __name__ == '__main__':

    csv_in = "bad.csv"

    csv_out = "clean.csv"

    # Start time for timestep
    start = datetime.datetime(year=2014, month=1, day=1)
    start

    # Add a description in the csv file (First row)
    title = "Created on {:%B\t%d/%m/%Y %H:%M}".format(datetime.datetime.now())
    units = "Temperature [°C] -- Flow [l/min]" +\
            " -- Radiation [W/m2] -- Drawing_up [l] -- State [0 or 100]"
    head = title + "\t\t" + units + "\n"

    unit_converter = {"celsius": (re.compile("\AT\d+"), to_celsius),
                      "kWh": (re.compile("[A-Z]([a-z A-Z])*_Energy"), to_kwh),
                      "l_min": (re.compile("\Z\AS\d+" "|\AFlow_[A-Z]+"), to_l_min),
                      "mult_100": (re.compile("(\S+),_state"), to_100)}

    fields = process_actions(csv_in, csv_out, start, nrows=20, head=head,
                             convert_dicts=(field_converter, unit_converter))

    print(fields)
