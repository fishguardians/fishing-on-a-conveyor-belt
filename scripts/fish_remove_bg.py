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


# TODO: get the final output folder of the image capture script and put that below


def get_image_names():
    # creating list
    imageList = []

    # Process folder for image to be processed
    for file in glob.glob(constant.image_storage + "testing" + "/*.jpg"):
        # appending instances to list
        imageList.append(FishImage(file))

    return imageList


def remove_background(image):

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

    # Crop image to specified area using slicing
    # Crop out only the yellow conveyor belt area
    image = image[y:y + height, x:x + width]
    return image
    """
    For testing.
    Code below can display output image and write image to filepath
    
    # Show the images (for testing)
    result = image.img
    # cv2.imshow("Background Removed", result)

    # Export the images
    # image_name = str(image.name)

    # Get the current working directory
    # cwd = 'r' + os.getcwd()
    # filepath = cwd + '/images/output/'
    # filepath2 = 'D:/Projects/fishguardians-ITP/images/output/'

    # print(filepath)
    # print(os.path.expanduser('~'))

    # if not cv2.imwrite(os.path.join(filepath2, '{}_bgr.png'.format(image_name)), result):
    #     raise Exception("Could not write image")

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    """



# For future reference if needed.
"""
# draw filled white contour on input
# result = img.copy()
# cv2.rectangle(result,(x,y),(x+width,y+height),(255,255,255),-1)
# cv2.imwrite('barramundi_bg_removed.png', result)
"""

"""
# For testing how to write to file path
# Code below can display output image and write image to filepath

# Show the images (for testing)
result = image.img
cv2.imshow("Background Removed", result)

# Export the images
image_name = str(image.name)

# Get the current working directory
cwd = 'r' + os.getcwd()
filepath = cwd + '/images/output/'
filepath2 = 'D:/Projects/fishguardians-ITP/images/output/'

print(filepath)
print(os.path.expanduser('~'))

if not cv2.imwrite(os.path.join(filepath2, '{}_bgr.png'.format(image_name)), result):
    raise Exception("Could not write image")

cv2.waitKey(0)
cv2.destroyAllWindows()
"""

"""
# For reference on how to get the sides of the background.
# Areas that are not belt
# Code below applies a colour overlay to section of image

# Add blue rectangle on conveyor belt area (MIDDLE. exactly within the belt)
# cv2.rectangle(Parameters: image, start_point, end_point, color, thickness)
uncropped_middle = cv2.rectangle(image.org, (x, y), (x + width, y + height), (255, 0, 0), -1)
cv2.imshow("uncropped_middle", uncropped_middle)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Add red rectangle on conveyor belt area (LEFT of belt)
uncropped_left = cv2.rectangle(image.org, (0, 0), (0 + x, y + height), (0, 0, 255), -1)
cv2.imshow("uncropped_left", uncropped_left)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Add green rectangle on conveyor belt area (RIGHT of belt)
uncropped_right = cv2.rectangle(image.org, ((x + width), 0), (og_width, og_height), (0, 255, 0), -1)
cv2.imshow("uncropped_right", uncropped_right)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
