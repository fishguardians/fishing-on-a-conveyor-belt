#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''text_recognition.py: Module that reads the fish id using the given image
    @Author: "Muhammad Abdurraheem, Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)
from pytesseract import pytesseract
import cv2
import numpy as np

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
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.threshold(cv2.medianBlur(image, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    text = pytesseract.image_to_string(image, \
                                        config='-l eng --psm 3 --oem 3 -c tessedit_char_whitelist="' + str(user_ocr_whitelist) + '"')
                                        
    words = ''.join(char for char in text if char.isalnum())
    return words
