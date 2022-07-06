#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''_fish_measurement.py: Starts the fish measur
    @Author: "Nicholas Bingei"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''

# import if necessary (built-in, third-party, path, own modules)

# Fish Dimension modules
import cv2
import \
    scripts.FishMeasurement._1_fish_crop_belt_image as cropBelt  # Blacks out all parts of the image apart from the belt
import \
    scripts.FishMeasurement._2_fish_remove_background as removeBg  # Removes the colour of the belt, leaving intented objects for measurement
import \
    scripts.FishMeasurement._3_fish_measure_dimensions as getDimensions  # Get dimensions of Fish based on length of reference object


def fish_measurement(image):
    fish_length, fish_depth = 0.0, 0.0
    og_img = image.copy()
    og_img = cv2.resize(og_img, None, fx=0.4, fy=0.4)

    # print('Running fish image processing functions')

    # 1. Run cropBelt function to black out all but the belt in the image
    cropBelt_output_img = cropBelt.crop_belt(image)
    # 2. Run removeBackground function to remove yellow belt colour and water reflections
    removeBg_output_img = removeBg.remove_background(cropBelt_output_img)
    # 3. Run getDimensions function to get measurements of fish (E.g. Barramundi and Snapper)

    flag = ""  # For flagging out errors during the processing
    try:
        fish_length, fish_depth = getDimensions.get_dimensions(removeBg_output_img,
                                                               og_img)
    except Exception as e:
        print(e)  # TypeError: cannot unpack non-iterable NoneType object
        flag = "ERROR! Please verify measurements for this fish"

    return fish_length, fish_depth, cropBelt_output_img, flag
