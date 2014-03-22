#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""

    Clean and formate a Dymola output file
    for SolisGraph software.

"""

########################################
#### Classes and Methods imported : ####
########################################

import datetime

from functools import wraps


dict_fields = {"Time": "Date", "TRooAir.T": "Thouse[°C]", "TRooHou.y": "Thouse_hour[°C]",
               "T1.T": "T1_statique[°C]", "T2.T": "T2[°C]", "T3.T": "T3[°C]", "T4.T": "T4[°C]",
               "pump_algo.T5": "T5[°C]", "pump_algo.T3": "T3[°C]", "pump_algo.T4": "T4[°C]",
               "pump_algo.T1": "T1[°C]", "T5.T": "T5[°C]", "T7.T": "T7[°C]", "T8.T": "T8[°C]", "pump_algo.pumps_state[1]": "S6_state",
               "pump_algo.pumps_state[2]": "S5_state", "pump_algo.pumps_state[3]": "S4_state",
               "pump_algo.pumps_state[4]": "S2_state", "pump_algo.S6_outter": "S6", "pump_algo.S5_outter": "S5",
               "pump_algo.S4_outter": "S4", "pump_algo.Sj_outter[1]": "S2", "algo.Text": "Text[°C]",
               "algo.extract_TdryBulb.TminOfDay": "Tmin_day[°C]", "algo.V3V_solar_outter": "V3V_solar",
               "algo.V3V_extra_outter": "V3V_extra", "algo.backupHeater_mod.CHAUFF": "CHAUFF",
               "algo.backupHeater_mod.ECS": "ECS", "algo.backupHeater_mod.BackupHeater": "BackupHeater",
               "weaBus.HDifHor": "HDifHor[W/m2]", "weaBus.HDirNor": "HDirNor[W/m2]", "solarPanel_ISO.HDifTilIso.H": "HDifTil_collector[W/m2]",
               "solarPanel_ISO.HDirTil.H": "HDirTil_collector[W/m2]",
               "solarPanel_ISO.m_flow": "mFlow_collector[Kg/s]", "Solar_tank.port_a1.m_flow": "mFlowExtTank_bot[Kg/s]",
               "Solar_tank.port_a2.m_flow": "mFlowExtTank_top[Kg/s]", "Strorage_tank.port_a1.m_flow": "mFlow_StorTank_exch[Kg/s]"}


# Numpy sucks^^
# def convert_date(step):
#     """Format to date type before load into an array"""
#     return datetime.datetime.strftime(start + datetime.timedelta(seconds=int(step)), "%d/%m/%Y %H:%M")

# # dtype to load data with date in first column and value in other
# dt = np.dtype([('Date', 'U16'), ('T1', np.float64), ('T3', np.float64), ('T5', np.float64)])

# # Finally load csv ....
# file_in = np.loadtxt("test.csv", delimiter=",", skiprows=1, dtype=dt, converters={0: convert_date})


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


def format_step(time, start):
    """
        Clean time step and format it.
        <time>  must be a String which represent seconds (int, float, ...)
        <start> time reference ('datetime.datetime' class)
    """
    try:
        # Number with scientific notation or with no float part
        step = float(time)
    except ValueError:
        # Number with float part
        step = time.split(".")[0]
    return datetime.datetime.strftime(start +
                                      datetime.timedelta(seconds=int(step)),
                                      "%d/%m/%Y %H:%M")


#--------------------------------------------------
#------------- First choice : Slowest -------------
#--------------------------------------------------


@benchmark
def format_csv(csv_in, csv_out, start, title, delimiter=(",", ";")):
    """
        Read csv_in and write to csv_out with new time format
        Clean duplicate time step and rename field of first row to Date
        Change time step format to date like : 3600  --->  01/01/2014 01:00
        Return fields except first field ("Date")
    """

    import csv

    with open(csv_in, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=delimiter[0])
        older = ""                       # Used to compare time step
        with open(csv_out, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=delimiter[1])
            csvfile.write(title + "\t" + units + "\n")   # Add time at the top of file
            fields = ["Date"] + next(filereader)[1:]
            filewriter.writerow(fields)  # Add fields
            for row in filereader:
                if row[0] != older:
                    older = row[0]       # Keep trace of last time step
                    row[0] = format_step(row[0], start)
                    filewriter.writerow(row)
    return fields[1:]


#-----------------------------------------------------------------
#------------- Second choice : Fastest with little csv ------------
#-----------------------------------------------------------------


def getlines1(csv_in, start, delimiters):
    """
        Yield row by row with new format

        str.split() used

    """
    older = ""
    with open(csv_in, 'r') as f:
        # Yield the first row with right format
        yield f.readlines(1)[0].replace("Time", "Date")\
                               .replace("_1.y", "")\
                               .replace(delimiters[0], delimiters[1])
        for line in f:
            pas = line.split(',')[0]
            if pas != older:
                older = pas
                pas = format_step(pas, start)
                # Add formatted time and change delimiter
                # len(older) used to remove raw time from csv_in line
                yield pas + line.replace(delimiters[0],
                                         delimiters[1])[len(older):]


@benchmark
def format_csv_yield1(csv_in, csv_out, start, title, delimiters=(",", ";")):
    """
        Read csv_in and write to csv_out with new time format
        Clean duplicate time step and rename field of first row to Date
        Change time step format to date like : 3600  --->  01/01/2014 01:00

        Fastest with small csv, for more larger csv prefer :
                format_csv_yield2
                format_csv_yield22
    """
    with open(csv_out, 'w') as f:
        f.write(title + "\t" + units + "\n")
        for line in getlines1(csv_in, start, delimiters):
            f.write(line)


@benchmark
def format_csv_yield11(csv_in, csv_out, start, title, delimiters=(",", ";")):
    """
        Read csv_in and write to csv_out with new time format
        Clean duplicate time step and rename field of first row to Date
        Change time step format to date like : 3600  --->  01/01/2014 01:00
        Return fields except first field ("Date")

        Fastest with small csv, for more larger csv prefer :
                format_csv_yield2
                format_csv_yield22
    """
    with open(csv_out, 'w') as f:
        iterator = getlines1(csv_in, start, delimiters)
        fields = next(iterator)            # Kick out endline ("\n")
        f.write(title + "\t" + units + "\n")
        f.write(fields)
        for line in iterator:
            f.write(line)
        # Kick out endline ("\n") and "Date", return rest
        return fields[:-1].split(delimiters[1])[1:]


@benchmark
def format_csv_yield_test(csv_in, csv_out, start, title, delimiters=(",", ";")):
    """
        Read csv_in and write to csv_out with new time format
        Clean duplicate time step and rename field of first row to Date
        Change time step format to date like : 3600  --->  01/01/2014 01:00
        Return fields except first field ("Date")

        Fastest with small csv, for more larger csv prefer :
                format_csv_yield2
                format_csv_yield22
    """
    with open(csv_out, 'w') as f:
        iterator = getlines1(csv_in, start, delimiters)
        fields = next(iterator)            # Kick out endline ("\n")
        new_fields = fields[:-1].split(delimiters[0])
        new_fields = [field for field in change_fields(new_fields, dict_fields)]
        f.write(title + "\n")
        f.write(new_fields.join(";"))
        for line in iterator:
            f.write(line)
        # Kick out endline ("\n") and "Date", return rest
        return new_fields

#--------------------------------------------------------------
#------------- Third choice : speed with large csv ------------
#--------------------------------------------------------------


@benchmark
def format_csv_yield2(csv_in, csv_out, start, title, delimiters=(",", ";")):
    """
        Read csv_in and write to csv_out with new time format
        Clean duplicate time step and rename field of first row to Date
        Change time step format to date like : 3600  --->  01/01/2014 01:00

        Fastest with large csv, for small csv prefer :
                format_csv_yield1
                format_csv_yield11
    """
    with open(csv_out, 'w') as f:
        f.write(title + "\t" + units + "\n")
        for line in getlines2(csv_in, start, delimiters):
            f.write(line)


@benchmark
def format_csv_yield22(csv_in, csv_out, start, title, delimiters=(",", ";")):
    """
        Read csv_in and write to csv_out with new time format
        Clean duplicate time step and rename field of first row to Date
        Change time step format to date like : 3600  --->  01/01/2014 01:00
        Return fields except first field ("Date")

        Fastest with large csv, for small csv prefer :
                format_csv_yield1
                format_csv_yield11
    """
    with open(csv_out, 'w') as f:
        iterator = getlines2(csv_in, start, delimiters)
        fields = next(iterator)
        f.write(title + "\t" + units + "\n")
        f.write(fields)
        for line in iterator:
            f.write(line)
        # Kick out endline ("\n") and "Date", return rest
        return fields[:-1].split(delimiters[1])[1:]


def getlines2(csv_in, start, delimiters):
    """
       Yield row by row with new format

       Concatenation used
    """
    older = ''
    with open(csv_in, 'r') as f:
        # Yield the first row with right format
        yield f.readlines(1)[0].replace("Time", "Date")\
                               .replace("_1.y", "")\
                               .replace(delimiters[0], delimiters[1])
        for line in f:
            pas = ''
            for char in line:
                if char == ',':
                    break
                pas += char
            if pas != older:
                older = pas
                pas = format_step(pas, start)
                # Add formatted time and change delimiter
                # len(older) used to remove raw time from line
                yield pas + line.replace(delimiters[0],
                                         delimiters[1])[len(older):]


def change_fields(old_fields, dict_convert):
    """Change old_fields according to dict_convert values"""
    print(":::::", old_fields)
    for field in old_fields:
        yield dict_convert[field]

########################
#### Main Program : ####
########################


if __name__ == '__main__':

    def process_action(csv_in, csv_out, start, title):
        print("Meteo file start at", start)
        print("Input file is : {}".format(csv_in))
        print("Output file is : {}".format(csv_out))
        flag = input("Press <Yes> continue ... : ")
        if flag in ("Yes", "Y", "y", "yes", "YES"):
            fields = format_csv(csv_in, csv_out, title, start)
            print("Fields are", fields)
            print("File {} was generated without errors".format(csv_out))
        else:
            print("Treatment of {} stopped".format(csv_in))

    # Absolute or relative path
    file_in = "bad.csv"
    file_out = "clean.csv"

    # Start time for meteo file
    year, month, day = 2014, 1, 1
    start = datetime.datetime(year, month, day)

    # Add a description in the csv file (First row)
    title = "Created on {:%B\t%d/%m/%Y %H:%M}".format(datetime.datetime.now())
    units = "Temperature [°C] -- Flow [Kg/s] -- Radiation [W/m2] -- Drawing_up [l]"

    # fields = format_csv(file_in, file_out, start, title)
    # print(fields)

    # format_csv_yield1(file_in, file_out, start, title)
    # fields = format_csv_yield11(file_in, file_out, start, title)
    # print(fields)

    # format_csv_yield2(file_in, file_out, start, title)
    fields = format_csv_yield22(file_in, file_out, start, title)
    print(fields)
