#! /usr/bin/env python
# -*- coding:Utf8 -*-


#######################################
#### Classes, Methods, Functions : ####
#######################################


def extract_nested_json1(datas, parameter, rows, cols):
    """
        Extract a third level nested json dict according to the parameter value.
            datas : dict
            parameter : integer or string
                        dict last level key extracted
            rows : list or tuple
                   dict second level keys (all keys we want to extract)
            cols : list or tuple
                   dict first level keys (all keys we want to extract)
        structure must be like this one : {first_level: {second_level: {last_level: value_of_last_level}}}
        Return a prepare dict for create a dataframe with it.

        example : datas = {"chambery":
                                      {"January":
                                                   {"solar_heating": 1,
                                                    "extra_heating": 2},
                                       "February":
                                                   {"solar_heating": 3,
                                                    "extra_heating": 4}
                                      },
                           "bordeaux":
                                      {"January":
                                                   {"solar_heating": 11,
                                                    "extra_heating": 22},
                                       "February":
                                                   {"solar_heating": 33,
                                                    "extra_heating": 44}
                                      }
                          }
                  parameter can be "solar_heating"
                  rows can be ["January", "February"]
                  cols can be ["chambery", "bordeaux"]

                  return {'bordeaux': [11, 33], 'chambery': [1, 3]}
    """
    return {col: [datas[col][row][parameter] for row in rows] for col in cols}


def extract_nested_json2(datas, parameters, rows, cols):
    """
        Extract a third level nested json dict according to the parameter value.
            datas : dict
            parameter : integer or string
                        dict last level key extracted
            rows : list or tuple
                   dict second level keys (all keys we want to extract)
            cols : list or tuple
                   dict first level keys (all keys we want to extract)
        structure must be like this one : {first_level: {second_level: {last_level: value_of_last_level}}}
        Return a prepare dict for create a dataframe with it.

        example : datas = {"chambery":
                                      {"January":
                                                   {"solar_heating": 1,
                                                    "extra_heating": 2},
                                       "February":
                                                   {"solar_heating": 3,
                                                    "extra_heating": 4}
                                      },
                           "bordeaux":
                                      {"January":
                                                   {"solar_heating": 11,
                                                    "extra_heating": 22},
                                       "February":
                                                   {"solar_heating": 33,
                                                    "extra_heating": 44}
                                      }
                          }
                  parameter = ("solar_heating", "extra_heating")
                  rows      = ["January", "February"]
                  cols      = ["chambery", "bordeaux"]

                  yield     ("solar_heating",
                             {'bordeaux': [11, 33], 'chambery': [1, 3]})
                            ("extra_heating",
                             {'bordeaux': [22, 44], 'chambery': [2, 4]})

    """
    for val in parameters:
        yield val, {col: [datas[col][row][val] for row in rows] for col in cols}
