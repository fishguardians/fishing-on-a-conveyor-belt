#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''constant.py: Stores the constant values of the project'''
# import if necessary (built-in, third-party, path, own modules)

videos_location = './videos/'
image_storage = './images/'
data_output = './output/'

fish_color = (238, 238, 175)
id_color = (0, 255, 0)
scale_color = (255, 255, 255)
belt_color = (0, 255, 0)

tess_blacklist = ''
tess_whitelist = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcefghijklmnopqrstuvwxyz'

# Fish Dimension Module Constants
ref_width = 1.9  # Width of black circle reference dot

# class FishImage:
#     name = ''
#     path = None
#
#     def __init__(self, name):
#         self.name = name
#         self.img = cv2.imread(name)
#         self.org = None  # Original image. For testing. Can be removed to save memory.
#         self.id = ''
#         self.weight = ''
#         self.length = ''
#         self.depth = ''
