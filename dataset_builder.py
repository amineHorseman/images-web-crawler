#!/usr/bin/env python
""" DatasetBuilder: aggregate utilities to build large images datasets"""

from __future__ import print_function
import os
from shutil import copy2

__author__ = "Amine BENDAHMANE (@AmineHorseman)"
__email__ = "bendahmane.amine@gmail.com"
__license__ = "GPL"
__date__ = "May 6nd, 2016"
__status__ = "developpemnt"

class DatasetBuilder(object):
    """ Aggregate utilities to build large datasets (renaming files, spliting categories,
        creating labels, loading data...) """

    def __init__(self):
        print("Preparing DatasetBuilder...")

    @staticmethod
    def rename_files(source_folder, target_folder="renamed_images", extensions=('.jpg', '.png')):
        """ copy images and rename them according to the following the pattern: 1.jpg, 2.jpg..."""

        # check source_folder and target_folder:
        if not os.path.exists(source_folder):
            print("Error: source_folder does not exist")
            exit()
        if not os.path.exists(target_folder):
            print("Target folder '", target_folder, "' does not exist...")
            os.makedirs(target_folder)
            print(" >> Folder created")
        if source_folder[-1] == "/":
            source_folder = source_folder[:-1]
        if target_folder[-1] == "/":
            target_folder = target_folder[:-1]

        # copy file and rename:
        i = 1
        print("Renaming files...")
        for f in os.listdir(source_folder):
            for extension in extensions:
                if f.endswith(extension):
                    copy2(source_folder + "/" + f, target_folder + "/" + str(i) + "." + extension)
                    i = i+1
        print(" >> Files renamed and stored in: '" + target_folder + "' folder")
