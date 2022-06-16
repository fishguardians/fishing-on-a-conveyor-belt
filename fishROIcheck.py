import cv2
import numpy as np
import os
import constant


def RemoveUnwantedFrames():
    folderIncrement = 0
    imageIncrement = 0
    imageFolder_list = os.listdir(constant.image_storage)
    print(f'Number of videos found : {len(imageFolder_list)}')

    while folderIncrement < len(imageFolder_list):
        imageIncrement = 0
        currentFolder = imageFolder_list[folderIncrement]
        print(f'Checking ROI on {currentFolder}...')
        image_list = os.listdir(f'./images/{currentFolder}/actual')  # get the name of all the image files in the folder

        while imageIncrement < len(image_list):
            img = cv2.imread(f'./images/{currentFolder}/actual/{image_list[imageIncrement]}')
            cut_image = img[400:770, 470:1270]  # cropped image to ROI

            # openCV use BGR not RGB. Convert to HSV (Hue Saturation Value)
            hsv = cv2.cvtColor(cut_image, cv2.COLOR_BGR2HSV)

            # Determine upper and lower range of gray colour
            lower_gray = np.array([0, 0, 0])
            upper_gray = np.array([255, 10, 255])

            mask = cv2.inRange(hsv, lower_gray, upper_gray)

            # if there are any fish scale (grey) pixels on mask or Fish ID, sum will be > 0
            hasGrey = np.sum(mask)
            if hasGrey <= 0:
                os.remove(f'./images/{currentFolder}/actual/{image_list[imageIncrement]}')
            imageIncrement += 1

        print(f'ROI check on video {currentFolder} complete\n')
        folderIncrement += 1
