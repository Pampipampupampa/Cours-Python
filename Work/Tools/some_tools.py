# -*- coding:Utf8 -*-
# /Tools/some_tools.py

"""
    List of class and function which can be useful or not ...
"""


# def fields_converter(frame, fields_operation):
#     """Inline conversion field according to fields_operation dictionnary.

#     :param frame: A pandas DataFrame
#     :param fields_operation: Operation on the field (function) map to column name.
#     :type fields_operation: dict
#     """
#     for field, args in fields_operation.items():
#         func = args.pop()
#         func(frame, field, *args)
#     return


def fields_converter(frame, fields_operation):
    """Inline conversion field according to fields_operation dictionnary.

    :param frame: A pandas DataFrame
    :param fields_operation: Operation on the field (function) map to column name.
                             You can pass an ordered list compose of two element:
                                - named arguments as a dict
                                - function to call as a string
                             Named arguments will be passed at function call.
    :type fields_operation: dict
    """
    for field, args in fields_operation.items():
        # If structure implements pop() we have named arguments.
        if hasattr(args, "pop"):
            func = args.pop()
            func(frame, field, **args[0])
        else:
            # If alone args must be the function
            args(frame, field)
    return


def kelvin_to_celsius(struct, column):
    """Convert stuct[column] from Kelvin to Celsius.

    :param struct: A pandas DataFrame
    :param column: A pandas DataFrame field name (a column name)
    """
    struct[column] -= 273.15


def celsius_to_kelvin(struct, column):
    """Convert stuct[column] from Celsius to Kelvin.

    :param struct: A pandas DataFrame
    :param column: A pandas DataFrame field name (a column name)
    """
    struct[column] += 273.15


def kgs_to_lmin(struct, column):
    """Convert stuct[column] from kg/s to l/min.

    :param struct: A pandas DataFrame
    :param column: A pandas DataFrame field name (a column name)
    """
    struct[column] *= 60


def per_x(struct, column, x):
    """Each element of stuct[column] time 100.

    :param struct: A pandas DataFrame
    :param column: A pandas DataFrame field name (a column name)
    :param x: Multiplicator
    """
    struct[column] *= x


def plus_x(struct, column, x):
    """Each element of stuct[column] time 100.

    :param struct: A pandas DataFrame
    :param column: A pandas DataFrame field name (a column name)
    :param x: Multiplicator
    """
    struct[column] += x


def Jcm2_to_Whm2(struct, column):
    """Convert stuct[column] from J/cm2 to Wh/m2.

    :param struct: A pandas DataFrame
    :param column: A pandas DataFrame field name (a column name)
    """
    struct[column] *= 10000 / 3600


def pression_CIPM(temperature):
    """Compute the density of water using the CIPM method with
        - a1, a2, a4 == [°C]
        - a3 == [°C2]
        - a5 == [kg/m3]

    :param temperature: Temperature °C
    :type temperature: int, float

    :return: Density of water
    :rtype: int, float
    """
    a1, a2, a3, a4, a5 = -3.983035, 301.797, 522528.9, 69.34881, 999.974950
    return a5 * (1 - ((temperature + a1)**2 * (temperature + a2) / (a3 * (temperature + a4))))


if __name__ == '__main__':
    pass
