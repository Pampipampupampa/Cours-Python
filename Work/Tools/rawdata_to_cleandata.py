# -*- coding:Utf8 -*-
# /Tools/rawdata_to_cleandata.py

"""
    Script used to provide an easy to use interface to convert a raw data file
    (for instance a csv file from acquisitions) to a ready to use dataframe.
    Another function allows to export to a file the dataframe for differents support
    Currently output support for:
        - Dymola .mos extension file (weather data).
        - Dymola .txt extension file (input data).
"""

import pandas as pd
import datetime
# Function to convert columns data using vectorization (no python loops)
from some_tools import fields_converter, celsius_to_kelvin, plus_x


def string_to_datetime(dates, pattern="%m/%d/%Y %H:%M"):
    """Parse a iterable of string according to an expression and return a generator
    of a datetime object for each date in dates.

    :param dates: An iterable of string to convert
    :param pattern: An expression used to match the string representation of a date
    :type dates: list, tuple, array, narray, generator
    :type pattern: str

    :return: A generator of date in datetime format
    :rtype: datetime.datetime
    """
    for date in dates:
        # Does not keep seconds and micro-seconds.
        yield datetime.datetime.strptime(date, pattern)


def datetime_to_timestep(dates, base_date=None):
    """Return a generator of timestep (in seconds) for each date in dates which
    is an iterable.

    :param dates: An iterable of datetime.datetime object like
    :param base_date: A datetime.datetime object used as base to compute delta
                      (default use first datetime in dates as base_date)
    :type dates: list, tuple, array, narray, generator

    :return: A generator of datetime.timedelta in seconds.
    :rtype: float
    """
    if base_date is None:
        base_date = next(dates)
        yield 0.  # (base_date - base_date).total_seconds()
    for date in dates:
        yield (date - base_date).total_seconds()


def string_to_timestep(dates, pattern="%m/%d/%Y %H:%M",
                       limits=None, base_date=None):
    """Wrap ``datetime_to_timestep`` and ``string_to_datetime`` to provide a
    direct conversion from a string representing a datetime to a timestep in
    seconds.

    :param dates: An iterable of string to convert
    :param pattern: An expression used to match the string representation of a date
    :param limits: A two element list to keep a slice of the dates string
                    - limits[0] == start of slice
                    - limits[1] == end of slice (not included)
                   (default to full string)
    :param base_date: A datetime.datetime object used as base to compute delta
                      (default use first datetime in dates as base_date)
    :type dates: list, tuple, array, narray, generator
    :type pattern: str
    :type base_date: datetime.datetime

    :return: A generator of datetime.timedelta in seconds.
    :rtype: float
    """
    if limits is None:
        return datetime_to_timestep(string_to_datetime(dates, pattern), base_date)
    else:
        return datetime_to_timestep(string_to_datetime([el[limits[0]:limits[1]] for el in dates],
                                                       pattern),
                                    base_date)


def parse_csv(csv_file, index_col=None, delimiter=",", encoding='utf-8', names=None,
              converter_func=None, not_needed=[], conv_params={}):
    """Parse a csv file and return a pandas.DataFrame object of it.

    :param csv_file: File to parse.
    :param index_col: Column from the csv_file choose as index.
                       (default auto-incrementing field is used as index)
    :param delimiter: Character used as columns separator.
    :param encoding: csv_file encoding.
    :param names: If not None, used to replace dataframe columns names.
                   Be aware, removing columns ocurs before renaming
                   .. seealso:: not_needed
    :param converter_func: If not None, used to format the index column.
    :param not_needed: If not empty, used to remove columns from the csv_file.
                        Be aware, removing columns ocurs before renaming
                        .. seealso:: names
    :param conv_params: A dict of parameter pass to converter_func function call

    :return: A pandas DataFrame object from the csv structure.
    :rtype: pandas.core.frame.DataFrame
    """
    # Get dataframe from file.
    frame = pd.read_csv(csv_file, delimiter=delimiter, encoding=encoding, index_col=index_col)
    # Remove useless columns.
    if not_needed is not None:
        for col in not_needed:
            del frame[col]
    # Rename usefull columns.
    if names is not None:
        frame.columns = names
    # Update index according to converter_func (remove index name).
    if converter_func is not None:
        frame.index = (el for el in converter_func(frame.index, **conv_params))
    if index_col is not None:
        frame.index.name = index_col
    return frame


