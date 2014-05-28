#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""Renaming class constructor"""

########################################
#### Classes and Methods imported : ####
########################################

import os
import re

#####################
#### Constants : ####
#####################


# Regex and folder parmeter for music file before burning
REGEX_MP3 = re.compile("\A[0-9]{2}\. " "|\A[0-9]{2} \- " "|\A[0-9]{2}[ \-]")
FOLDER_MP3 = "/home/pampi/Output/cd_test/"


#######################################
#### Classes, Methods, Functions : ####
#######################################


class RenameMe:
    """
        In all files inside a directory (self.path) delete a part of the name
        according to regex and rename old file.
        To check another folder you only have to set self.path to new directory.

        Can be used to remove numbered songs like "10 song_nb.mp3".
    """

    def __init__(self, path="", regex=REGEX_MP3):
        self.path = path
        self.regex = regex

    def change_regex(self, source, regex_expr=r'', replacement="", mode="rb"):
        """
            Change file name according to regex replacement and path variable
        """
        with open(source, mode) as f:
            old = f.name[len(self.path):]
            new = re.sub(self.regex, replacement, old)
            os.rename(f.name, self.path+new)
            if old is not new:
                print(old, "------->", new)
            else:
                print(old, " didn't change")

    def regex_loop(self):
        """
            Check all elements inside self.path directory and call
            change if element is a file
        """
        for mp3 in os.listdir(self.path):
            if os.path.isfile(self.path+mp3):
                self.change_regex(self.path+mp3)


########################
#### Main Program : ####
########################

if __name__ == '__main__':
    cd_dir = RenameMe(FOLDER_MP3)
    cd_dir.regex_loop()
