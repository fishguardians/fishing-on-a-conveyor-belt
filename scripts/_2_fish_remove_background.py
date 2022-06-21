import cv2
import numpy as np
from constant import FishImage

"""
Step 2 for fish length image processing

# Mask inversion on a RGB image.
# To remove yellow conveyor belt background
# To remove water reflections on the belt, that affect the contour processing
"""

# Crops image based on percentage
# def crop_img(img, scale=1.0):
#     center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
#     width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
#     left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
#     top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2
#     img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
#     return img_cropped


def crop_belt(image_list):
    for image in image_list:

        # The kernel to be used for dilation purpose
        # kernel = np.ones((5, 5), np.uint8)

        # converting the image to HSV format
        hsv = cv2.cvtColor(image.img, cv2.COLOR_BGR2HSV)

        # defining the lower and upper values
        # of HSV, this will detect yellow colour
        Lower_hsv = np.array([20, 70, 100])
        Upper_hsv = np.array([30, 255, 255])

        # creating the mask
        Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)

        # Inverting the mask (Changes the yellow belt and changes it to black pixels)
        mask_yellow = cv2.bitwise_not(Mask)
        image.img = cv2.bitwise_and(image.img, image.img, mask=mask_yellow)

        # Removing the water reflections on the belt
        # Through CLAHE(Contrast Limited Adaptive Histogram Equalization)

        # create a CLAHE object (Arguments are optional).
        # Changing image to grayscale for histogram processing
        grayscale = cv2.cvtColor(image.img, cv2.COLOR_BGR2GRAY)
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # image.img = clahe.apply(grayscale)


        """
        TESTING
        """
        equ = cv2.equalizeHist(grayscale)
        res = np.hstack((grayscale, equ))  # stacking images side-by-side
        cv2.imshow('result', res)


        # Display the output images
        cv2.imshow('Removed_belt&reflections', image.img) #Demonstration
        cv2.waitKey(0) #Demonstration

        # cv2.namedWindow("Output_Resized", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("Output_Resized", 640, 360)
        # cv2.imshow("Output_Resized", image.img)
        # cv2.waitKey(0)

        # cv2.destroyAllWindows()

    return image_list
