#!/usr/bin/env python
""" DatasetBuilder: aggregate utilities to build large images datasets"""

from __future__ import print_function
import os
from shutil import copy2
from scipy import ndimage, misc

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
    def check_folder_existance(folderpath, throw_error_if_no_folder=False):
        """ check if a folder exists.
        If throw_error_if_no_folder = True and the folder does not exist:
            the method will print an error message and stop the program,
        Otherwise:
            the method will create the folder
        """
        if not os.path.exists(folderpath):
            if throw_error_if_no_folder:
                print("Error: folder '" + folderpath + "' does not exist")
                exit()
            else:
                print("Target folder '", folderpath, "' does not exist...")
                os.makedirs(folderpath)
                print(" >> Folder created")

    @classmethod
    def rename_files(cls, source_folder, target_folder, extensions=('.jpg', '.jpeg', '.png')):
        """ copy images and rename them according to the following the pattern: 1.jpg, 2.jpg..."""

        # check source_folder and target_folder:
        cls.check_folder_existance(source_folder, throw_error_if_no_folder=True)
        cls.check_folder_existance(target_folder)
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
                    copy2(source_folder + "/" + f, target_folder + "/" + str(i) + extension)
                    i = i+1
        print(" >> Files renamed and stored in: '" + target_folder + "' folder")

    @classmethod
    def reshape_images(cls, source_folder, target_folder, height=128, width=128, extensions=('.jpg', '.jpeg', '.png')):
        """ copy imaegs and reshape them"""

        # check source_folder and target_folder:
        cls.check_folder_existance(source_folder, throw_error_if_no_folder=True)
        cls.check_folder_existance(target_folder)
        if source_folder[-1] == "/":
            source_folder = source_folder[:-1]
        if target_folder[-1] == "/":
            target_folder = target_folder[:-1]

        # read imaegs and reshape:
        print("Reshapng files...")
        for f in os.listdir(source_folder):
            for extension in extensions:
                if f.endswith(extension):
                    copy2(source_folder + "/" + f, target_folder + "/" + f)
                    image = ndimage.imread(target_folder + "/" + f, mode="RGB")
                    image_resized = misc.imresize(image, (height, width))
                    misc.imsave(target_folder + "/" + f, image_resized)
        print(" >> Images reshaped")
