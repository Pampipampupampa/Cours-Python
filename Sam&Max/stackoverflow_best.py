#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""STOCK THE LAST 100 PYTHON QUESTIONS IN STACKOVERFLOW.COM"""
"SAM AND MAX"

########################################
#### Classes and Methods imported : ####
########################################

import csv
import json

from urllib import request
from datetime import datetime
from io import StringIO

#####################
#### Constants : ####
#####################

# URL
# URL = "http://data.stackexchange.com/stackoverflow/csv/165916"
# QUESTION_URL = "http://stackoverflow.com/questions/{id}"

#######################################
#### Classes, Methods, Functions : ####
#######################################


# Try 4
class Question:
    """Class which contains methods to format url request"""

    # URL : Classes attributes
    URL = "http://data.stackexchange.com/stackoverflow/csv/165916"
    QUESTION_URL = "http://stackoverflow.com/questions/{id}"

    def __init__(self, id, title, creation_date):
        self.id = id
        self.title = title
        self.creation_date = creation_date

    @property
    def date(self):
        return datetime.strptime(self.creation_date, '%Y-%m-%d %H:%M:%S')

    @property
    def url(self):
        return self.QUESTION_URL.format(id=self.id)

    # Now we can use attributes to add a method inside the class
    # We use cls instead of self because the first argument refers to the
    # actual class not actual object
    @classmethod
    def query(cls, url=URL):

            csv_data = StringIO(request.urlopen(url).read(100000).decode('utf8'))

            for question in csv.DictReader(csv_data):
                question['Post Link'] = json.loads(question['Post Link'])
                yield Question(creation_date=question['CreationDate'],
                               id=question['Post Link']['id'],
                               title=question['Post Link']['title'])


# Try 3
# class Question:
#     """Class which contains methods to format url request"""

#     def __init__(self, id, title, creation_date):
#         self.id = id
#         self.title = title
#         self.creation_date = creation_date

#     def get_creation_date(self):
#         return datetime.strptime(self.creation_date, '%Y-%m-%d %H:%M:%S')

#     def get_url(self):
#         return QUESTION_URL.format(id=self.id)


# Try 2
# def download_questions(url=URL):
#     csv_data = StringIO(request.urlopen(url).read(100000).decode('utf8'))

#     for question in csv.DictReader(csv_data):
#         # Change time format
#         question['CreationDate'] = datetime.strptime(question['CreationDate'],
#                                                      '%Y-%m-%d %H:%M:%S')
#         # Second field in json format, turn into a python object
#         question['Post Link'] = json.loads(question['Post Link'])

#         # Add url generated with the id
#         question['Post Link']['url'] = QUESTION_URL.format(id=question['Post Link']['id'])
#         yield question


# Try 3
# def download_questions(url=URL):
#         csv_data = StringIO(request.urlopen(url).read(100000).decode('utf8'))

#         for question in csv.DictReader(csv_data):

#             question['Post Link'] = json.loads(question['Post Link'])

#             # Return Question object instead of Dicts
#             yield Question(creation_date=question['CreationDate'],
#                            id=question['Post Link']['id'],
#                            title=question['Post Link']['title'])

########################
#### Main Program : ####
########################

#
# First try
#
# # Download and decode, use StringIO to simulate a file despite of
# # they are only in memory
# csv_data = StringIO(request.urlopen(URL).read(100000).decode('utf8'))
# # CSV module
# # DictReader return a list of dictionnary, one for each files entries
# for question in csv.DictReader(csv_data):
#     # Datas
#     print(question['CreationDate'])  # Date
#     print(question['Post Link'])  # Question tile and id


#
# Second try
#
# for question in download_questions():
#     # Print title and url
#     print("{title} : {url}".format(**question['Post Link']))


#
# Third try (POO)
#
# for question in download_questions():
#     # affiche le titre et l'url
#     print("{title} : {url}".format(title=question.title, url=question.get_url()))


#
# Fourth try (POO)
#
print("Questions from : {}\n".format(Question.URL))

for question in Question.query():
    # affiche le titre et l'url
    print("{date}\n{title} : {url}".format(title=question.title, url=question.url, date=question.date))
