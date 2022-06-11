import generate_roi
import digit_recognization as dr
import cv2

def get_text():
    outline_thickness = 5
    path = "preprocess_images/fish03.png"
    # path = "preprocess_images/ocbc.png"
    roi_image = generate_roi.get_roi(path, outline_thickness)
    roi_rgb = cv2.cvtColor(roi_image, cv2.COLOR_GRAY2RGB) #greyscale image 
    roi_grey = cv2.cvtColor(roi_rgb, cv2.COLOR_BGR2GRAY) #greyscale image 
    cv2.imshow("image",roi_grey)
    cv2.waitKey(0)
    dr.digit_recognization(roi_rgb)


get_text()