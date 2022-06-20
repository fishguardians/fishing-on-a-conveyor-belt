from logging import PlaceHolder
import cv2
import numpy as np
import generate_roi
import os
import imutils



FONT = cv2.FONT_HERSHEY_SIMPLEX
CYAN = (255, 255, 0)
DIGITSDICT = {
    (1, 1, 1, 1, 1, 1, 0): 0,
    (0, 1, 1, 0, 0, 0, 0): 1,
    (1, 1, 0, 1, 1, 0, 1): 2,
    (1, 1, 1, 1, 0, 0, 1): 3,
    (0, 1, 1, 0, 0, 1, 1): 4,
    (1, 0, 1, 1, 0, 1, 1): 5,
    (1, 0, 1, 1, 1, 1, 1): 6,
    (1, 1, 1, 0, 0, 0, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9,
}
dir_path = 'processed_images2/' 
imageList = [] #list to store image
outputList = [] #list to store the output


def digit_recognition(image):
    # path = re.search("(?<=\/)(.*)(?=\.jpg)",generate_roi.path).group()
    # roi_color = cv2.imread("processed_images/"+path+"-roi.jpg")
    roi_color = cv2.imread(dir_path+image)
    roi_color = cv2.resize(roi_color, None,None,fx=1.2,fy=1.2) #resize image
    roi_color= imutils.rotate(roi_color, angle=6)
    # roi_color = cv2.rotate(roi_color,cv2.ROTATE_90_COUNTERCLOCKWISE) #change orientation
    roi = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY) #greyscale image 
    # cv2.imshow("Blurred and Trimmed", roi)
    # cv2.waitKey(0)

    roi = cv2.bilateralFilter(roi, 5, 30, 60) #reduce noise
    #roi.shape[0] = height, roi.shape[1] = width
    RATIO = roi.shape[0] * 0.01
    #trim image, in sequence of y1:y2, x1:x2
    trimmed = roi[int(RATIO)+2 :, int(RATIO) : roi.shape[1] - int(RATIO)-10]

    edged = cv2.adaptiveThreshold(  
        trimmed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5
    )
    # cv2.imshow("trimmed_image", trimmed) #display thresholded image
    # cv2.waitKey(0)

    #enhance image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 5))
    dilated = cv2.dilate(edged, kernel, iterations=1)

    # cv2.imshow("Dilated", dilated)
    # cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
    dilated = cv2.dilate(dilated, kernel, iterations=1)

    # cv2.imshow("Dilated x2", dilated)
    # cv2.waitKey(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 1),)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    h = roi.shape[0] 
    ratio = int(h * 0.01) 
    eroded[-ratio:,] = 0 
    eroded[:, :ratio] = 0

    cnts, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    digits_cnts = []

    canvas = trimmed.copy()
    cv2.drawContours(canvas, cnts, -1, (255, 255, 255), 1)
    # cv2.imshow("All Contours", canvas)
    # cv2.waitKey(0)

    #detect & draw contours in random sequence
    for cnt in cnts:
        #compute bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(cnt)
        if h > 50: #determine if the item should be read (by height)
            digits_cnts.append(cnt) #determine how many digits are there
            # print(digits_cnts)
            #draw bounding box
            cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 0), 1)
            cv2.drawContours(canvas, cnt, 0, (255, 255, 255), 1)
            # cv2.imshow("Digit Contours", canvas)
            # cv2.waitKey(0)

    # print(f"No. of Digit Contours: {len(digits_cnts)}")

    #sort by the value of the x coordinates of the countour
    sorted_digits = sorted(digits_cnts, key=lambda cnt: cv2.boundingRect(cnt)[0])
    # print(sorted_digits)

    canvas = trimmed.copy()
    #draw contours in sorted sequence
    for i, cnt in enumerate(sorted_digits):
        (x, y, w, h) = cv2.boundingRect(cnt)
        #check if the width of the bounding box is too small.
        #solve the issue for digit '1'
        if w < 24:
            x-=21
            w = 32
        else:
            pass
        cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 0), 1)
        cv2.putText(canvas, str(i), (x, y - 3), FONT, 0.3, (0, 0, 0), 1)
        # cv2.imshow("All Contours sorted", canvas)
        # cv2.waitKey(0)

    digits = []
    canvas = trimmed.copy()

    #loop over each of the digit
    for cnt in sorted_digits:
        # extract the digit ROI
        #x coordinate, y coordinate, width, height
        (x, y, w, h) = cv2.boundingRect(cnt)
        #check if the width is too small.
        if w < 24:
            x-=21
            w = 32
        else:
            pass
        #y1,y2,x1,x2
        roi = eroded[y : y + h, x : x + w]
        qW, qH = int(w * 0.25), int(h * 0.15)
        fractionH, halfH, fractionW = int(h * 0.05), int(h * 0.5), int(w * 0.25)

        # seven segments in the order of wikipedia's illustration
        sevensegs = [
            ((0, 0), (w, qH)),  # a (top bar)
            ((w - qW, 0), (w, halfH)),  # b (upper right)
            ((w - qW, halfH), (w, h)),  # c (lower right)
            ((0, h - qH), (w, h)),  # d (lower bar)
            ((0, halfH), (qW, h)),  # e (lower left)
            ((0, 0), (qW, halfH)),  # f (upper left)
            # ((0, halfH - fractionH), (w, halfH + fractionH)) # center
            (
                (0 + fractionW, halfH - fractionH),
                (w - fractionW, halfH + fractionH),
            ),  # center / g 
        ]

        # initialize to off
        on = [0] * 7
        try:
            for (i, ((p1x, p1y), (p2x, p2y))) in enumerate(sevensegs):
                region = roi[p1y:p2y, p1x:p2x]
                # print(p1y,p2y, p1x,p2x)
                # print(
                #     f"{i}: Sum of 1: {np.sum(region == 255)}, Sum of 0: {np.sum(region == 0)}, Shape: {region.shape}, Size: {region.size}"
                # )
                #detect seven segments and store inside the array
                if np.sum(region == 255) > region.size * 0.5:
                    on[i] = 1
                
                # print(f"State of ON: {on}")

            digit = DIGITSDICT[tuple(on)]
            print(f"Digit is: {digit}")
            digits += [digit]
            cv2.rectangle(canvas, (x, y), (x + w, y + h), CYAN, 1)
            cv2.putText(canvas, str(digit), (x - 5, y + 6), FONT, 0.3, (0, 0, 0), 1)
            # cv2.imshow("Digit", canvas)
            # cv2.waitKey(0)
        except:
            pass
    if(len(digits)==4):
        digit = ''.join(map(str, digits[1:]))
        digit = str(digits[0])+"."+digit
        return digit
    else:
        return "N.A"

#function to validate if the item is an image
def imageValidator():
    extension = ('png', 'jpg', 'jpeg')
    for item in os.listdir(dir_path):
        if item.endswith(extension): 
            imageList.append(item)
    imageList.sort()
    return imageList

imageList = imageValidator()
for image in imageList:
    outputList.append(digit_recognition(image))

# print(digit_recognition("Frame13.jpg-roi.jpg"))
print(outputList)