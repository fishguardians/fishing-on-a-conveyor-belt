from pytesseract import pytesseract
import cv2
import numpy as np
import constant

def text_recognition(image):
    #increase size to read image better
    image = cv2.resize(image, None, fx=4, fy=4)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert from GBR to RGB
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # change orientation
    
    image = cv2.bilateralFilter(image, 5, 30, 60)
    # edged = cv2.Canny(id_image, 30, 200)
    # thresholding = cv2.threshold(id_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("test", opening)
    
    text = pytesseract.image_to_string(opening, \
                                        config='-l eng --psm 3 --oem 3 -c tessedit_char_whitelist="' + constant.tess_whitelist + '" tessedit_char_blacklist="' + constant.tess_blacklist + '"')
    words = ''.join(char for char in text if char.isalnum())
    return words