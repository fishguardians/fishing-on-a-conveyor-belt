""""
Not as effective as object_bg3
"""

# import cv2
# import numpy as np
#
# # Read image
# img = cv2.imread('images/barramundi_28.png')
# hh, ww = img.shape[:2]
#
# # # threshold on white
# # # Define lower and uppper limits
# # lower = np.array([200, 200, 200])
# # upper = np.array([255, 255, 255])
#
# # threshold on yellow
# # Define lower and uppper limits
# lower = np.array([0, 130, 130])
# upper = np.array([100, 255, 255])
#
# # Create mask to only select black
# thresh = cv2.inRange(img, lower, upper)
#
# # apply morphology
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
# morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
#
# # invert morp image
# mask = 255 - morph
#
# # apply mask to image
# result = cv2.bitwise_and(img, img, mask=mask)
#
# # save results
# # cv2.imwrite('barramundi_28.png', thresh)
# # cv2.imwrite('barramundi_28.png', morph)
# # cv2.imwrite('barramundi_28.png', mask)
# # cv2.imwrite('barramundi_28.png', result)
#
# cv2.imshow('thresh', thresh)
# cv2.imshow('morph', morph)
# cv2.imshow('mask', mask)
# cv2.imshow('result', result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
