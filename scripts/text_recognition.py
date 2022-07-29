#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''text_recognition.py: Module that reads the fish id using the given image
    @Author: "Muhammad Abdurraheem, Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
    
from pytesseract import pytesseract
import cv2
import numpy as np
import os
import constant

def text_recognition(image, user_ocr_whitelist):
    # Get the text from the fish id image

    # Super resolution for image
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    path = "dnn_model/LapSRN_x8.pb"
    sr.readModel(path)
    sr.setModel("lapsrn",8)
    image = sr.upsample(image)

    #increase size to read image better
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert from GBR to RGB
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # change orientation
    
    image = cv2.bilateralFilter(image, 5, 30, 60)
    # edged = cv2.Canny(id_image, 30, 200)
    # thresholding = cv2.threshold(id_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.threshold(cv2.medianBlur(image, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("test", opening)

    print('user_ocr_whitelist in text_recognition ', user_ocr_whitelist)
    
    text = pytesseract.image_to_string(image, \
                                        config='-l eng --psm 3 --oem 3 -c tessedit_char_whitelist="' + str(user_ocr_whitelist) + '" tessedit_char_blacklist="' + constant.tess_blacklist + '"')
                                        
    words = ''.join(char for char in text if char.isalnum())
    return words

# Test for best accuracy
# for images in os.listdir('../images/20june_fishyy.mp4/id/'):
#     if(images != '.DS_Store'):
#         print(images)
#         print(text_recognition(cv2.imread('../images/20june_fishyy.mp4/id/' + images)))
