#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''_2_fish_remove_background.py: Removes conveyor belt colour and water reflections on belt
    @Author: "Nicholas Bingei"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''

# import if necessary (built-in, third-party, path, own modules)
import statistics

import cv2
import imutils
import numpy as np
from cv2 import mean

"""
Step 2 for fish length image processing

# Mask inversion on a RGB image.
# Removes yellow conveyor belt background
# Removes water reflections on the belt, 
# that affects the contour processing
"""

def remove_background(cropBelt_output_img):

    image = cropBelt_output_img.copy()

    # Defining the lower and upper values of HSV
    # this will detect yellow colour of the belt
    # and threshold based on the species of fish on the conveyor belt
    # print('fish_species',fish_species)

    # if fish_species == 'Baby Red Snapper':
    #     # print('Baby Red Snapper')
    #     Lower_hsv = np.array([20, 170, 100])
    #     Upper_hsv = np.array([30, 255, 255])
    # else:
        # print('Default')
    Lower_hsv = np.array([20, 70, 100])
    Upper_hsv = np.array([30, 255, 255])

    # creating the mask
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask_yellow_belt = cv2.inRange(hsv_img, Lower_hsv, Upper_hsv)

    # Inverting the mask (Changes the yellow belt and changes it to black pixels)
    inverted_mask = cv2.bitwise_not(mask_yellow_belt)
    mask_output = cv2.bitwise_and(image, image, mask=inverted_mask)

    # Change images to grayscale
    gray = cv2.cvtColor(mask_output, cv2.COLOR_BGR2GRAY)

    # Apply blur to image
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    # For getting thresholds for Canny using the adjustable sliders
    # t1, t2 = tuneCanny(gray) # Demonstration
    # print(f"Threshold1: {t1}, Threshold2: {t2}")
    t1, t2 = 10, 10  # For default threshold

    # Perform edge detection to show edges in the image based on the image and its 2 threshold variables
    edged = cv2.Canny(blur, t1, t2)

    # Dilation increases the boundaries of regions of foreground pixels.
    # Areas of foreground pixels expand in size while holes within those regions become smaller.
    kernel = np.ones((2, 2), 'uint8')
    erode_dilate = cv2.dilate(edged, kernel, iterations=1)
    # cv2.imshow('erode_dilate.png', erode_dilate)

    # Fill in the closed contours. Mainly for reference dots, id tag and fish
    cnts = cv2.findContours(erode_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        cv2.drawContours(erode_dilate, [c], 0, (255,255,255), -1)
    # cv2.imshow('filling_contours.png', erode_dilate)

    # Remove leftover contours from water reflections
    cleaned_image = erode_dilate.copy()
    cnts = cv2.findContours(cleaned_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    rect_areas = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        rect_areas.append(w * h)
    avg_area = statistics.mean(rect_areas)
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cnt_area = w * h
        # Removes contours smaller than the reference dot
        if cnt_area < 0.2 * avg_area:
            cleaned_image[y:y + h, x:x + w] = 0
    # cv2.imshow('cleanup.png', erode_dilate)

    # find contours in the edge map
    cnts = cv2.findContours(cleaned_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[0])

    bbox_image = image.copy()
    # Draw bounding boxes for contours
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if h > 50 and w > 50: # Only contours as large as than the reference should be returned as ROI
            roi = bbox_image[y:y + h, x:x + w]
            # cv2.imshow('regions_of_interest.png', roi) # Shows the fish
            cv2.rectangle(bbox_image, (x,y), (x+w, y+h), (36, 255, 12), 2)

    combined_mask_output = cleaned_image
    # cv2.imshow('bounding_boxes.png', bbox_image)  # Bounding boxes on the original image
    # cv2.imshow('combined_mask_output.png', combined_mask_output)
    return combined_mask_output


# Function is needed for the createTrackbar step downstream
def nothing(x):
    pass

"""
Creates a window with sliders to adjust canny in the image
For specific tuning for new fish types
Currently only used for snapper testing
"""
def tuneCanny(image):
    window = 'canny'
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.createTrackbar('threshold1', window, 10, 500, nothing)
    cv2.createTrackbar('threshold2', window, 10, 500, nothing)

    while True:
        image_copy = np.copy(image)
        threshold1 = cv2.getTrackbarPos('threshold1', window)
        threshold2 = cv2.getTrackbarPos('threshold2', window)

        # Displays the image based on the new and adjusted threshold values
        edged = cv2.Canny(image_copy, threshold1, threshold2)
        cv2.imshow('edged', edged)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    return threshold1, threshold2


