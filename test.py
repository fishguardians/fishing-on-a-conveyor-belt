import cv2
import numpy as np

FONT = cv2.FONT_HERSHEY_SIMPLEX
CYAN = (255, 255, 0)
DIGITS_LOOKUP = {
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

roi_color = cv2.imread("processed_images/fish03-roi.png")
img_color = cv2.rotate(roi_color,cv2.ROTATE_90_COUNTERCLOCKWISE) #change orientation
roi = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY) #greyscale image 
cv2.imshow("Blurred and Trimmed", roi_color)
cv2.waitKey(0)

roi = cv2.bilateralFilter(roi, 5, 30, 60) #reduce noise
#y1:y2, x1:x2
trimmed = roi[80: 160, 150 : 380]  #trim image
roi_color = roi[80: 160, 150 : 380] #trim image

edged = cv2.adaptiveThreshold(  
    trimmed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5
)
cv2.imshow("Edged", edged) #display thresholded image
cv2.waitKey(0)

#-----enhance image ----------
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 5))
dilated = cv2.dilate(edged, kernel, iterations=1)

cv2.imshow("Dilated", dilated)
cv2.waitKey(0)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
dilated = cv2.dilate(dilated, kernel, iterations=1)

# cv2.imshow("Dilated x2", dilated)
# cv2.waitKey(0)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 1),)
eroded = cv2.erode(dilated, kernel, iterations=1)

# cv2.imshow("Eroded", eroded)
# cv2.waitKey(0)

h = roi.shape[0] #304
ratio = int(h * 0.01) #3
eroded[-ratio:,] = 0
eroded[:, :ratio] = 0

cv2.imshow("Eroded + Black", eroded)
cv2.waitKey(0)

cnts, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# print("cnts=",cnts)
digits_cnts = []

canvas = trimmed.copy()
cv2.drawContours(canvas, cnts, -1, (255, 255, 255), 1)
cv2.imshow("All Contours", canvas)
cv2.waitKey(0)
#-------------------------------------

#detect & draw contours in random sequence
for cnt in cnts:
    #compute bounding box of the contour
    (x, y, w, h) = cv2.boundingRect(cnt)
    if h > 50: #determine if the item should be read (by height)
        digits_cnts.append(cnt) #determine how many digits are there
        # print(digits_cnts)
        cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 0), 1)
        cv2.drawContours(canvas, cnt, 0, (255, 255, 255), 1)
        cv2.imshow("Digit Contours", canvas)
        cv2.waitKey(0)

print(f"No. of Digit Contours: {len(digits_cnts)}")

#sort by the value of the x coordinates of the countour
sorted_digits = sorted(digits_cnts, key=lambda cnt: cv2.boundingRect(cnt)[0])
# print(sorted_digits)

canvas = trimmed.copy()

#draw contours in sorted sequence
for i, cnt in enumerate(sorted_digits):
    (x, y, w, h) = cv2.boundingRect(cnt)
    cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 0, 0), 1)
    cv2.putText(canvas, str(i), (x, y - 3), FONT, 0.3, (0, 0, 0), 1)
    cv2.imshow("All Contours sorted", canvas)
    cv2.waitKey(0)

digits = []
canvas = roi_color.copy()
for cnt in sorted_digits:
  # extract the digit ROI
	(x, y, w, h) = cv2.boundingRect(cnt)
	roi = eroded[y:y + h, x:x + w]
	# compute the width and height of each of the 7 segments
	# we are going to examine
	(roiH, roiW) = roi.shape
	(dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
	dHC = int(roiH * 0.05)
	# define the set of 7 segments
	segments = [
		((0, 0), (w, dH)),	# top
		((0, 0), (dW, h // 2)),	# top-left
		((w - dW, 0), (w, h // 2)),	# top-right
		((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
		((0, h // 2), (dW, h)),	# bottom-left
		((w - dW, h // 2), (w, h)),	# bottom-right
		((0, h - dH), (w, h))	# bottom
	]
	on = [0] * len(segments)
  # loop over the segments
	for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
		# extract the segment ROI, count the total number of
		# thresholded pixels in the segment, and then compute
		# the area of the segment
		segROI = roi[yA:yB, xA:xB]
		total = cv2.countNonZero(segROI)
		area = (xB - xA) * (yB - yA)
		# if the total number of non-zero pixels is greater than
		# 50% of the area, mark the segment as "on"
		if total / float(area) > 0.5:
			on[i]= 1
	# lookup the digit and draw it on the image
	digit = DIGITS_LOOKUP[tuple(on)]
	digits.append(digit)
	cv2.rectangle(canvas, (x, y), (x + w, y + h), (0, 255, 0), 1)
	cv2.putText(canvas, str(digit), (x - 10, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

# display the digits
print(u"{}{}.{} \u00b0C".format(*digits))
cv2.imshow("Output", digits)
cv2.waitKey(0)
    
# print(f"Digits on the token are: {digits}")

