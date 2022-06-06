from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import argparse
import numpy as np
import imutils
import cv2

"""
USAGE
python object_size.py --image images/barramundi_28.png --width 1.2
python object_size.py --image images/barramundi_32.png --width 1.2
python object_size.py --image images/snapper_71.png --width 1.2
"""

# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
ap.add_argument("-w", "--width", type=float, required=True,
                help="width of the left-most object in the image (in inches)")
args = vars(ap.parse_args())

# Load the image
image = cv2.imread(args["image"])
# print(image.shape)
x, y, z = image.shape

# Load the reference image (Ruler for length)
imageRef = cv2.imread('images/ruler.png')

# Cropping the image to get only the fish
sliceImage = image[:, 750:1080, :]

# Concats the ref image with the fish image
h_img = cv2.hconcat([imageRef, sliceImage]) # Horizontal
cv2.imshow('Horizontal', h_img)
sliceImage = h_img

# convert it to grayscale, and blur it slightly
gray = cv2.cvtColor(sliceImage, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# Displays the title of the image display in the window
def show_image(title, image, destroy_all=True):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    if destroy_all:
        cv2.destroyAllWindows()

# Function is needed for the createTrackbar step downstream
def nothing(x):
    pass

# Returns the midpoint of 2 points
def midpoint(ptA, ptB):
    return (ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5

# Creates a window
def tuneCanny(image):
    window = 'canny'
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.createTrackbar('threshold1', window, 10, 500, nothing)
    cv2.createTrackbar('threshold2', window, 10, 500, nothing)

    while True:
        image_copy = np.copy(image)
        threshold1 = cv2.getTrackbarPos('threshold1', window)
        threshold2 = cv2.getTrackbarPos('threshold2', window)

        # Displays the image based on the new and adjusted threshold values
        edged = cv2.Canny(image_copy, threshold1, threshold2)
        cv2.imshow('edged', edged)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    return threshold1, threshold2

# For getting thresholds for Canny
# tuneCanny(gray)
t1, t2 = tuneCanny(gray)
print(f"Threshold1: {t1}, Threshold2: {t2}")

# Performs edge detection, then perform a dilation + erosion to
# Closes gaps in between object edges
edged = cv2.Canny(gray, t1, t2)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
show_image("erode and dilate", edged, True)

# find contours in the edge map
cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
# print("Total number of contours are: ", len(cnts))

# sort the contours from left-to-right and initialize the
# 'pixels per metric' calibration variable
(cnts, _) = contours.sort_contours(cnts)
pixelPerMetric = None

# loop over the contours individually
count = 0
for c in cnts:
    # if the contour is not sufficiently large, ignore it
    if cv2.contourArea(c) < 1000:
        continue
    count += 1

    # compute the rotated bounding box of the contour
    orig = sliceImage.copy()

    # order the points in the contour such that they appear
    # in top-left, top-right, bottom-right, and bottom-left
    # order, then draw the outline of the rotated bounding box
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")

    box = perspective.order_points(box)
    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

    # loop over the original points and draw them
    for (x, y) in box:
        cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

    # unpack the ordered bounding box, then compute the midpoint
    # between the top-left and top-right coordinates, followed by
    # the midpoint between bottom-left and bottom-right coordinates
    (tl, tr, br, bl) = box
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)

    # compute the midpoint between the top-left and top-right points,
    # followed by the midpoint between the top-right and bottom-right
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)

    cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

    # draw lines between the midpoints
    cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)), (255, 0, 255), 2)
    cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)), (255, 0, 255), 2)

    # compute the Euclidean distance between the midpoints
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    # if the pixels per metric has not been initialized, then
    # compute it as the ratio of pixels to supplied metric
    # (in this case, inches)
    if pixelPerMetric is None:
        pixelPerMetric = dB / args["width"]

    # compute the size of the object
    dimA = dA / pixelPerMetric # Length
    dimB = dB / pixelPerMetric # Depth

    cv2.putText(orig, "{:.1f}in".format(dimA), (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    cv2.putText(orig, "{:.1f}in".format(dimB), (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    # show the output image
    cv2.imshow("Image", orig)
    cv2.waitKey(0)

# print("Total contours processed: ", count)
print("Dimensions of fish",
      "------------",
      "Length: {}".format(dimA),
      "Depth: {}".format(dimB), sep='\n')
