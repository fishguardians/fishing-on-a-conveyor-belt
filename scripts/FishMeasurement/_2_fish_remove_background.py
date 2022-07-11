#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''_2_fish_remove_background.py: Removes conveyor belt colour and water reflections on belt
    @Author: "Nicholas Bingei"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''

# import if necessary (built-in, third-party, path, own modules)

import cv2
import numpy as np

"""
Step 2 for fish length image processing

# Mask inversion on a RGB image.
# Removes yellow conveyor belt background
# Removes water reflections on the belt, 
# that affects the contour processing
"""


def remove_background(cropBelt_output_img):

    image = cropBelt_output_img

    # Removing the water reflections on the belt
    # of HSV, this will detect the water reflections of the belt
    GLARE_MIN = np.array([10, 30, 160], np.uint8)
    GLARE_MAX = np.array([40, 65, 250], np.uint8)
    # converting the image to HSV format
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # creating the mask
    mask_reflections = cv2.inRange(hsv_img, GLARE_MIN, GLARE_MAX)

    # Defining the lower and upper values
    # of HSV, this will detect yellow colour of the belt
    Lower_hsv = np.array([20, 70, 100])
    Upper_hsv = np.array([30, 255, 255])
    # creating the mask
    mask_yellow_belt = cv2.inRange(hsv_img, Lower_hsv, Upper_hsv)

    # Join the water reflection mask and yellow belt masks together
    combined_mask = mask_reflections | mask_yellow_belt
    # Inverting the mask (Changes the yellow belt and changes it to black pixels)
    inverted_mask = cv2.bitwise_not(combined_mask)
    combined_mask_output = cv2.bitwise_and(image, image, mask=inverted_mask)

    # Display Output
    # cv2.imshow("Reflections mask", mask_reflections)
    # cv2.imshow("Yellow mask", mask_yellow_belt)
    # cv2.imshow("Combined mask", combined_mask)
    # cv2.imshow("Removed background output", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return combined_mask_output


