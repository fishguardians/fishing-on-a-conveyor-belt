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

        # TODO:

        # Removing the water reflections on the belt
        # Through CLAHE(Contrast Limited Adaptive Histogram Equalization) And Image Inpainting
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

        # convert to gray
        gray = cv2.cvtColor(image.img, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite('gray.jpg', gray)
        clahe_gray = clahe.apply(gray)
        # cv2.imshow('clahe_gray', clahe_gray)
        # cv2.imwrite('clahe_gray.jpg',clahe_gray )

        # GLARE_MIN = np.array([0, 0, 50], np.uint8)
        # GLARE_MAX = np.array([0, 0, 225], np.uint8)
        GLARE_MIN = np.array([0, 0, 150], np.uint8)
        GLARE_MAX = np.array([10, 10, 255], np.uint8)

        hsv_img = cv2.cvtColor(image.img, cv2.COLOR_BGR2HSV)

        # HSV
        frame_threshed = cv2.inRange(hsv_img, GLARE_MIN, GLARE_MAX)

        # INPAINT + HSV
        inpaint_plus_hsv = cv2.inpaint(image.img, frame_threshed, 0.1, cv2.INPAINT_TELEA)

        # HSV+ INPAINT + CLAHE
        lab = cv2.cvtColor(inpaint_plus_hsv, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe_l = clahe.apply(l)
        lab = cv2.merge((clahe_l, a, b))
        hsv_plus_inpaint_clahe = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        # display it
        cv2.imshow("IMAGE", image.img)
        # cv2.imshow("GRAY", gray)
        cv2.imshow("HSV Mask", frame_threshed)
        cv2.imshow("HSV + INPAINT + CLAHE   ", hsv_plus_inpaint_clahe)

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
