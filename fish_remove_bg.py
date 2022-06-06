import cv2
import numpy as np

# read image
img = cv2.imread('images/barramundi_28.png')

# threshold on yellow
lower = (0, 120, 120)
upper = (100, 255, 255)
thresh = cv2.inRange(img, lower, upper)

# apply dilate morphology
kernel = np.ones((9, 9), np.uint8)
mask = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

# get largest contour
contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]
big_contour = max(contours, key=cv2.contourArea)

# These values can be used to either draw a rectangle or crop out the image part using pixel coordinates.
# X coordinate, Y coordinate, Width, Height
x, y, width, height = cv2.boundingRect(big_contour)

# Crop image to specified area using slicing
# Crop out only the yellow conveyor belt area
result = img[y:y+height, x:x+width]


# show the images
# cv2.imshow("cropped", result)
cv2.imwrite('images/fish_bg_removed.png', result)
cv2.waitKey(0)
cv2.destroyAllWindows()

# draw filled white contour on input
# result = img.copy()
# cv2.rectangle(result,(x,y),(x+width,y+height),(255,255,255),-1)
# cv2.imwrite('fish_bg_removed.png', result)

