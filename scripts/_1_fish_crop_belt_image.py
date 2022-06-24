#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''camera.py: Video capture module that takes the images of the fish
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
from constant import FishImage

"""
Step 1 for fish length image processing
Imports and processes the raw fish images 
and crops out the non-conveyor belt parts of the image. 
Leaving only the yellow conveyor belt parts of the image
that contains the fish itself and its ID.
"""

"""
For demonstration of code, search for 'Demonstration' and uncomment those lines
"""


# TODO: get the final output folder of the image capture script and put that below


def get_image_names():
    # creating list
    image_list = []

    # Process folder for image to be processed
    for file in glob.glob(constant.image_storage + "testing" + "/*.jpg"):
        # appending instances to list
        image_list.append(FishImage(file))

    return image_list


def remove_background(image_list):
    for image in image_list:
        # Store original image to image object
        image.org = (image.img).copy()

        # Threshold on yellow
        lower = (0, 120, 120)
        upper = (100, 255, 255)
        thresh = cv2.inRange(image.img, lower, upper)

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
        og_height = np.size(image.org, 0)
        og_width = np.size(image.org, 1)

        # Add black border to belt center to cover background leftovers
        # For any offset if the belt is film tilted or slightly diagonal
        # cv2.rectangle(Parameters: image, start_point, end_point, color, thickness)
        # Add black border in the left of belt (5% width of the belt area)
        add_border_l = cv2.rectangle(image.img, (x, y), (int(x + width * 0.05), y + height), (0, 0, 0), -1)
        # cv2.imshow("add_border_left", add_border_l) # For Debug
        # cv2.waitKey(0) # For Debug
        # cv2.destroyAllWindows() # For Debug

        end_x = int(x + width)
        start_x = int(end_x - width * 0.08) # Change based on percentage 5% or more

        add_border_r = cv2.rectangle(add_border_l, (start_x, y), (end_x, y + height), (0, 0, 0), -1)
        # cv2.imshow("add_border_right", add_border_r) # For Debug
        # cv2.waitKey(0) # For Debug
        # cv2.destroyAllWindows() # For Debug

        # Fill left side of belt background with colour black
        colored_left = cv2.rectangle(add_border_r, (0, 0), (0 + x, y + height), (0, 0, 0), -1)
        # cv2.imshow("colored_left", colored_left) # For Debug
        # cv2.waitKey(0) # For Debug
        # cv2.destroyAllWindows() # For Debug

        # Fill right side of belt background with colour black
        colored_right = cv2.rectangle(colored_left, ((x + width), 0), (og_width, og_height), (0, 0, 0), -1)
        # cv2.imshow("colored_right", colored_right) # For Debug
        # cv2.waitKey(0) # For Debug
        # cv2.destroyAllWindows() # For Debug

        # Write the final output image into image.img
        image.img = colored_right

        # # Display the output images
        # cv2.imshow("Remove Background Result", image.img) #Demonstration
        # cv2.waitKey(0) # For Debug
        # cv2.destroyAllWindows() # For Debug

        # Display in smaller window
        # cv2.namedWindow("Resize_test", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("Resize_test", 640, 360)
        # cv2.imshow("Window", image.img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    return image_list
