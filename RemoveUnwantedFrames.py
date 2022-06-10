import cv2
import os
from pytesseract import pytesseract

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Path of where pytesseract.exe is located

increment = 1
incrementFrame = 0
numVideos = 4
count = 0

while increment <= numVideos:
    count = 0
    incrementFrame = 0
    if not os.path.exists(
            'tank' + str(increment)):  # if data folder does not exist,then make a new directory called data
        os.makedirs('tank' + str(increment))

        cap = cv2.VideoCapture(
            r'C:\Users\rahee\Desktop\Raheem Stuff\SIT Software Engineering\Trimester 2.3 ITP\videos/vid' + str(
                increment) + '.MOV')

        while cap.isOpened():
            ret, frame = cap.read()  # ret is a boolean regarding whether there was a return at all, at the frame is
            # each frame that is returned

            if ret:
                cv2.imwrite('./tank' + str(increment) + '/frame' + str(incrementFrame) + '.jpg',
                            frame)  # save image in data folder
                count += 30  # i.e. at 30 fps, this advances one second

                img = cv2.imread('./tank' + str(increment) + '/frame' + str(incrementFrame) + '.jpg')
                words_in_image = pytesseract.image_to_string(img)
                array = words_in_image.split()
                print(array)

                if "Fish" not in array:
                    os.remove('./tank' + str(increment) + '/frame' + str(incrementFrame) + '.jpg')

                incrementFrame += 1
                cap.set(1, count)
            else:
                increment += 1
                incrementFrame = 0
                break




