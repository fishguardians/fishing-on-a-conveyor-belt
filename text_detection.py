from textwrap import wrap
import cv2
import pytesseract
import numpy as np
import os
import re

# pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/Cellar/tesseract/5.1.0/bin/tesseract'
dir_path = 'preprocess_images' #directory of the image folder
imageList = [] 

#function to validate if the item is an image
def imageValidator():
    extension = ('png', 'jpg', 'jpeg')
    for item in os.listdir(dir_path):
        if item.endswith(extension): 
            imageList.append(item)
    imageList.sort()
    return imageList
            
imageValidator()
# print(imageList)


cv2.imshow('result',displaySingleImage()) #display image
cv2.waitKey(0)

def textRecognition():
    text = pytesseract.image_to_string(displaySingleImage())
    list1 = []
    list1.append(re.split('\n+',text))
    print(list1)
    return list1

print(textRecognition()[0][1])
#function to generate csv
'''
def generateCsv():
    file = open("text.csv", "w+")
    file.write("")
    file.write(textRecognition())
    file.write("\n")
    file.close()
'''

#function to process all the image 
'''
def imageProcessing():
    for image in imageList:
        image = cv2.imread(dir_path+'/'+image) #read image
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #convert from GBR to RGB
        image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE) #change orientation
        image = cv2.medianBlur(image,5) #reduce noise
        cv2.imshow('result',image) #display image
        cv2.waitKey(0) #destroy window only after any key is press (0)
imageProcessing()
'''
