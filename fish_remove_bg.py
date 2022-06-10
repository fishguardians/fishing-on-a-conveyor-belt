import numpy as np
import cv2
import os
import sys
from pathlib import Path

"""
Step 1 for fish length image processing

Imports and processes the raw fish images 
and crops out the non-conveyor belt parts of the image. 
Leaving only the yellow conveyor belt parts of the image
that contains the fish itself and its ID.
"""

# read image (for testing individual images)
img = cv2.imread('images/import/barramundi_28.png')
# img = cv2.imread('images/import/barramundi_32.png')
# img = cv2.imread('images/import/snapper_71.png')

def remove_background(image_arr):
    for img in image_arr:
        # print(img)

        # Threshold on yellow
        lower = (0, 120, 120)
        upper = (100, 255, 255)
        thresh = cv2.inRange(img, lower, upper)

        # Apply dilate morphology
        kernel = np.ones((9, 9), np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

        # Get largest contour
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        big_contour = max(contours, key=cv2.contourArea)

        # These values can be used to either draw a rectangle or crop out the image part using pixel coordinates.
        # X coordinate, Y coordinate, Width, Height
        x, y, width, height = cv2.boundingRect(big_contour)

        # Crop image to specified area using slicing
        # Crop out only the yellow conveyor belt area
        result = img[y:y + height, x:x + width]

        # Show the images (for testing)
        # cv2.imshow("cropped", result)

        # Export the images
        cv2.imwrite("images\\export\\barramundi_belt_removed_{}.png", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

"""
# For future reference if needed

# draw filled white contour on input
# result = img.copy()
# cv2.rectangle(result,(x,y),(x+width,y+height),(255,255,255),-1)
# cv2.imwrite('barramundi_bg_removed.png', result)
"""
