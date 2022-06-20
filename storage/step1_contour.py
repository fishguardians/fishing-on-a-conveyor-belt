import cv2

GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)
THICKNESS = 4
FONT = cv2.FONT_HERSHEY_SIMPLEX

thresh_lower = 130 #lower threshold
thresh_upper = 150 #upper threshold


img_color = cv2.imread("preprocess_images/ocbc.png") #read image
img_color = cv2.resize(img_color, None, None, fx=0.5, fy=0.5) #resize
img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)  #greyscale 

blurred = cv2.GaussianBlur(img, (7, 7), 0)  #reduce noise
blurred = cv2.bilateralFilter(blurred, 5, sigmaColor=50, sigmaSpace=50) #reduce noise
edged = cv2.Canny(blurred, thresh_lower, thresh_upper, 255)  #get the edge 

cv2.imshow("Outline of device", edged) #display image 
cv2.waitKey(0)

cnts, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
# sort contours by area, and get the first 10
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]


for i, cnt in enumerate(cnts):
    print(i,"->",cnt)
    cv2.drawContours(img_color, cnts, i, GREEN, THICKNESS) 
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(img_color, (x, y), (x + w, y + h), YELLOW, THICKNESS)
    area = round(cv2.contourArea(cnt), 1)

    peri = round(cv2.arcLength(cnt, closed=True), 1)
    if(80>area>60 and peri>2000):
        print(f"ContourArea:{area}, Peri: {peri}")
        cv2.putText(img_color, "Area:" + str(area), (x, y - 15), FONT, 0.4, GREEN, 1)
        cv2.putText(img_color, "Perimeter:" + str(peri), (x, y - 5), FONT, 0.4, GREEN, 1)

cv2.imshow("Contours", img_color)
cv2.waitKey(0)
