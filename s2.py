import cv2
import numpy as np
import segments
# from segments import Segments

img = cv2.imread("processed_images/new1-roi.jpg")
img = cv2.resize(img, None,None,fx=2,fy=2) #resize image
# img_color = cv2.rotate(roi_color,cv2.ROTATE_90_COUNTERCLOCKWISE) #change orientation
roi = cv2.cvtColor(img, cv2.COLOR_BGR2LAB) #greyscale image 
l,a,b = cv2.split(img);
cv2.imshow("Blurred and Trimmed", img)
cv2.waitKey(0)

lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB);
l,a,b = cv2.split(lab);

# show
cv2.imshow("orig", img);

# closing operation
kernel = np.ones((5,5), np.uint8);

# threshold params
low = 165;
high = 200;
iters = 3;

# make copy
copy = b.copy();

# threshold
thresh = cv2.inRange(copy, low, high);

# dilate
for a in range(iters):
    thresh = cv2.dilate(thresh, kernel);

# erode
for a in range(iters):
    thresh = cv2.erode(thresh, kernel);

# show image
cv2.imshow("thresh", thresh);
cv2.imwrite("threshold.jpg", thresh);

# start processing
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE);

# draw
for contour in contours:
    cv2.drawContours(img, [contour], 0, (0,255,0), 3);

# get res of each number
bounds = [];
h, w = img.shape[:2];
for contour in contours:
    left = w;
    right = 0;
    top = h;
    bottom = 0;
    for point in contour:
        point = point[0];
        x, y = point;
        if x < left:
            left = x;
        if x > right:
            right = x;
        if y < top:
            top = y;
        if y > bottom:
            bottom = y;
    tl = [left, top];
    br = [right, bottom];
    bounds.append([tl, br]);

# crop out each number
cuts = [];
number = 0;
for bound in bounds:
    tl, br = bound;
    cut_img = thresh[tl[1]:br[1], tl[0]:br[0]];
    cuts.append(cut_img);
    number += 1;
    cv2.imshow(str(number), cut_img);

# font 
font = cv2.FONT_HERSHEY_SIMPLEX;

# create a segment model
model = segments();
index = 0;
for cut in cuts:
    # save image
    cv2.imwrite(str(index) + "_" + str(number) + ".jpg", cut);

    # process
    model.digest(cut);
    number = model.getNum();
    print(number);
    cv2.imshow(str(index), cut);

    # draw and save again
    h, w = cut.shape[:2];
    drawn = np.zeros((h, w, 3), np.uint8);
    drawn[:, :, 0] = cut;
    drawn = cv2.putText(drawn, str(number), (10,30), font, 1, (0,0,255), 2, cv2.LINE_AA);
    cv2.imwrite("drawn" + str(index) + "_" + str(number) + ".jpg", drawn);
    
    index += 1;
    # cv2.waitKey(0);


# show
cv2.imshow("contours", img);
cv2.imwrite("contours.jpg", img);
cv2.waitKey(0);