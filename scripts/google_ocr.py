#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''google_ocr.py: [Working but not used] Module that uses internet connection and google text reader to read images
    @Author: "Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)
import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './googleaccount.json'
# Instantiates a client
client = vision.ImageAnnotatorClient()

def google_ocr(image_path):

    file_name = os.path.abspath(image_path)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    text_detection_response = client.text_detection(image=image)
    annotations = text_detection_response.text_annotations
    if len(annotations) > 0:
        text = annotations[0].description
        text=text.replace(" ", "")
        text=text.replace("\n", "")
    else:
        text = ""
    # print("Extracted text {} from image ({} chars).".format(text, len(text)))

    return text