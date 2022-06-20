from logging import PlaceHolder
import cv2
import numpy as np
import generate_roi
import re



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
    (1, 1, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9,
}

generate_roi.get_roi()

def digit_recognization():
    path = re.search("(?<=\/)(.*)(?=\.png)",generate_roi.path).group()
    roi_color = cv2.imread("processed_images/"+path+"-roi.png")
    # img_color = cv2.rotate(roi_color,cv2.ROTATE_90_COUNTERCLOCKWISE) #change orientation
    roi = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY) #greyscale image 
    # cv2.imshow("Blurred and Trimmed", roi)
    # cv2.waitKey(0)

    roi = cv2.bilateralFilter(roi, 5, 30, 60) #reduce noise
    #y1:y2, x1:x2
    trimmed = roi[80: 160, 150 : 380]  #trim image
    # roi_color = roi[80: 160, 150 : 380] #trim image

    edged = cv2.adaptiveThreshold(  
        trimmed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5
    )
    # cv2.imshow("Edged", edged) #display thresholded image
    # cv2.waitKey(0)

    #-----enhance image ---------------------------------------------------------------------------------
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

    # cv2.imshow("Eroded", eroded)
    # cv2.waitKey(0)
    #---------------------------------------------------------------------------------------------------------------

    h = roi.shape[0] #304
    ratio = int(h * 0.01) #3
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
            cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 0), 1)
            cv2.drawContours(canvas, cnt, 0, (255, 255, 255), 1)
            # cv2.imshow("Digit Contours", canvas)
            # cv2.waitKey(0)

    # print(f"No. of Digit Contours: {len(digits_cnts)}")

    #sort by the value of the x coordinates of the countour
    sorted_digits = sorted(digits_cnts, key=lambda cnt: cv2.boundingRect(cnt)[0])
    # print(sorted_digits)

    canvas = trimmed.copy()
    placeHolder= [0,0]
    #draw contours in sorted sequence
    for i, cnt in enumerate(sorted_digits):
        (x, y, w, h) = cv2.boundingRect(cnt)
        if w < placeHolder[1]:
            x = placeHolder[0]+placeHolder[1]+7
            w = placeHolder[1]
        else:
            placeHolder[0] = x
            placeHolder[1] = w
        cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 0), 1)
        cv2.putText(canvas, str(i), (x, y - 3), FONT, 0.3, (0, 0, 0), 1)
        cv2.imshow("All Contours sorted", canvas)
        cv2.waitKey(0)

    digits = []
    canvas = trimmed.copy()
    # canvas = roi_color.copy()

    for cnt in sorted_digits:
        # extract the digit ROI
        (x, y, w, h) = cv2.boundingRect(cnt)
        if w < placeHolder[1]:
            x = placeHolder[0]+placeHolder[1] +7
            w = placeHolder[1]
        else:
            placeHolder[0] = x
            placeHolder[1] = w
        # compute the width and height of each of the 7 segments
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
            ),  # center
        ]

        # initialize to off
        on = [0] * 7
        
        for (i, ((p1x, p1y), (p2x, p2y))) in enumerate(sevensegs):
            region = roi[p1y:p2y, p1x:p2x]
            # print(region)
            # print(
            #     f"{i}: Sum of 1: {np.sum(region == 255)}, Sum of 0: {np.sum(region == 0)}, Shape: {region.shape}, Size: {region.size}"
            # )
            #detect seven segments and store inside the array
            if np.sum(region == 255) > region.size * 0.2:
                on[i] = 1
            
            # print(f"State of ON: {on}")

        digit = DIGITSDICT[tuple(on)]
        # print(f"Digit is: {digit}")
        digits += [digit]
        cv2.rectangle(canvas, (x, y), (x + w, y + h), CYAN, 1)
        cv2.putText(canvas, str(digit), (x - 5, y + 6), FONT, 0.3, (0, 0, 0), 1)
        # cv2.imshow("Digit", canvas)
        # cv2.waitKey(0)
    digit = ''.join(map(str, digits[1:]))
    digit = str(digits[0])+"."+digit
    print(digit)

if __name__ == "__main__":
    digit_recognization()