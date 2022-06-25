import cv2
import numpy as np
from matplotlib import pyplot as plt

"""
Step 2 for fish length image processing

# Mask inversion on a RGB image.
# To remove yellow conveyor belt background
# To remove water reflections on the belt, that affect the contour processing
"""


def crop_belt(image_list):
    for image in image_list:
        # Removing the water reflections on the belt
        # of HSV, this will detect the water reflections of the belt
        GLARE_MIN = np.array([10, 30, 160], np.uint8)
        GLARE_MAX = np.array([40, 65, 250], np.uint8)
        # converting the image to HSV format
        hsv_img = cv2.cvtColor(image.img, cv2.COLOR_BGR2HSV)
        # creating the mask
        mask_reflections = cv2.inRange(hsv_img, GLARE_MIN, GLARE_MAX)
        cv2.imshow("Reflections mask", mask_reflections)

        # Defining the lower and upper values
        # of HSV, this will detect yellow colour
        Lower_hsv = np.array([20, 70, 100])
        Upper_hsv = np.array([30, 255, 255])
        # creating the mask
        mask_yellow_belt = cv2.inRange(hsv_img, Lower_hsv, Upper_hsv)
        cv2.imshow("Yellow mask", mask_yellow_belt)
        cv2.waitKey(0)
        #Join the water reflection mask and yellow belt masks together
        combined_mask = mask_reflections | mask_yellow_belt
        cv2.imshow("Combined mask", combined_mask)
        cv2.waitKey(0)
        # Inverting the mask (Changes the yellow belt and changes it to black pixels)
        mask = cv2.bitwise_not(combined_mask)
        image.img = cv2.bitwise_and(image.img, image.img, mask=mask)

        # Display Output
        cv2.imshow("FINAL OUTPUT", image.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return image_list

# # Converting image to LAB Color so CLAHE can be applied to the luminance channel
# lab_img = cv2.cvtColor(image.img, cv2.COLOR_BGR2LAB)
#
# # Splitting the LAB image to L, A and B channels, respectively
# l, a, b = cv2.split(lab_img)
#
# # ###########Histogram Equlization#############
# # # Apply histogram equalization to the L channel
# # equ = cv2.equalizeHist(l)
# #
# # updated_lab_img1 = cv2.merge((equ, a, b))
# # hist_eq_img = cv2.cvtColor(updated_lab_img1, cv2.COLOR_LAB2BGR)
#
# ###########CLAHE#########################
# # Apply CLAHE to L channel
# clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
# clahe_l = clahe.apply(l)
#
# # Combine the CLAHE enhanced L-channel back with A and B channels
# updated_lab_img2 = cv2.merge((clahe_l, a, b))
#
# # Convert LAB image back to color (RGB)
# CLAHE_img = cv2.cvtColor(updated_lab_img2, cv2.COLOR_LAB2BGR)
#
# cv2.imshow("Before image processing", image.img)
# # cv2.imshow("Equalized image",hist_eq_img)
# cv2.imshow('CLAHE Image', CLAHE_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
