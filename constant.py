#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''constant.py: Stores the constant values of the project'''
#import if necessary (built-in, third-party, path, own modules)

import cv2

videos_location = './videos/'
image_storage = './images/'
data_output = './output/'

# (height, width, channel)
frame_dimension = (540,480,3)

class FishImage:
    name = ''
    path = None

    def __init__(self, name):
        self.name = name
        self.img = cv2.imread(name)
        self.org = None # Original image. For testing. Can be removed to save memory.
        self.id = ''
        self.weight = ''
        self.length = ''
        self.depth = ''

# Width of paperID reference in centimeters
ref_width = 1.2