def write_dymola_file(frame, output_file, data_name, delimiter="\t",
                      float_format=None, encoding='utf-8'):
    """Write a mos file using Dymola format.

    :param frame: A DataFrame object.
    :param output_file: The output file.
    :param data_name: The name used inside the file to describe the data.
    :param encoding: Encoding of the output file.

    :return: None
    """
    # Write metadata on the file.
    with open(output_file, 'w', encoding=encoding) as mos:
        # Line separator are not added by default (Unix style used here).
        mos.write("#1\n")
        rows, cols = frame.shape
        mos.write("double {}({}, {})\n".format(data_name, rows, cols+1))
        mos.write("#C1 {}\n".format(frame.index.name))
        mos.writelines(("#C{} {}\n".format(ind+2, el) for ind, el in enumerate(frame.columns)))
    # Append dataframe to the file.
    frame.to_csv(output_file, mode="a", sep=delimiter, float_format=float_format,
                 header=False, index=True, encoding=encoding)
    return


if __name__ == '__main__':
    # Parameters.
    FOLDER = "C:\\Users\\bois\\Downloads\\Temp\\"
    test_file = FOLDER + "dat00001.csv"
    output_file = FOLDER + "test.txt"
    converter = string_to_timestep
    converter_dict = {"limits": [0, -7], "pattern": "%m/%d/%Y %H:%M"}
    NEW_COLUMNS = ("101_Tdepart_secondaire", "102_Tretour_secondaire", "105_Tsol_1.6m",
                   "106_Tfondations_14ml", "107_Tsol_1.2m", "108_Tfondations_5ml",
                   "109_Tsol_0.6m", "110_Tfondations_26ml",
                   "115_Tdepart_primaire", "116_Tretour_primaire")
    # NEW_COLUMNS = ("101_Tdepart_secondaire", "102_Tretour_secondaire", "105_Tsol_1.6m",
    #                "106_Tfondations_14ml", "107_Tsol_1.2m", "108_Tfondations_5ml",
    #                "109_Tsol_0.6m", "110_Tfondations_26ml", "114_Tplafond_sejour",
    #                "115_Tdepart_primaire", "116_Tretour_primaire",
    #                "117_Tint_0.1m", "118_Tint_1.1m", "119_Tint_1.7m",
    #                "120_Tplafond_cuisine", "122_Humidite")
    operations = {field: celsius_to_kelvin for field in NEW_COLUMNS}

    # #
    # #   Test algorithm implementation   #
    # #
    # # Get a clean dataframe.
    # frame = parse_csv(test_file, index_col="Time", converter_func=converter,
    #                   names=NEW_COLUMNS, not_needed=["Sweep #"],
    #                   conv_params=converter_dict)
    # # Change data units.
    # fields_converter(frame, operations)
    # print("Dataframe data processed.\n")

    # # Write to the computer.
    # write_dymola_file(frame, output_file=output_file, float_format="%.3f", data_name="dat00001")
    # print("Frame wrote to << {} >> using Dymola style.\n".format(output_file))
    # print("Script over, now closing.")

    #
    # Recursively prepare all files in each folder of foundations.
    #
    from path import path

    # Get root folder where we will start search recursively.
    # root = path("D:\Github\Projets\IGC\Etudes\Etude_experimentale_PlafinoInnovert\Experimentations\Data\Fondations")
    root = path("D:\Github\Projets\IGC\Etudes\Etude_experimentale_PlafinoInnovert\Experimentations\Data\Fondations\Experience_4\\20150724_123823654")
    print("Enter in ", root, "\n")
    for inlet in root.walk(pattern="*001.csv"):
        outlet = inlet.parent / inlet.namebase + ".txt"
        print("-----")
        print("Open: \n", inlet)

        frame = parse_csv(inlet, index_col="Time", converter_func=converter,
                          names=NEW_COLUMNS, not_needed=["Sweep #"],
                          conv_params=converter_dict)
        print("Do:")
        # °C to Kelvin
        print("Update temperature to Kelvin.")
        fields_converter(frame, operations)
        # Data shift.
        print("Compute data shifting.")
        shifts = {"105_Tsol_1.6m": [{"x": -2.606}, plus_x],
                  "106_Tfondations_14ml": [{"x": -2.540}, plus_x],
                  "107_Tsol_1.2m": [{"x": -0.562}, plus_x],
                  "108_Tfondations_5ml": [{"x": -2.606}, plus_x],
                  "110_Tfondations_26ml": [{"x": -2.318}, plus_x]}
        # shifts = {}
        fields_converter(frame, shifts)
        write_dymola_file(frame, output_file=outlet, float_format="%.3f", data_name="dat00001")
        print("Write: \n", outlet)
        print("-----")
        print()
