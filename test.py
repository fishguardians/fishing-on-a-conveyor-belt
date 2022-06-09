from textwrap import wrap
import cv2
import pytesseract
import numpy as np
import os
import re

# pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/Cellar/tesseract/5.1.0/bin/tesseract'
dir_path = 'preprocess_images' #directory of the image folder
imageList = [] 

#function to count number of files in the image folder
def imageValidator():
    extension = ('png', 'jpg', 'jpeg')
    for item in os.listdir(dir_path):
        if item.endswith(extension): #validate extension (if it is an image)
            imageList.append(item)
    imageList.sort()
    return imageList
            
imageValidator()
# print(imageList)

def displaySingleImage():
    image = cv2.imread(dir_path+'/'+'fish05.png') #read image
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #convert from GBR to RGB
    image = cv2.rotate(image,cv2.ROTATE_90_COUNTERCLOCKWISE) #change orientation
    image = cv2.medianBlur(image,5) #reduce noise
    return image

def increaseContrastImage():
    image = displaySingleImage()
    matrix = np.ones(image.shape)*1.2
    img_bright = np.uint8(cv2.multiply(np.float64(image),matrix))
    return img_bright

def brighterImage():
    image = displaySingleImage()
    matrix = np.ones(image.shape,dtype="uint8")*50
    imgBright = cv2.add(image,matrix)
    return imgBright
    
def darkerImage():
    image = displaySingleImage()
    matrix = np.ones(image.shape,dtype="uint8")*50
    imgDark = cv2.subtract(image,matrix)
    return imgDark

   
def greyImage():
    image = displaySingleImage()
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #grey image
    return grey_image






# define the dictionary of digit segments so we can identify
# each digit on the thermostat
DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}

def readDigit():
    # pre-process the image by resizing it, converting it to
    # graycale, blurring it, and computing an edge map
    BCOLOR = (75, 0, 130)
    THICKNESS = 4
    image = displaySingleImage()
    image = cv2.resize(image, None,None,fx=0.5,fy=0.5) #resize image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to greycale
    blurred = cv2.GaussianBlur(gray, (3, 3), 0) #blur image
    blurred = cv2.bilateralFilter(blurred,5,sigmaColor=50,sigmaSpace=50)
    edged = cv2.Canny(blurred, 30, 100, 255) #compute edge map
    cnts, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # sort contours by area, and get the first 10
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:9]

    # cv2.drawContours(image, cnts, 0, BCOLOR, THICKNESS)
    # cv2.imshow("Target Contour", image)
    # cv2.waitKey(0)

    # for i, cnt in enumerate(cnts):
    #     cv2.drawContours(image, cnts, i, BCOLOR, THICKNESS)
    #     print(f"ContourArea:{cv2.contourArea(cnt)}")
    #     cv2.imshow("Contour one by one", image)
    #     cv2.waitKey(0)
    return edged


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
