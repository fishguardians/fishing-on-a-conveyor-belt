#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''_3_fish_measure_dimensions.py: Measures the fish in image based on a reference object
    @Author: "Nicholas Bingei"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''

# import if necessary (built-in, third-party, path, own modules)

from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2

from constant import ref_width

"""
Step 3 for fish length image processing
Measures the fish in the image against the reference point.
Uses the black dot stickers at a reference point
Black dot stickers are 19mm or 1.9cm
Reference length can be modified in constant.py
"""


def get_dimensions(removeBg_output_img: object, og_img: object) -> object:
    ref_measured = False
    fishID_measured = False

    image = cv2.resize(removeBg_output_img, None, fx=0.4, fy=0.4)
    # image = removeBg_output_img  # Image for processing

    """
    # # its is already in greyscale for the process before
    # # blur it slightly
    # gray = cv2.GaussianBlur(image, (7, 7), 0)
    # 
    # # For getting thresholds for Canny using the adjustable slides
    # # t1, t2 = tuneCanny(gray) # Demonstration
    # # print(f"Threshold1: {t1}, Threshold2: {t2}")
    # t1, t2 = 10, 10  # For default threshold
    # 
    # # Performs edge detection, then perform a dilation + erosion to
    # # Closes gaps in between object edges
    # edged = cv2.Canny(gray, t1, t2)
    # 
    # # Dilation increases the boundaries of regions of foreground pixels.
    # # Areas of foreground pixels expand in size while holes within those regions become smaller.
    # 
    # kernel = np.ones((4, 4), 'uint8')  # 4 is the minimum before it there will be broken contours
    # dilate = cv2.dilate(edged, kernel, iterations=1)
    # erode_dilate = cv2.erode(dilate, None, iterations=1)
    """

    # find contours in the edge map
    cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    print("Total number of contours are: ", len(cnts))

    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    pixelPerMetric = None

    # loop over the contours individually
    count = 0

    # initialize array of length for objects
    list_of_objects_length = list()

    for c in cnts:

        # Get the contour area of the current object measured
        area = cv2.contourArea(c)
        print('objects contour area: ', area)

        # Contour area of the reference dot
        # Anything smaller will be ignored for measurement
        if cv2.contourArea(c) < 500:
            count += 1
            continue

        # Count number of contours found to
        count += 1

        # compute the rotated bounding box of the contour
        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding box
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)

        # Source video frame to layover the dimensions
        orig = og_img
        # orig = cv2.resize(og_img, None, fx=0.4, fy=0.4)
        # cv2.imshow('orig', orig)

        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
        # cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)qq

        # loop over the original points and draw them
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        # unpack the ordered bounding box, then compute the midpoint
        # between the top-left and top-right coordinates, followed by
        # the midpoint between bottom-left and bottom-right coordinates
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

        # compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-right and bottom-right
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        # draw circles for the points
        cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

        # draw lines between the midpoints
        cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
        cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)

        # compute the Euclidean distance between the midpoints
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        # if the pixels per metric has not been initialized, then
        # compute it as the ratio of pixels to supplied metric
        # in this case, inches, hence since input is in centimeters
        # it will be divided by 2.54 to convert cm to inches
        if pixelPerMetric is None:
            pixelPerMetric = dB / (ref_width / 2.54)

        # compute the size of the object
        dimA = dA / pixelPerMetric  # Length
        dimB = dB / pixelPerMetric  # Depth

        # Converts inch to centimeters
        def inch_to_cm(inch):
            return inch * 2.54

        dimA_CM = inch_to_cm(dimA)  # Length of object
        dimB_CM = inch_to_cm(dimB)  # Depth/Width of object

        # Adds the length and depth of the objects onto the source video image frame
        cv2.putText(orig, "{:.2f}cm".format(dimA_CM), (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2)
        cv2.putText(orig, "{:.2f}cm".format(dimB_CM), (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                    (255, 255, 255), 2)

        # Output length and depth in 3 decimal places
        length = round(dimA_CM, 3)
        depth = round(dimB_CM, 3)

        # Shows the source image with bounding boxes with dimensions overlay
        # cv2.imshow("Fish Dimensions", orig)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # append object's length to the list
        list_of_objects_length.append(dimA_CM)
        print("")
        print('list_of_objects_length: ', list_of_objects_length)
        print('Current count: ', count)

        if count == len(cnts):
            print('lenght of object: ', length)
            print('width of object: ', depth)
            print('_________________________________________________________________________')

            # Sort lengths by largest to smallest. Largest should always be a fish.
            list_of_objects_length.sort(reverse=True)
            return length, depth

# Returns the midpoint of 2 points
def midpoint(ptA, ptB):
    return (ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5


"""
        # Length buffers for error control
        ref_length_buffer_high = ref_width + (ref_width * 0.05)
        ref_depth_buffer_high = ref_width + (ref_width * 0.05)
        ref_length_buffer_low = ref_width - (ref_width * 0.05)
        ref_depth_buffer_low = ref_width - (ref_width * 0.05)

        # Contour checking starts from left to right
        # In this order, reference object, fish id tag and fish
        # Hence checks for reference object first

        # If object is smaller than the reference object by 5%, skip
        if ref_length_buffer_low > dimA_CM or ref_depth_buffer_low > dimB_CM:
            # print("")
            # print('contour area: ', area)
            # print("SKIPPED OBJECT SMALLER THAN REFERENCE")
            # print("Dimensions of Object",
            #       "------------",
            #       "Length: {:.3} cm".format(dimA_CM),
            #       "Depth: {:.3} cm".format(dimB_CM), sep='\n')
            print("Value of count:", count)

        # Detected another ref, reset pixel per metric formula
        elif ref_measured and ref_length_buffer_low < dimA_CM < ref_length_buffer_high and ref_depth_buffer_low \
                < dimB_CM < ref_depth_buffer_high:
            pixelPerMetric = dB / (ref_width / 2.54)
            # print("")
            # print("Another reference detected")
            # print('contour area: ', area)
            # print("Dimensions of Reference",
            #       "------------",
            #       "Length: {:.3f} cm".format(dimA_CM),
            #       "Depth: {:.3f} cm".format(dimB_CM), sep='\n')
            print("Value of count:", count)

        # Once suitable reference is found, it will start measurement process
        elif dimA_CM < ref_length_buffer_high and dimB_CM < ref_depth_buffer_high:
            ref_measured = True
            # print("")
            # print('contour area: ', area)
            # print("Dimensions of Reference",
            #       "------------",
            #       "Length: {:.3f} cm".format(dimA_CM),
            #       "Depth: {:.3f} cm".format(dimB_CM), sep='\n')
            print("Value of count:", count)

        # Measure the Fish ID tag after ref has been measured
        elif ref_measured and not fishID_measured and dimA_CM > ref_length_buffer_high:
            fishID_measured = True
            # print("")
            # print('contour area: ', area)
            # print("Dimensions of Fish ID tag",
            #       "------------",
            #       "Length: {:.3f} cm".format(dimA_CM),
            #       "Depth: {:.3f} cm".format(dimB_CM), sep='\n')
            print("Value of count:", count)

        # Measure the fish, once there are at least 2 counts
        # And both the ref and fishID have been measured
        elif ref_measured and fishID_measured and count > 2:
            # print("")
            # print('contour area: ', area)
            # print("Dimensions of Fish",
            #       "------------",
            #       "Length: {:.3f} cm".format(dimA_CM),
            #       "Depth: {:.3f} cm".format(dimB_CM), sep='\n')
            # print("Total contours processed: ", count)
            return length, depth
"""


