# -*- coding:Utf8 -*-

"""
    Extract informations from a csv weather file from Meteo France
    and update a .mos file with the uploaded data.
    This script does not update longitude and lattitude and other metadata from the epws files.
"""

import pandas as pd
from numpy import all as np_all
from numpy import isnan as np_isnan
from path import path


# .mos columns names
column_name = ['#C1 Time in seconds. Beginning of a year is 0s.',
               '#C2 Dry bulb temperature in Celsius at indicated time',
               '#C3 Dew point temperature in Celsius at indicated time',
               '#C4 Relative humidity in percent at indicated time',
               '#C5 Atmospheric station pressure in Pa at indicated time',
               '#C6 Extraterrestrial horizontal radiation in Wh/m2',
               '#C7 Extraterrestrial direct normal radiation in Wh/m2',
               '#C8 Horizontal infrared radiation intensity in Wh/m2',
               '#C9 Global horizontal radiation in Wh/m2',
               '#C10 Direct normal radiation in Wh/m2',
               '#C11 Diffuse horizontal radiation in Wh/m2',
               '#C12 Averaged global horizontal illuminance in lux during minutes preceding the indicated time',
               '#C13 Direct normal illuminance in lux during minutes preceding the indicated time',
               '#C14 Diffuse horizontal illuminance in lux  during minutes preceding the indicated time',
               '#C15 Zenith luminance in Cd/m2 during minutes preceding the indicated time',
               '#C16 Wind direction at indicated time. N=0, E=90, S=180, W=270',
               '#C17 Wind speed in m/s at indicated time',
               '#C18 Total sky cover at indicated time',
               '#C19 Opaque sky cover at indicated time',
               '#C20 Visibility in km at indicated time',
               '#C21 Ceiling height in m',
               '#C22 Present weather observation',
               '#C23 Present weather codes',
               '#C24 Precipitable water in mm',
               '#C25 Aerosol optical depth',
               '#C26 Snow depth in cm',
               '#C27 Days since last snowfall',
               '#C28 Albedo',
               '#C29 Liquid precipitation depth in mm at indicated time',
               '#C30 Liquid precipitation quantity']


def Jcm2_to_Whm2(struct, column):
    """
        Convert stuct[column] from J/cm2 to Wh/m2.
          - struct is a panda dataFrame
          - column is a panda dataFrame column name
    """
    struct[column] *= 10000 / 3600


def change_weather(file_mos, file_weather, dict_transform,
                   encoding='utf-8', delimiter=";", skiprows=1,
                   header=0, index_col="Timestamp"):
    """
        Return a frame based on `file_mos` with columns inside dict_transform
        updated with `file_weather` columns. Be careful with units inside standard weather files.
            encoding : encoding of file_weather
                       default: "utf-8"
            delimiter : characters used to delimit columns of file_weather.
                        default: ";"
            skiprows : number of row to skip before data inside file_weather.
                       default: 1
            header : please fill in row number of header if exist else used None.
                     default: 0
            index_col : column name used as index (if header is not None, index_col must be inside header).
                        default: "Timestamp"
    """
    # Load file_mos. using regex for delimeter (file separator can have multiple tab ...).
    # Use of regex force python engine.
    data_mos = pd.read_csv(file_mos, delimiter=r"[\t]+", skiprows=40,
                           encoding='utf-8', header=None, names=column_name,
                           index_col=column_name[0], engine="python")
    # Load file_weather.
    data_weather = pd.read_csv(file_weather, delimiter=delimiter,
                               skiprows=skiprows, encoding=encoding,
                               header=header, index_col=index_col)
    # Select the smallest index to avoid NaN at end of file when update columns.
    mos_last, weather_last = data_mos.index[-1], data_weather.index[-1]
    if mos_last <= weather_last:
        lower_last = mos_last
    else:
        lower_last = weather_last
    # Create new table base on data_mos.
    data_output = data_mos[:lower_last].copy()
    # Update columns from data_mos with columns from data_weather and adapt units.
    for col_name in dict_transform:
        data_output[col_name] = data_weather[dict_transform[col_name][0]][:lower_last]
        # Replace all np.nan values with 0 (modelica can not parse NaN).
        data_output[col_name].fillna(0, inplace=True)
        if dict_transform[col_name][1]:
            dict_transform[col_name][1](data_output, col_name)
        print(col_name, "updated to ", dict_transform[col_name][0], "values")
    return data_output


def extract_metadata(file_mos, encoding='utf-8', nb_line=40):
    """
        Read a .mos weather file and extract all metadata.
            nb_line: number of extracted lines on the stream.
                     default: 40
    """
    metadata = []  # Default value
    with open(file_mos, 'r', encoding=encoding) as f:
        if f.readable():
            metadata = [f.readline() for line in range(nb_line)]
    return metadata


def write_mos_file(data, file_name, metadata=None, encoding='utf-8'):
    """
        Write metadata and data to a file using .mos weather format.
    """
    length = len(data.index)
    if metadata:
        mode = 'a'
        with open(file_name, 'w', encoding=encoding) as f:
            f.writelines(metadata)
    else:
        mode = 'w'
    data.to_csv(file_name, mode=mode, sep="\t", header=False,
                encoding='utf-8', index=True)
    print("dataframe length is {}".format(length))


def main(file_mos, file_weather, file_output, dict_transform):
    """
    Write to your computer a .mos file for each file in file_output according to
    file_mos, file_weather, and dict_transform.

        :file_mos .mos weather file path.
        :file_weather List of csv file path.
        :file_output Corresponding .mos file as output.
                     Must have the same order and length as file_weather.
        :dict_transform Dict of .mos columns to alter with for each file in file_weather.
                        Dict values must be a list with:
                            - first element  = corresponding csv column name.
                            - second element = a function to pass before altering .mos
                        dict_transform allows for example to replace for each csv file
                        the column 1 of the `file_mos` with column 3(first element)
                        of csv files minus 30(second element).

        :return Nothing
    """
    # Treatment for each input/output file pair.
    for source, output in zip(file_weather, file_output):
        # Extract data from .mos and weather file to create new dataframe mix
        # according to dict_transform.
        data_output = change_weather(file_mos=file_mos, file_weather=source,
                                     dict_transform=dict_transform)
        # Extract metadata from original file
        metadata = extract_metadata(file_mos)
        # Write file_output.
        write_mos_file(data=data_output, file_name=output, metadata=metadata)
        print("Weather {} done !".format(output))


if __name__ == '__main__':
    # Inputs parameters
    FOLDER = path("C:\\Users\\bois\\TEMP\\Conversion_weatherFiles")

    file_mos = FOLDER / "FRA_Bordeaux.075100_IWEC.mos"
    # Order inside tuples important.
    file_weather = (FOLDER / "Merignac_2012.txt", FOLDER / "Merignac_2013.txt",
                    FOLDER / "Merignac_2014.txt")
    file_output = (FOLDER / "Merignac_2012.mos", FOLDER / "Merignac_2013.mos",
                   FOLDER / "Merignac_2014.mos")

    # Diffuse irradiation not provide inside Meteo France data ---> fill of 0.
    dict_transform = {"#C2 Dry bulb temperature in Celsius at indicated time": ["T", None],
                      "#C9 Global horizontal radiation in Wh/m2": ["GLO", Jcm2_to_Whm2],
                      "#C10 Direct normal radiation in Wh/m2": ["DIR", Jcm2_to_Whm2],
                      "#C11 Diffuse horizontal radiation in Wh/m2": ["DIF", Jcm2_to_Whm2]}

    main(file_mos, file_weather, file_output, dict_transform)
    print("Weathers files updated !!")
