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

    image = removeBg_output_img  # Image for processing

    # its is already in greyscale for the process before
    # blur it slightly
    gray = cv2.GaussianBlur(image, (7, 7), 0)

    # For getting thresholds for Canny using the adjustable slides
    # t1, t2 = tuneCanny(gray) # Demonstration
    # print(f"Threshold1: {t1}, Threshold2: {t2}")
    t1, t2 = 10, 10  # For default threshold

    # Performs edge detection, then perform a dilation + erosion to
    # Closes gaps in between object edges
    edged = cv2.Canny(gray, t1, t2)

    # Dilation increases the boundaries of regions of foreground pixels.
    # Areas of foreground pixels expand in size while holes within those regions become smaller.

    kernel = np.ones((4, 4), 'uint8')  # 4 is the minimum before it there will be broken contours
    dilate = cv2.dilate(edged, kernel, iterations=1)
    erode_dilate = cv2.erode(dilate, None, iterations=1)

    # find contours in the edge map
    cnts = cv2.findContours(erode_dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # print("Total number of contours are: ", len(cnts))

    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    pixelPerMetric = None

    # loop over the contours individually
    count = 0
    flagged = False

    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 1000:
            continue
        count += 1

        # compute the rotated bounding box of the contour
        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding box
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)

        orig = og_img  # Source video frame to layover the dimensions
        orig = cv2.resize(og_img, None, fx=0.4, fy=0.4)

        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

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
            # pixelPerMetric = dB / (args["width"]/2.54)
            pixelPerMetric = dB / (ref_width / 2.54)

        # compute the size of the object
        dimA = dA / pixelPerMetric  # Length
        dimB = dB / pixelPerMetric  # Depth

        # Converts inch to centimeters
        def inch_to_cm(inch):
            return inch * 2.54

        dimA_CM = inch_to_cm(dimA)
        dimB_CM = inch_to_cm(dimB)

        # Adds the length and depth of the objects onto the source video image frame
        cv2.putText(orig, "{:.2f}cm".format(dimA_CM), (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2)
        cv2.putText(orig, "{:.2f}cm".format(dimB_CM), (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                    (255, 255, 255), 2)

        # Sends image with dimensions to another module
        sendDimensions(orig)

        d_length = dimA_CM
        d_depth = dimB_CM

        ref_length_buffer_high = ref_width + (ref_width * 0.05)
        ref_depth_buffer_high = ref_width + (ref_width * 0.05)

        ref_length_buffer_low = ref_width - (ref_width * 0.05)
        ref_depth_buffer_low = ref_width - (ref_width * 0.05)

        # Output length and depth in 2 decimal places
        # length = "{:.3f}cm".format(dimA_CM)
        # depth = "{:.3f}cm".format(dimB_CM)
        length = round(dimA_CM,3)
        depth = round(dimB_CM,3)

        # cv2.imwrite("gray.jpg", gray)
        # cv2.imwrite("erode_dilate.jpg", erode_dilate)
        # cv2.imwrite("Measured.jpg", orig)

        # cv2.imshow("gray", gray)
        # cv2.imshow("Erode and dilate", erode_dilate)
        # cv2.imshow("Fish Dimensions", orig)
        # cv2.waitKey(0)

        # TODO: ADD MORE SOPHISTICATED ERROR CHECKING
        # TODO: For tiny water blob reflections (If smaller than a certain threshold ignore)

        # Contour checking starts from the most left
        # In this order, reference object, fish id tag and fish
        # Hence checks for reference object first

        # If object is smaller than the reference object by 5%, skip
        if ref_length_buffer_low > d_length or ref_depth_buffer_low > d_depth:
            print("")
            # print("SKIPPED OBJECT SMALLER THAN REFERENCE")
            # print("Dimensions of Object",
            #       "------------",
            #       "Length: {:.3} cm".format(d_length),
            #       "Depth: {:.3} cm".format(d_depth), sep='\n')
            # print("Value of count:", count)

        # Detected another ref, reset pixel per metric formula
        elif ref_measured and ref_length_buffer_low < d_length < ref_length_buffer_high and ref_depth_buffer_low \
                < d_depth < ref_depth_buffer_high:
            pixelPerMetric = dB / (ref_width / 2.54)
            # print("")
            # print("Another reference detected")
            # print("Dimensions of Reference",
            #       "------------",
            #       "Length: {:.3f} cm".format(d_length),
            #       "Depth: {:.3f} cm".format(d_depth), sep='\n')
            # print("Value of count:", count)

        # Once suitable reference is found, it will start measurement process
        elif d_length < ref_length_buffer_high and d_depth < ref_depth_buffer_high:
            ref_measured = True
            # print("")
            # print("Dimensions of Reference",
            #       "------------",
            #       "Length: {:.3f} cm".format(d_length),
            #       "Depth: {:.3f} cm".format(d_depth), sep='\n')
            # print("Value of count:", count)

        # Measure the Fish ID tag after ref has been measured
        elif ref_measured and not fishID_measured and d_length > ref_length_buffer_high:
            fishID_measured = True
            # print("")
            # print("Dimensions of Fish ID tag",
            #       "------------",
            #       "Length: {:.3f} cm".format(d_length),
            #       "Depth: {:.3f} cm".format(d_depth), sep='\n')
            # print("Value of count:", count)

        # Measure the fish, once there are at least 2 counts
        # And both the ref and fishID have been measured
        elif ref_measured and fishID_measured and count > 2:
            # print("")
            # print("Dimensions of Fish",
            #       "------------",
            #       "Length: {:.3f} cm".format(d_length),
            #       "Depth: {:.3f} cm".format(d_depth), sep='\n')
            # print("Total contours processed: ", count)
            return length, depth


# Function is needed for the createTrackbar step downstream
def nothing(x):
    pass


# Returns the midpoint of 2 points
def midpoint(ptA, ptB):
    return (ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5


# Displays the title of the image display in the window
# def show_image(title, image, destroy_all=True):
#     cv2.imshow(title, image)
#     cv2.waitKey(0)
#     if destroy_all:
#         cv2.destroyAllWindows()


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

# Sends image with dimensions to another module
def sendDimensions(img):
    # print("sent Dimensions")
    return img

