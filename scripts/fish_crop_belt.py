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

def crop_belt(imageList):

    # Reading an image
    # img = cv2.imread('images/samples/barramundi_bg_removed.png')

    for image in imageList:

        # # Save the cropped image to object
        # # Ensure it scales with the final edited reference image
        # image.org = crop_img(image.img, 0.9)

        # The kernel to be used for dilation purpose
        kernel = np.ones((5, 5), np.uint8)

        # converting the image to HSV format
        hsv = cv2.cvtColor(image.img, cv2.COLOR_BGR2HSV)

        # defining the lower and upper values
        # of HSV, this will detect yellow colour
        Lower_hsv = np.array([20, 70, 100])
        Upper_hsv = np.array([30, 255, 255])

        # creating the mask
        Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)

        # Inverting the mask
        mask_yellow = cv2.bitwise_not(Mask)
        image.img = cv2.bitwise_and(image.img, image.img, mask=mask_yellow)

        # To remove leftover of background other than the yellow belt
        image.img = crop_img(image.img, 0.9)
        cropped = image.img

        # Original image's height and width
        og_height = np.size(image.org, 0)
        og_width = np.size(image.org, 1)

        # Cropped image 's height and width
        crp_height = np.size(cropped, 0)
        crp_width = np.size(cropped, 1)

        # Adding black borders to sides of image
        h_border = int((og_height - crp_height))
        w_border = int((og_width - crp_width))
        print('h_border: ', h_border, 'w_border', w_border)

        # For full scale measurements of the image
        # Black borders are added to match the cropped image with the width of the original image

        # params: src, top, bottom, left, right
        crp_borders = cv2.copyMakeBorder(cropped, h_border, h_border, w_border, w_border, cv2.BORDER_CONSTANT, None, value=0)
        cb_height = np.size(crp_borders, 0)
        cb_width = np.size(crp_borders, 1)
        print('cb_height: ',cb_height, 'cb_width: ', cb_width)

        # Write new cropped image to image.img
        image.img = crp_borders

        # cv2.imshow('crop with borders', crp_borders)
        # cv2.waitKey(0)

        # # For testing.
        # cv2.imshow('Result', image.img)
        # # waits for user to press any key
        # cv2.waitKey(0)
        # # closing all open windows
        # cv2.destroyAllWindows()

        """
        # For testing.
        cv2.imshow('Result', result)

        # waits for user to press any key
        cv2.waitKey(0)

        # closing all open windows
        cv2.destroyAllWindows()
        """

    return imageList
