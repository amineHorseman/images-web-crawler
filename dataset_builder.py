#!/usr/bin/env python
""" DatasetBuilder: aggregate utilities to build large images datasets"""

from __future__ import print_function
import os
from shutil import copy2
from scipy import ndimage, misc
import numpy as np

__author__ = "Amine BENDAHMANE (@AmineHorseman)"
__email__ = "bendahmane.amine@gmail.com"
__license__ = "GPL"
__date__ = "May 6nd, 2016"

class DatasetBuilder(object):
    """ Aggregate utilities to build large datasets (renaming files, spliting categories,
        creating labels, loading data...) """

    merge_files_counter = 1
    rename_files_counter = 1
    data = []
    labels = []

    def __init__(self):
        print("\nPreparing DatasetBuilder...")

    @staticmethod
    def check_folder_existance(folderpath, throw_error_if_no_folder=False, display_msg=True):
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
                os.makedirs(folderpath)
                if display_msg:
                    print("Target folder '", folderpath, "' does not exist...")
                    print(" >> Folder created")

    @classmethod
    def rename_files(cls, source_folder, target_folder, extensions=('.jpg', '.jpeg', '.png')):
        """ list subfolders recursively and rename files according to
            the following the pattern: 1.jpg, 2.jpg..."""
        # check source_folder and target_folder:
        cls.check_folder_existance(source_folder, throw_error_if_no_folder=True)
        cls.check_folder_existance(target_folder, display_msg=False)
        if source_folder[-1] == "/":
            source_folder = source_folder[:-1]
        if target_folder[-1] == "/":
            target_folder = target_folder[:-1]

        # copy files and rename:
        print("Renaming files '", source_folder, "' files...")
        cls.rename_files_counter = 1
        for filename in os.listdir(source_folder):
            if os.path.isdir(source_folder + '/' + filename):
                cls.rename_files(source_folder + '/' + filename,
                                 target_folder + '/' + filename,
                                 extensions=extensions)
            else:
                if extensions == '' and os.path.splitext(filename)[1] == '':
                    copy2(source_folder + "/" + filename,
                          target_folder + "/" + str(cls.rename_files_counter))
                    cls.rename_files_counter += 1
                else:
                    for extension in extensions:
                        if filename.endswith(extension):
                            copy2(source_folder + "/" + filename,
                                  target_folder + "/" + str(cls.rename_files_counter) + extension)
                            cls.rename_files_counter += 1

    @classmethod
    def reshape_images(cls, source_folder, target_folder, height=128, width=128,
                       extensions=('.jpg', '.jpeg', '.png')):
        """ copy images and reshape them"""

        # check source_folder and target_folder:
        cls.check_folder_existance(source_folder, throw_error_if_no_folder=True)
        cls.check_folder_existance(target_folder, display_msg=False)
        if source_folder[-1] == "/":
            source_folder = source_folder[:-1]
        if target_folder[-1] == "/":
            target_folder = target_folder[:-1]

        # read images and reshape:
        print("Resizing '", source_folder, "' images...")
        for filename in os.listdir(source_folder):
            if os.path.isdir(source_folder + '/' + filename):
                cls.reshape_images(source_folder + '/' + filename,
                                   target_folder + '/' + filename,
                                   height, width, extensions=extensions)
            else:
                if extensions == '' and os.path.splitext(filename)[1] == '':
                    copy2(source_folder + "/" + filename,
                          target_folder + "/" + filename)
                    image = ndimage.imread(target_folder + "/" + filename, mode="RGB")
                    image_resized = misc.imresize(image, (height, width))
                    misc.imsave(target_folder + "/" + filename, image_resized)
                else:
                    for extension in extensions:
                        if filename.endswith(extension):
                            copy2(source_folder + "/" + filename,
                                  target_folder + "/" + filename)
                            image = ndimage.imread(target_folder + "/" + filename, mode="RGB")
                            image_resized = misc.imresize(image, (height, width))
                            misc.imsave(target_folder + "/" + filename, image_resized)
        
    @classmethod                       
    def crop_images(cls, source_folder, target_folder, height=128, width=128,
                       extensions=('.jpg', '.jpeg', '.png')):
        """ copy images and center crop them"""

        # check source_folder and target_folder:
        cls.check_folder_existance(source_folder, throw_error_if_no_folder=True)
        cls.check_folder_existance(target_folder, display_msg=False)
        if source_folder[-1] == "/":
            source_folder = source_folder[:-1]
        if target_folder[-1] == "/":
            target_folder = target_folder[:-1]

        # read images and crop:
        print("Cropping '", source_folder, "' images...")
        for filename in os.listdir(source_folder):
            if os.path.isdir(source_folder + '/' + filename):
                cls.crop_images(source_folder + '/' + filename,
                                   target_folder + '/' + filename,
                                   height, width, extensions=extensions)
            else:
                if extensions == '' and os.path.splitext(filename)[1] == '':
                    copy2(source_folder + "/" + filename,
                          target_folder + "/" + filename)
                    image = ndimage.imread(target_folder + "/" + filename, mode="RGB")
                    [width_original, height_original, _] = image.shape
                    offset_w = (width_original - width) / 2
                    offset_h = (width_original - width) / 2
                    image_cropped = image[offset_w : width + offset_w, offset_h : height + offset_h, :]
                    misc.imsave(target_folder + "/" + filename, image_cropped)
                else:
                    for extension in extensions:
                        if filename.endswith(extension):
                            copy2(source_folder + "/" + filename,
                                  target_folder + "/" + filename)
                            image = ndimage.imread(target_folder + "/" + filename, mode="RGB")
                            [width_original, height_original, _] = image.shape
                            offset_w = (width_original - width) / 2
                            offset_h = (width_original - width) / 2
                            image_cropped = image[offset_w : width + offset_w, offset_h : height + offset_h, :]
                            misc.imsave(target_folder + "/" + filename, image_cropped)

    @classmethod
    def merge_folders(cls, source_folder, target_folder,
                      extensions=('.jpg', '.jpeg', '.png')):
        """ merge images in separated folders in one single folder
            The images will be renamed"""

        # check source_folder and target_folder:
        cls.check_folder_existance(source_folder, throw_error_if_no_folder=True)
        cls.check_folder_existance(target_folder, display_msg=False)
        if source_folder[-1] == "/":
            source_folder = source_folder[:-1]
        if target_folder[-1] == "/":
            target_folder = target_folder[:-1]

        # copy files and rename:
        print("Merging '", source_folder, "' files...")
        for filename in os.listdir(source_folder):
            if os.path.isdir(source_folder + '/' + filename):
                cls.merge_folders(source_folder + '/' + filename,
                                  target_folder, extensions=extensions)
            else:
                if extensions == '' and os.path.splitext(filename)[1] == '':
                    copy2(source_folder + "/" + filename,
                          target_folder + "/" + str(cls.merge_files_counter))
                    cls.merge_files_counter += 1
                else:
                    for extension in extensions:
                        if filename.endswith(extension):
                            copy2(source_folder + "/" + filename,
                                  target_folder + "/" + str(cls.merge_files_counter) + extension)
                            cls.merge_files_counter += 1

    @classmethod
    def convert_to_grayscale(cls, source_folder, target_folder,
                             extensions=('.jpg', '.jpeg', '.png')):
        """ convert images from RGB to Grayscale"""

        # check source_folder and target_folder:
        cls.check_folder_existance(source_folder, throw_error_if_no_folder=True)
        cls.check_folder_existance(target_folder, display_msg=False)
        if source_folder[-1] == "/":
            source_folder = source_folder[:-1]
        if target_folder[-1] == "/":
            target_folder = target_folder[:-1]

        # read images and reshape:
        print("Convert '", source_folder, "' images to grayscale...")
        for filename in os.listdir(source_folder):
            if os.path.isdir(source_folder + '/' + filename):
                cls.convert_to_grayscale(source_folder + '/' + filename,
                                         target_folder + '/' + filename,
                                         extensions=extensions)
            else:
                if extensions == '' and os.path.splitext(filename)[1] == '':
                    copy2(source_folder + "/" + filename,
                          target_folder + "/" + filename)
                    image = ndimage.imread(target_folder + "/" + filename, flatten=True)
                    misc.imsave(target_folder + "/" + filename, image)
                else:
                    for extension in extensions:
                        if filename.endswith(extension):
                            copy2(source_folder + "/" + filename,
                                  target_folder + "/" + filename)
                            image = ndimage.imread(target_folder + "/" + filename, flatten=True)
                            misc.imsave(target_folder + "/" + filename, image)

    @classmethod
    def convert_format(cls, source_folder, target_folder,
                       extensions=('.jpg', '.jpeg', '.png'), new_extension='.jpg'):
        """ change images from one format to another (eg. change png files to jpeg) """

        # check source_folder and target_folder:
        cls.check_folder_existance(source_folder, throw_error_if_no_folder=True)
        cls.check_folder_existance(target_folder, display_msg=False)
        if source_folder[-1] == "/":
            source_folder = source_folder[:-1]
        if target_folder[-1] == "/":
            target_folder = target_folder[:-1]

        # read images and reshape:
        print("Change format of '", source_folder, "' files...")
        for filename in os.listdir(source_folder):
            if os.path.isdir(source_folder + '/' + filename):
                cls.convert_format(source_folder + '/' + filename,
                                   target_folder + '/' + filename,
                                   extensions=extensions, new_extension=new_extension)
            else:
                if extensions == '' and os.path.splitext(filename)[1] == '':
                    copy2(source_folder + "/" + filename,
                          target_folder + "/" + filename + new_extension)
                    image = ndimage.imread(target_folder + "/" + filename + new_extension)
                    misc.imsave(target_folder + "/" + filename + new_extension, image)
                else:
                    for extension in extensions:
                        if filename.endswith(extension):
                            new_filename = os.path.splitext(filename)[0] + new_extension
                            copy2(source_folder + "/" + filename,
                                  target_folder + "/" + new_filename)
                            image = ndimage.imread(target_folder + "/" + new_filename)
                            misc.imsave(target_folder + "/" + new_filename, image)

    @classmethod
    def convert_to_array(cls, source_folder, target_folder, create_labels_file=False,
                       flatten=False, extensions=('.jpg', '.jpeg', '.png')):
        """ Read all images in subfolders and convert them to a single array """

        # check source_folder and target_folder:
        cls.check_folder_existance(source_folder, throw_error_if_no_folder=True)
        cls.check_folder_existance(target_folder, display_msg=False)
        if source_folder[-1] == "/":
            source_folder = source_folder[:-1]
        if target_folder[-1] == "/":
            target_folder = target_folder[:-1]

        # read images and concatenate:
        print("Converting '", source_folder, "' images...")
        for filename in os.listdir(source_folder):
            if os.path.isdir(source_folder + '/' + filename):
                cls.convert_to_array(source_folder + '/' + filename, target_folder, 
                    create_labels_file=create_labels_file, extensions=extensions)
            else:
                if extensions == '' and os.path.splitext(filename)[1] == '':
                    image = ndimage.imread(source_folder + "/" + filename, mode="RGB")
                    if (flatten):
                        cls.data.append(image.flatten())
                    else:
                        cls.data.append(image)
                    if create_labels_file:
                        cls.labels.append(source_folder.replace('/', '_'))
                else:
                    for extension in extensions:
                        if filename.endswith(extension):
                            image = ndimage.imread(source_folder + "/" + filename, mode="RGB")
                            if (flatten):
                                cls.data.append(image.flatten())
                            else:
                                cls.data.append(image)
                            if create_labels_file:
                                cls.labels.append(source_folder.replace('/', '_'))

    @classmethod
    def convert_to_single_file(cls, source_folder, target_folder, create_labels_file=False,
                       flatten=False, extensions=('.jpg', '.jpeg', '.png')):
        """ Convert dataset images to a single file (array of images)
            The algorithm generates labels automatically according to subfolders"""

        # convert files in source_folder to data array and labels array:
        print("Converting images to single file...")
        cls.data = []
        cls.labels = []
        cls.convert_to_array(source_folder, target_folder, create_labels_file=create_labels_file, 
            flatten=flatten, extensions=extensions)

        # convert string labels to numeric type:
        if create_labels_file:
            print("Converting Labels to numeric type...")
            keys = list(set(cls.labels)) # unique list of labels
            numeric_labels = dict(zip(keys, range(len(keys))))
            for i in xrange(len(cls.labels)):
                cls.labels[i] = numeric_labels[cls.labels[i]]

        # save files:
        print(" Saving...")
        np.save(target_folder + '/data.npy', cls.data)
        print(" > Images saved to: ", target_folder + '/data.npy')
        if create_labels_file:
            np.save(target_folder + '/labels.npy', cls.labels)
            print(" > Labels saved to: ", target_folder + '/labels.npy')

