#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""

    Clean and formate a Dymola output file
    for SolisGraph software.

"""

########################################
#### Classes and Methods imported : ####
########################################

import csv
import datetime
from functools import wraps

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
        <time>  must be a String
        <start> time reference ('datetime.datetime' class)
    """
    # Number with float part
    if not "e" in time and "." in time:
        time_step = time.split(".")
    # Number with scientific notation or with no float part
    else:
        time_step = [float(time), 0]
    step = datetime.timedelta(seconds=int(time_step[0]),
                              microseconds=int(time_step[1]))
    return "{:%d/%m/%Y %H:%M}".format(start + step)


@benchmark
def format_csv(csv_in, csv_out, title, start, delimiter=(",", ";")):
    """
        Read csv_in and write to csv_out with new time format
        Clean duplicate time step and rename field of first row to Date
        Change time step format to date like : 3600  --->  01/01/2014 01:00
        Return fields except first field ("Date")
    """
    with open(csv_in, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=delimiter[0])
        older = -1                       # Used to compare time step
        with open(csv_out, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=delimiter[1])
            filewriter.writerow(title)   # Add time at the top of file
            fields = ["Date"] + next(filereader)[1:]
            filewriter.writerow(fields)  # Add fields
            for row in filereader:
                if row[0] != older:
                    older = row[0]       # Keep trace of last time step
                    row[0] = format_step(row[0], start)
                    filewriter.writerow(row)
    return fields[1:]


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
    title = ["Created on {:%B\t%d/%m/%Y %H:%M}".format(datetime.datetime.now())]

    process_action(file_in, file_out, start, title)
