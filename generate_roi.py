import cv2
import argparse
import re
import os

outline_thickness = 5
# path = "preprocess_images2/"
path = "20June(2)_pre/"
def get_roi(image):
    img_color = cv2.imread(path+image)
    img_color = cv2.resize(img_color, None, None, fx=0.5, fy=0.5)
    img_color = cv2.rotate(img_color,cv2.ROTATE_90_COUNTERCLOCKWISE) #change orientation
    img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(img, (7, 7), 0) #reduce noise
    blurred = cv2.bilateralFilter(blurred, 6, sigmaColor=50, sigmaSpace=50) #reduce noise 
    edged = cv2.Canny(blurred, 30, 50, 255) #get the edge 

    # cv2.imshow("Outline of device", edged) 
    # cv2.waitKey(0) 

    #array that contain all the contours in the image
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # sort contours by area, and get the largest
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    cv2.drawContours(edged, contours, 0, (255,0,0), outline_thickness) 
    # cv2.imshow("Target Contour", edged) #display image with roi
    # cv2.waitKey(0)

    x_coor, y_coor, width, height = cv2.boundingRect(contours[0])  #return 4 points 
    roi = img[y_coor : y_coor + height, x_coor : x_coor + width] #crop image (roi)
    # cv2.imshow("ROI", roi) 
    # cv2.waitKey(0)
    # roi = cv2.rotate(roi,cv2.ROTATE_90_CLOCKWISE) #change orientation

    # img_name = re.search("(?<=\/)(.*)(?=\.jpg)",path).group()
    cv2.imwrite(f"20June(2)_post/{image}-roi.jpg", roi)
    return roi

#function to validate if the item is an image
def imageValidator():
    for item in os.listdir(path):
        # print(item)
        get_roi(item)

imageValidator()