#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''_1_fish_crop_belt_image.py: Processes video frames and crops out the non-conveyor belt parts of the image.
    @Author: "Nicholas Bingei"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''

# import if necessary (built-in, third-party, path, own modules)

import numpy as np
import cv2
import os
import constant
import glob
import sys
from pathlib import Path

"""
Step 1 for fish length image processing
Imports and processes the raw fish images 
and crops out the non-conveyor belt parts of the image. 
Leaving only the yellow conveyor belt parts of the image
that contains the fish itself and its ID tag
and the reference object (the 19mm black sticker).
"""


def crop_belt(image):
    # Threshold on yellow
    lower = (0, 120, 120)
    upper = (100, 255, 255)
    thresh = cv2.inRange(image, lower, upper)

    # Apply dilate morphology
    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

    # Get largest contour
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    big_contour = max(contours, key=cv2.contourArea)

    # These values can be used to either draw a rectangle or crop out the image part using pixel coordinates.
    # X coordinate, Y coordinate, Width, Height
    x, y, width, height = cv2.boundingRect(big_contour)

    # Original image's height and width
    og_height = np.size(image, 0)
    og_width = np.size(image, 1)

    # Add black border to belt center to cover background leftovers
    # For any offset if the belt is film tilted or slightly diagonal
    # cv2.rectangle(Parameters: image, start_point, end_point, color, thickness)
    # Add black border in the left of belt (5% width of the belt area)
    add_border_l = cv2.rectangle(image, (x, y), (int(x + width * 0.05), y + height), (0, 0, 0), -1)
    end_x = int(x + width)
    start_x = int(end_x - width * 0.08)  # Change based on percentage 5% or more
    add_border_r = cv2.rectangle(add_border_l, (start_x, y), (end_x, y + height), (0, 0, 0), -1)
    # Fill left side of belt background with colour black
    colored_left = cv2.rectangle(add_border_r, (0, 0), (0 + x, y + height), (0, 0, 0), -1)
    # Fill right side of belt background with colour black
    colored_right = cv2.rectangle(colored_left, ((x + width), 0), (og_width, og_height), (0, 0, 0), -1)
    # Write the final output image into image
    cropBelt_output_img = colored_right

    # # Display the output result
    # cv2.imshow("Remove Background Result", image.img)
    # cv2.waitKey(0) # For Debug
    # cv2.destroyAllWindows() # For Debug

    return cropBelt_output_img
