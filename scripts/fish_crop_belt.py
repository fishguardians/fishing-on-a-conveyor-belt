import cv2
import numpy as np
from constant import FishImage

"""
Step 2 for fish length image processing

# Mask inversion on a RGB image.
# To remove yellow conveyor belt background
"""

# Crops image based on percentage
def crop_img(img, scale=1.0):
    center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
    width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
    left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
    top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2
    img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
    return img_cropped

def crop_belt(bgimage, original):

    # Reading an image
    # img = cv2.imread('images/samples/barramundi_bg_removed.png')

    # Save the cropped image to object
    # Ensure it scales with the final edited reference image
    original = crop_img(bgimage, 0.9)

    # The kernel to be used for dilation purpose
    kernel = np.ones((5, 5), np.uint8)

    # converting the image to HSV format
    hsv = cv2.cvtColor(bgimage, cv2.COLOR_BGR2HSV)

    # defining the lower and upper values
    # of HSV, this will detect yellow colour
    Lower_hsv = np.array([20, 70, 100])
    Upper_hsv = np.array([30, 255, 255])

    # creating the mask
    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)

    # Inverting the mask
    mask_yellow = cv2.bitwise_not(Mask)
    bgimage = cv2.bitwise_and(bgimage, bgimage, mask=mask_yellow)

    # To remove leftover of background other than the yellow belt
    bgimage = crop_img(bgimage, 0.9)

    return [bgimage,original]

    """
    For testing.
    # cv2.imshow('Result', result)
    # 
    # # waits for user to press any key
    # cv2.waitKey(0)
    # 
    # # closing all open windows
    # cv2.destroyAllWindows()
    """

    
