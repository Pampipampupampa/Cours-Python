#! /usr/bin/env python
# -*- coding:Utf8 -*-

#
# Generation of scenarios which can be used inside Modelica as input.
#

import csv

from itertools import chain, islice


def chunks_iterator(iterable, size, out_format=tuple):
    """Can be used to extract element by chunk from many iterable (tuple, list, generator, files, ...)
    >>> l = ["a", "b", "c", "d", "e", "f", "g"]
    >>> for morceau in morceaux(l, 3):
    ...         print(morceau)
    ("a", "b", "c")
    ("d", "e", "f")
    ("g",)
    """
    it = iter(iterable)
    # Will break when chain throws the warning StopIteration.
    while True:
        # Yield next element in the iterable followed by the next size - 1 elements
        yield out_format(chain((next(it),), islice(it, size - 1)))


def extract_rows_from(input_file, delimiter=",", map_format=int, encoding="utf-8",
                      mode='r'):
    """Extract a table from a csv file. Return a generator of rows"""
    with open(input_file, mode=mode, encoding=encoding) as csv:
        for row in csv.readlines():
            yield [el for el in map(map_format, row[:-1].split(delimiter))]


def extract_columns_from(input_file, headers=None, caster=(int, float), delimiter=",", encoding="utf-8", mode='r'):
    """Extract a table from a csv file. Return a generator of columns"""
    fieldnames = headers or [1, 2, 3, 4, 5, 6, 7]
    with open(input_file, mode=mode, encoding=encoding) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=delimiter, fieldnames=fieldnames)
        mapper = {}
        for row in reader:
            for col in row:
                # Float
                if "." in row[col]:
                    mapper.setdefault(col, []).append(caster[1](row[col]))
                # Integer
                else:
                    mapper.setdefault(col, []).append(caster[0](row[col]))
    return mapper


def week_schedule_from_table(files, start=0, step_size=1, out_format=list, **kwargs):
    """Construct a schedule base on a table as input file.
    Each columns will be concatenated together and time step added for each value.
    Each file will be added as a new column inside the table.

    :param files: Can be a list of path or just a unique file path.
    """
    time_step = start
    schedule = "["
    if hasattr(files, "pop"):
        mappers = [extract_columns_from(file_input, **kwargs) for file_input in files]
    else:
        mappers = [extract_columns_from(files, **kwargs)]
    for col in mappers[0]:
        for index in range(0, len(mappers[0][col])):
            elements = ", ".join(map(str, [mapper[col][index] for mapper in mappers]))
            schedule += "{}, {}; ".format(time_step * step_size, elements)
            time_step += 1
    # Used to double the last step due to how combitable on Modelica works
    # Necessary only when using `Modelica.Blocks.Types.Extrapolation.Periodic`.
    schedule += "{}, {}; ".format(time_step * step_size, elements)
    return schedule[:-2] + "]"


def construct_table(input_file, start=0, step_size=1, **kwargs):
    """Construct a schedule base on a table as input file.
    Each row will be map to a time step beginning at start.
    """
    table = extract_rows_from(input_file, **kwargs)
    time_step = start
    scenario = "[" + ", ".join(map(str, [time_step] + next(table)))
    for row in table:
        time_step += 1
        scenario = scenario + "; ".format(time_step * step_size) + ", ".join(map(str, row))
    return scenario + "]"


