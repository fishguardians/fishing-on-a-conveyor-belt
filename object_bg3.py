# Python program to explain
# mask inversion on a RGB image.

# importing cv2 and numpy library
import cv2
import numpy as np

# Reading an image
img = cv2.imread('images/barramundi_28.png')

# The kernel to be used for dilation
# purpose
kernel = np.ones((5, 5), np.uint8)

# converting the image to HSV format
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# defining the lower and upper values
# of HSV, this will detect yellow colour
Lower_hsv = np.array([20, 70, 100])
Upper_hsv = np.array([30, 255, 255])

# creating the mask
Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)

# Inverting the mask
mask_yellow = cv2.bitwise_not(Mask)
Mask = cv2.bitwise_and(img, img, mask=mask_yellow)

# Displaying the image
cv2.imshow('Mask', Mask)
cv2.imwrite('Mask.png', Mask)

# waits for user to press any key
cv2.waitKey(0)

# closing all open windows
cv2.destroyAllWindows()
