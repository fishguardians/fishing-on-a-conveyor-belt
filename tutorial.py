import cv2
import numpy as np

# #load image
# # -1, cv2.IMREAD_COLOR: Loads a color image. Any transparency of image will be neglected. It is the default 
# # 0, cv2.IMREAD_GRAYSCALE: Loads image in grayscale mode
# # 1, cv2.IMREAD_UNCHANGED: Load image as such including alpha channel
# img = cv2.imread('assets/fish28.png', -1)

# #Change color in the image
# for i in range (100):
#     for j in range (400):
#         img[i][j] = [0,0,0,0]

# #resize image by pixel
# img = cv2.resize(img, (400,400))
# #resize image by ratio
# # img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)

# #rotate image
# # img = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
# img = cv2.rotate(img, ROTATE_180)

# #saving image
# # cv2.imwrite('new_img.jpg', img)

# #Open CV Blue,Green,Red
# #[0,0,0]
# #Get the dimensions of the image
# # print(img.shape)

# #copy part of the image
# #[row,column]
# fish = img[200:300, 400:500]

#video capturing with camera
# cap = cv2.VideoCapture(0)
#load video
cap = cv2.VideoCapture('assets/fishvideo.mov')

while True:
    ret, frame = cap.read()

    #get width of frame
    width = int(cap.get(3))
    #get height of frame
    height = int(cap.get(4))

    #get shape of the frame
    new_frame = np.zeros(frame.shape, np.uint8)
    #resize the image
    smaller_image = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    #input the images into the frame
    new_frame[:height//2, :width//2] = smaller_image
    new_frame[height//2:, :width//2] = smaller_image
    new_frame[:height//2, width//2:] = smaller_image
    new_frame[height//2:, width//2:] = smaller_image

    #add a line
    #cv2.line(image, start_position, end_position, color, )
    img = cv2.line(frame, (0,0), (width,height), (255,0,0 ), 10)


    # cv2.imshow('frame', image)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

#paste image
#img [row, column] = fish

# #display image on a windows
# cv2.imshow('Fish', img)
# #wait for any key to be pressed (seconds)
# cv2.waitKey(0)
# #destroy windows
# cv2.destroyAllWindows()