if __name__ == '__main__':
    # TEST

    # # Test chunks_iterator.
    # alist = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 70.0, 70.0, 70.0, 70.0,
    #          70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    #          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 70.0, 70.0, 70.0, 70.0,
    #          70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    #          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 70.0, 70.0, 70.0, 70.0,
    #          70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    #          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 70.0, 70.0, 70.0, 70.0,
    #          70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    #          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 70.0, 70.0, 70.0, 70.0,
    #          70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    #          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 70.0, 70.0, 70.0, 70.0,
    #          70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
    #          0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 70.0, 70.0, 70.0, 70.0,
    #          70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # for el in chunks_iterator(alist, 24):
    #     print(el)

    # # Test extract_rows_from.
    # table = extract_rows_from("table.csv")
    # for row in table:
    #     print(row)

    # # Test construct_table.
    # print(construct_table("table.csv", delimiter=","))

    # # Test extract_columns_from.
    # print(extract_columns_from("table.csv")[1])

    # Test week_schedule_from_table.
    # week_schedule_from_table(["table.csv", "table.csv", "table.csv"])

    #
    # Generation of IGC schedules
    #
    # FOLDER = "D://Github//Projets//IGC//Etudes//Simulations_Air_Solaire_maisonIndividuelle//Simulations//Scenarios//"
    # FOLDER = "D://Github//Projets//IGC//Etudes//Simulations_Air_Solaire_maisonIndividuelle//Etude//Scenarios//"
    # occupancy, lights, equipments = FOLDER + "occupancy.csv", FOLDER + "lights.csv", FOLDER + "equipments_RT2012.csv"

    # consigne, solaire, ventilation = FOLDER + "consigne.csv", FOLDER + "solaire.csv", FOLDER + "ventilation.csv"
    # consigneRT = FOLDER + "consigneRT.csv"
    # hiver_occ = FOLDER + "occultation_hiver.csv"
    # ete_est_occ, ete_ouest_occ = FOLDER + "occultation_ete_est.csv", FOLDER + "occultation_ete_ouest.csv"
    # puisage_soir, puisage_soir_4pers = FOLDER + "puisage_soir.csv", FOLDER + "puisage_soir_4pers.csv"

    # puisage_reparti, puisage_matin = FOLDER + "puisage_reparti.csv", FOLDER + "puisage_matin.csv"
    # consigne_19_16 = FOLDER + "consigne_19_16.csv"
    # consigne_solaire_10_10 = FOLDER + "consigne_solaire_10_10.csv"
    # consigne_19_18_16 = FOLDER + "consigne_19_18_16.csv"
    # consigne_20_18_16, consigne_solaire_22_10, ventilation_hygroB = (FOLDER + "consigne_20_18_16.csv",
    #                                                                  FOLDER + "consigne_solaire_22_10.csv",
    #                                                                  FOLDER + "ventilation_hygroB.csv")
    # ventilation_hygroA = FOLDER + "ventilation_hygroA.csv"

    # schedule = week_schedule_from_table([occupancy, lights, equipments],
    #                                     step_size=3600, delimiter=",")
    # schedule = week_schedule_from_table([consigne_19_18_16, consigne_solaire_10_10, ventilation_hygroB],
    #                                     step_size=3600, delimiter=",")
    # schedule = week_schedule_from_table([consigne_20_18_16, consigne_solaire_22_10, ventilation_hygroB],
    #                                     step_size=3600, delimiter=",")
    # schedule = week_schedule_from_table([ventilation],
    #                                     step_size=3600, delimiter=",")
    # schedule = week_schedule_from_table([consigne, solaire],
    #                                     step_size=3600, delimiter=",")
    # schedule = week_schedule_from_table(consigneRT,
    #                                     step_size=3600, delimiter=",")
    # schedule = week_schedule_from_table([occupancy, lights, equipments, hiver_occ, ete_est_occ, ete_ouest_occ],
    #                                     step_size=3600, delimiter=",")
    # schedule = week_schedule_from_table(FOLDER + "puisage_soir_4pers.csv",
    #                                     step_size=3600, delimiter=",")

    FOLDER = "D://Github//Projets//IGC//Etudes//Simulations_Air_Solaire_maisonIndividuelle//Etude_201611//Scenarios//"
    puisage_reparti33 = FOLDER + "puisage_reparti_33.csv"
    puisage_EN12977_27, puisage_EN12977_33, puisage_EN12977_40 = (FOLDER + "puisage_EN12976_27.csv",
                                                                  FOLDER + "puisage_EN12976_33.csv",
                                                                  FOLDER + "puisage_EN12976_40.csv")
    puisage_matin33, puisage_soir33 = (FOLDER + "puisage_matin_33.csv",
                                       FOLDER + "puisage_soir_33.csv")
    # puisage_matin27, puisage_soir27 = (FOLDER + "puisage_matin_27.csv",
    #                                    FOLDER + "puisage_soir_27.csv")
    # puisage_matin40, puisage_soir40 = (FOLDER + "puisage_matin_40.csv",
    #                                    FOLDER + "puisage_soir_40.csv")
    # occupation = FOLDER + "occupation.csv"
    # eclairage = FOLDER + "eclairageRT2012.csv"
    # equipement = FOLDER + "equipementRT2012.csv"
    # consigne_20_18_16, consigne_19_18_16 = (FOLDER + "consigne_20_18_16.csv",
    #                                         FOLDER + "consigne_19_18_16.csv")
    # consigne_solaire_22_10 = FOLDER + "consigne_solaire_22_10.csv"
    # consigne_solaire_variable_10 = FOLDER + "consigne_solaire_variable_10.csv"
    # ventilation_hygroA, ventilation_hygroB = (FOLDER + "ventilation_hygroA.csv",
    #                                           FOLDER + "ventilation_hygroB.csv")
    # schedule = week_schedule_from_table([consigne_19_18_16, consigne_solaire_variable_10, ventilation_hygroA],
    #                                     step_size=3600, delimiter=",")
    schedule = week_schedule_from_table(puisage_soir33,
                                        step_size=3600, delimiter=",")

    print(schedule)
