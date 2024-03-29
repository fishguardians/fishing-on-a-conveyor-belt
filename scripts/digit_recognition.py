#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''digit_recognition.py: Retrieves the weighting scale reading from a given frame
    @Author: "Chen Dong, Yao Yujing"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
    
import cv2
import numpy as np
import imutils

DIGITSDICT = {
    (1, 1, 1, 1, 1, 1, 0): 0,
    (0, 1, 1, 0, 0, 0, 0): 1,
    (1, 1, 0, 1, 1, 0, 1): 2,
    (1, 1, 1, 1, 0, 0, 1): 3,
    (0, 1, 1, 0, 0, 1, 1): 4,
    (1, 0, 1, 1, 0, 1, 1): 5,
    (1, 0, 1, 1, 1, 1, 1): 6,
    (1, 1, 1, 0, 0, 0, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9,
}

def digit_recognition(image,angle=5.0):
    #function call that gets the image with the right roi
    roi_color = get_roi(image)
    roi_grey = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY) #greyscale image 
    roi_color = cv2.rotate(roi_color,cv2.ROTATE_90_COUNTERCLOCKWISE) #change orientation
    roi = cv2.resize(roi_grey, None,None,fx=1.0,fy=1.0) #resize image
    roi= imutils.rotate(roi, angle)
    
    roi = cv2.bilateralFilter(roi, 5, 30, 60) #reduce noise
    #roi.shape[0] = height, roi.shape[1] = width
    RATIO = roi.shape[0] * 0.01
    #trim image, in sequence of y1:y2, x1:x2
    trimmed = roi[int(RATIO)+2 :, int(RATIO) : roi.shape[1] - int(RATIO)-10]
    
    edged = cv2.adaptiveThreshold(  
        trimmed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5
    )
    
    #-----------------enhance image------------------------------------
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 5))
    dilated = cv2.dilate(edged, kernel, iterations=1)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
    dilated = cv2.dilate(dilated, kernel, iterations=1)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 1),)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    #------------------------------------------------------------------
    h = roi.shape[0] 
    ratio = int(h * 0.01) 
    eroded[-ratio:,] = 0 
    eroded[:, :ratio] = 0

    cnts, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    digits_cnts = []

    canvas = trimmed.copy()
    cv2.drawContours(canvas, cnts, -1, (255, 255, 255), 1)

    #detect & draw contours in random sequence
    for cnt in cnts:
        #compute bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(cnt)
        if h > 50: #determine if the item should be read (by height)
            digits_cnts.append(cnt) #determine how many digits are there
            #draw bounding box
            cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 0), 1)
            cv2.drawContours(canvas, cnt, 0, (255, 255, 255), 1)

    # print(f"No. of Digit Contours: {len(digits_cnts)}")

    #sort by the value of the x coordinates of the countour
    sorted_digits = sorted(digits_cnts, key=lambda cnt: cv2.boundingRect(cnt)[0])

    canvas = trimmed.copy()
    #draw contours in sorted sequence
    for i, cnt in enumerate(sorted_digits):
        (x, y, w, h) = cv2.boundingRect(cnt)
        #check if the width of the bounding box is too small.
        #solve the issue for digit '1'
        if w < 24:
            x-=21
            w = 32
        else:
            pass
        cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 0), 1)
        cv2.putText(canvas, str(i), (x, y - 3), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)

    digits = []
    canvas = trimmed.copy()

    #loop over each of the digit
    for cnt in sorted_digits:
        # extract the digit ROI
        #x coordinate, y coordinate, width, height
        (x, y, w, h) = cv2.boundingRect(cnt)
        #check if the width is too small.
        if w < 24:
            x-=21
            w = 32
        else:
            pass
        #y1,y2,x1,x2
        roi = eroded[y : y + h, x : x + w]
        qW, qH = int(w * 0.25), int(h * 0.15)
        fractionH, halfH, fractionW = int(h * 0.05), int(h * 0.5), int(w * 0.25)

        # seven segments in the order of wikipedia's illustration
        sevensegs = [
            ((0, 0), (w, qH)),  # a (top bar)
            ((w - qW, 0), (w, halfH)),  # b (upper right)
            ((w - qW, halfH), (w, h)),  # c (lower right)
            ((0, h - qH), (w, h)),  # d (lower bar)
            ((0, halfH), (qW, h)),  # e (lower left)
            ((0, 0), (qW, halfH)),  # f (upper left)
            # ((0, halfH - fractionH), (w, halfH + fractionH)) # center
            (
                (0 + fractionW, halfH - fractionH),
                (w - fractionW, halfH + fractionH),
            ),  # center / g 
        ]

        # initialize to off
        on = [0] * 7
        try:
            for (i, ((p1x, p1y), (p2x, p2y))) in enumerate(sevensegs):
                region = roi[p1y:p2y, p1x:p2x]
                #detect seven segments and store inside the array
                if np.sum(region == 255) > region.size * 0.5:
                    on[i] = 1
                

            digit = DIGITSDICT[tuple(on)]
            digits += [digit]
            cv2.rectangle(canvas, (x, y), (x + w, y + h), (255, 255, 0), 1)
            cv2.putText(canvas, str(digit), (x - 5, y + 6), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)
        except:
            pass
    if(len(digits)==4):
        digit = ''.join(map(str, digits[1:]))
        digit = str(digits[0])+"."+digit
        return digit
    else:
        angle+=0.5
        if(angle<=12):
            digit_recognition(image,angle)
        return "N.A"

def get_roi(image):
    img_color = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE) #change orientation
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY) #grey scale image
    blurred = cv2.GaussianBlur(img, (7, 7), 0) #reduce noise
    blurred = cv2.bilateralFilter(blurred, 6, sigmaColor=50, sigmaSpace=50) #reduce noise 
    edged = cv2.Canny(blurred, 30, 50, 255) #get the edge 

    #array that contain all the contours in the image
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # sort contours by area, and get the largest
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    cv2.drawContours(edged, contours, 0, (255,0,0), 5) 

    x_coor, y_coor, width, height = cv2.boundingRect(contours[0])  #return 4 points 
    roi = img[y_coor : y_coor + height, x_coor : x_coor + width] #crop image (roi)
    roi = cv2.cvtColor(roi, cv2.COLOR_GRAY2RGB) #greyscale image 
    return roi


