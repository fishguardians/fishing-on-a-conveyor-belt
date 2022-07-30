#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''test_project.py: This is a unit test for the entire project module.
    Run python test_project.py to test all the given modules
    @Author: "Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
    
import cv2
import unittest
import numpy as np
import os
import pytesseract
if (os.name == 'nt'):
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe" 

import scripts.digit_recognition as dr
import scripts.generate_csv as gc
import scripts.FishMeasurement._1_fish_crop_belt_image as fm1
import scripts.FishMeasurement._2_fish_remove_background as fm2
import scripts.FishMeasurement._3_fish_measure_dimensions as fm3
import scripts.text_recognition as tr

class TestDigitRecognition(unittest.TestCase):
    def runTest(self):
        # Check if the region of interest of scale is retrieved into a numpy format
        test1 = dr.get_roi(cv2.imread('testing/3346.jpg'))
        self.assertEqual(isinstance(test1,np.ndarray), True, "get roi not numpy array format")
        # Check if value of image is 0.048
        test2 = dr.digit_recognition(cv2.imread('testing/3346.jpg'))
        self.assertEqual(test2, '0.078', "get digits error")

class TestFishMeasurement(unittest.TestCase):
    def runTest(self):
        # Check if the region of interest of conveyor belt is retrieved into a numpy format
        test1 = fm1.crop_belt(cv2.imread('testing/361.jpg'))
        self.assertEqual(isinstance(test1,np.ndarray), True, "crop belt not numpy array format")
        # Check if the remove baackground function returned a numpy format
        test2 = fm2.remove_background(test1)
        self.assertEqual(isinstance(test2,np.ndarray), True, "remove background not numpy array format")
        # Check if the length and depth is returned
        test3_length, test3_depth = fm3.get_dimensions(test2,cv2.imread('testing/361.jpg'))
        self.assertEqual(test3_length, 19.343, "get length error")
        self.assertEqual(test3_depth, 5.962, "get depth error")

class TestGenerateCSV(unittest.TestCase):
    def runTest(self):
        # Developers: Drag sample folder from testing to output folder before running
        # Return a output in results folder with a sample
        test1 = gc.write_data_output('sample')
        self.assertEqual(test1[1][2],'0.030', "no output error")
        # Get the iqr of the final data set 
        test2 = gc.check_iqr_data([['1', 'Z29MUSI3', '0.048', '14.537', '4.121'], ['2', 'IOHC1FWE', '0.030', '12.971', '3.703'], ['3', 'TEUB383I', '0.064', '16.061', '4.494'], ['4', 'm32spobi', '0.070', '13.691', '4.148'], ['5', '67B4RLBN', '0.016', '11.108', '2.837'], ['6', 'LRW2HINU', '0.058', '15.052', '4.314']])
        self.assertEqual(test2[1][5],'-0.005', "no iqr error")

class TestTextRecognition(unittest.TestCase):
    def runTest(self):
        # Read the text from the given image
        test1 = tr.text_recognition(cv2.imread('testing/406.jpg'),'0123456789TF')
        self.assertEqual(test1,'T04F01', "read wrong text error")

unittest.main()