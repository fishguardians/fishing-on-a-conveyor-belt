#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''camera.py: Video capture module that takes the images of the fish
    @Author: "Muhammad Abdurraheem and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)
import os
import shutil
import csv
import cv2
from pytesseract import pytesseract
import glob
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import constant
# from threading import Thread

# Fish Dimension modules
import scripts._1_fish_crop_belt_image as cropBelt  # Blacks out all parts of the image apart from the belt
import \
    scripts._2_fish_remove_background as removeBg  # Removes the colour of the belt, leaving intented objects for measurement
import scripts._3_fish_measure_dimensions as getDimensions  # Get dimensions of Fish based on length of reference object

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"  # Path of where pytesseract.exe is located

# Read the scale
# from digit_recognization import digit_recognization
from digit_recognition import digit_recognition

from object_detection import ObjectDetection

# Initialize Object Detection
od = ObjectDetection()


def GetVideoNames():
    """ # 1 - directory of stored videos """

    folder = os.listdir(constant.videos_location)
    videos_to_be_processed = []

    for file in folder:
        _, file_extension = os.path.splitext(file)
        # Add required txt files
        if (file != '.gitignore'):
            with open('output/' + file + '-images.txt', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(['#', 'Fish#', 'Frame', 'Hypothenuse'])
            with open('output/' + file + '-dimensions.txt', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(['#', 'Fish#', 'Frame', 'Length', 'Depth'])
            with open('output/' + file + '-id.txt', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header
                writer.writerow(['#', 'Fish#', 'Frame', 'Value'])
        match file_extension.lower():
            case '.mov':
                videos_to_be_processed.append(file.lower())
            case '.mp4':
                videos_to_be_processed.append(file.lower())
            case _:
                continue
    return videos_to_be_processed


def CaptureImagesOnVideo(videos_to_be_processed):
    """# 2 - Process the videos [batch processing]"""
    # check for smallest distance
    hypo_threshold = 70
    # center points curr
    prev_center_pts = []
    # check if last 3 frames has a fish
    check_empty = 0
    # allocate the id for the fish
    wells_id = 0
    id_name = ""

    for index, _video_name in enumerate(videos_to_be_processed):
        print('Processing video ' + str(index + 1) + '...\n')
        # use to capture 1 frame per second
        _skip_frames = 0
        # use for naming frames in case id cannot be detected
        _frame_index = 0
        # ids for tracking in txt files
        _fish_id = 0
        _id_id = 0
        _scale_id = 0

        cap = cv2.VideoCapture(constant.videos_location + _video_name)

        if (cap.isOpened() == False):
            print("Error opening video stream or file")

        while (cap.isOpened()):
            ret, frame = cap.read()

            # exact frame counts
            _frame_index += 1

            # when stream ends
            if not ret:
                cap.release()
                MoveVideo(_video_name)
                print(f'Video {index + 1} process complete.')
                break

            # Loading image
            img = frame.copy()  # 1080 1920 original image
            img = cv2.resize(img, None, fx=0.4, fy=0.4)

            og_img = frame.copy()

            # Width & Height of img
            height, width, channels = img.shape
            # center point location of img
            posY = int(height / 2)
            posX = int(width / 2)

            # display location of objects
            fish_coords = []
            fish_center_coords = []
            id_coords = []
            scale_coords = []

            # Detect objects on frame
            (class_ids, scores, boxes) = od.detect(img)

            # check if can save img
            _has_image = False
            _has_id = False

            print(class_ids)

            for (index, box) in enumerate(boxes):
                x, y, w, h = box

                # check if all 3 objects are in the image [fish, id, scale]
                match class_ids[index]:
                    case 1:  # Fish
                        fish_coords = box
                        # center point of the fish
                        cx = int((x + x + w) / 2)
                        cy = int((y + y + h) / 2)
                        fish_center_coords.append((cx, cy))

                        hypothenuse = round(math.hypot(cx - posX, cy - posY))
                        # print(hypothenuse, hypo_threshold)

                        # distance lesser than previous distance
                        if (hypothenuse < hypo_threshold):
                            _fish_id += 1
                            hypo_threshold = hypothenuse
                            _has_image = True

                            # TODO: Run fish dimension function (Nicholas)


                            print('Running fish image processing functions')

                            """
                            frame - for original frame in the video
                            removeBg
                            getDimensions
                            """

                            # 1. Run cropBelt function to black out all but the belt in the image
                            cropBelt_output_img = cropBelt.crop_belt(frame)

                            # 2. Run removeBackground function to remove yellow belt colour and water reflections
                            removeBg_output_img = removeBg.remove_background(cropBelt_output_img)

                            # 3. Run getDimensions function to get measurements of fish (E.g. Barramundi and Snapper)
                            fish_length, fish_depth = getDimensions.get_dimensions(removeBg_output_img, og_img)

                            # open the file to write
                            with open('output/' + _video_name + '-dimensions.txt', 'a', encoding='UTF8') as f:
                                writer = csv.writer(f)
                                # write the header

                                """
                                '#' - fish_id is the # unique key for the data
                                'Fish#' - current num of fish that's passing through the conveyor belt
                                'Frame' - the num value of the frame of the video image taken
                                'Length' - length of the fish (From head to tail)
                                'Depth' - the length of the depth of the fish (Widest point of the fish)
                                """
                                # writer.writerow(['#', 'Fish#', 'Frame', 'Length', 'Depth'])
                                writer.writerow([_fish_id, wells_id, _frame_index, fish_length, fish_depth])

                            SaveImages(frame, _frame_index, _video_name, 'fish')
                            # open the file to write
                            with open('output/' + _video_name + '-images.txt', 'a', encoding='UTF8') as f:
                                # create the csv writer
                                writer = csv.writer(f)

                                """
                                '_fish_id' - fish_id is the # unique key for the data
                                'wells_id' - current num of fish that's passing through the conveyor belt
                                '_frame_index' - the num value of the frame of the video image taken
                                'hypotenuse' - the point where the fish is detected?
                                """
                                writer.writerow([_fish_id, wells_id, _frame_index, hypothenuse])

                        # reset checker
                        else:
                            hypo_threshold = 70  # Try to another fish that is closer

                    case 0:  # Id
                        id_coords = box
                        _id_id += 1
                        # TODO: Read Fish ID before saving as img
                        _has_id = True

                        id_image = img.copy()
                        id_image = id_image[y:y + h, x:x + w]
                        # id_image = cv2.resize(id_image, None, fx=4, fy=4)
                        id_image = cv2.cvtColor(id_image, cv2.COLOR_BGR2GRAY)  # convert from GBR to RGB
                        id_image = cv2.rotate(id_image, cv2.ROTATE_90_COUNTERCLOCKWISE)  # change orientation
                        cv2.imshow("test_id", id_image)
                        id_image = cv2.bilateralFilter(id_image, 5, 30, 60)
                        # edged = cv2.Canny(id_image, 30, 200)
                        # thresholding = cv2.threshold(id_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                        kernel = np.ones((5, 5), np.uint8)
                        opening = cv2.morphologyEx(id_image, cv2.MORPH_OPEN, kernel)
                        # cv2.imshow("test", opening)
                        words = pytesseract.image_to_string(opening)
                        print(words)
                        text = pytesseract.image_to_string(opening, \
                                                           config='-l eng --psm 9 --oem 3 -c tessedit_char_whitelist="' + constant.tess_whitelist + '" tessedit_char_blacklist="' + constant.tess_blacklist + '"')
                        edited = ''.join(char for char in text if char.isalnum())
                        # print(edited)
                        SaveImages(id_image, _frame_index, _video_name, 'id')

                        # open the file to write
                        with open('output/' + _video_name + '-id.txt', 'a', encoding='UTF8') as f:
                            # create the csv writer
                            writer = csv.writer(f)
                            # ['#', 'Fish#', 'Frame', 'Value', 'x', 'y', 'w', 'h']
                            writer.writerow([_id_id, wells_id, _frame_index, edited])

                    case 2:  # scale
                        _scale_id += 1
                        scale_coords = box

                        ###
                        # Test Contours
                        ###
                        scale_image = img.copy()
                        scale_image = scale_image[y - 10:y + h + 10, x - 10:x + w + 10]
                        scale_image = cv2.resize(scale_image, None, fx=2, fy=2)
                        saveCopy = scale_image.copy()

                        scale_image = cv2.cvtColor(scale_image, cv2.COLOR_BGR2HSV)
                        GRAY_MIN = np.array([90, 8, 37], np.uint8)
                        GRAY_MAX = np.array([105, 255, 255], np.uint8)

                        frame_threshed = cv2.inRange(scale_image, GRAY_MIN, GRAY_MAX)
                        output = cv2.bitwise_and(scale_image, scale_image, mask=frame_threshed)
                        ret, thresh = cv2.threshold(frame_threshed, 40, 255, 0)  # For shadows
                        if (int(cv2.__version__[0]) > 3):
                            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                        else:
                            im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                                                        cv2.CHAIN_APPROX_NONE)

                        if len(contours) != 0:
                            # draw in blue the contours that were founded
                            cv2.drawContours(output, contours, -1, 255, 3)

                            # find the biggest countour (c) by the area
                            c = max(contours, key=cv2.contourArea)
                            x, y, w, h = cv2.boundingRect(c)

                            # draw the biggest contour (c) in green
                            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)

                            saveCopy = saveCopy[y:y + h, x:x + w]
                            if (_has_image == True):
                                SaveImages(saveCopy, _frame_index, _video_name, 'scale')

                        # show the images
                        # cv2.imshow("Result", np.hstack([scale_image, output]))

                        # cv2.waitKey(0)

                        # img1 = cv2.imread('template/1segment.png',1)          # queryImage

                        # # Initiate SIFT detector
                        # orb = cv2.ORB()

                        # # find the keypoints and descriptors with SIFT
                        # kp1, des1 = orb.detectAndCompute(img1,None)
                        # kp2, des2 = orb.detectAndCompute(saveCopy,None)

                        # # create BFMatcher object
                        # bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

                        # # Match descriptors.
                        # matches = bf.match(des1,des2)

                        # # Sort them in the order of their distance.
                        # matches = sorted(matches, key = lambda x:x.distance)

                        # # Draw first 10 matches.
                        # img3 = cv2.drawMatches(img1,kp1,saveCopy,kp2,matches[:10], flags=2)

                        # plt.imshow(img3),plt.show()

                        ###
                        # BGR
                        ###

                        # scale_image = img.copy()
                        # scale_image = scale_image[y-10:y+h+10,x-10:x+w+10]
                        # scale_image = cv2.resize(scale_image, None, fx=2, fy=2)

                        # # grey boundary
                        # lower = [80,70,60]
                        # upper = [100,90,80]

                        # # arrays
                        # lower = np.array(lower, dtype="uint8")
                        # upper = np.array(upper, dtype="uint8")

                        # # find the colors within the specified boundaries and apply
                        # # the mask
                        # mask = cv2.inRange(scale_image, lower, upper)
                        # output = cv2.bitwise_and(scale_image, scale_image, mask=mask)

                        # ret,thresh = cv2.threshold(mask, 40, 255, 0)
                        # if (int(cv2.__version__[0]) > 3):
                        #     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                        # else:
                        #     im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

                        # if len(contours) != 0:
                        #     # draw in blue the contours that were founded
                        #     cv2.drawContours(output, contours, -1, 255, 3)

                        #     # find the biggest countour (c) by the area
                        #     c = max(contours, key = cv2.contourArea)
                        #     x,y,w,h = cv2.boundingRect(c)

                        #     # draw the biggest contour (c) in green
                        #     cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

                        #     saveCopy = scale_image[y:y+h,x:x+w]
                        #     if(_has_image == True):
                        #         SaveImages(saveCopy, _frame_index, _video_name, 'scale')

                        # show the images
                        # cv2.imshow("Result", np.hstack([scale_image, output]))

                        # cv2.waitKey(0)

                        # digit_recognization(frame, y-16, y+h+16, x-16, x+w+16, h, w)
                    case _:
                        continue

            # if(_has_image==True):
            # _scale_id+=1
            # print("images/"+_video_name+"/fish/"+str(_frame_index)+".jpg")
            # scale_reading = digit_recognition("images/"+_video_name+"/fish/"+str(_frame_index)+".jpg")

            # open the file to write
            # with open('output/' + _video_name + '-id.txt', 'a', encoding='UTF8') as f:
            # create the csv writer
            # writer = csv.writer(f)
            # ['#', 'Fish#', 'Frame', 'Value']
            # writer.writerow([_scale_id, wells_id, _frame_index, scale_reading])

            # View Video
            ViewVideo(fish_coords, fish_center_coords, id_coords, scale_coords, _video_name, img)

            if (prev_center_pts == [] and len(fish_center_coords) > 0):
                # check if the previous 3 frames are empty if not it is the same fish
                if (check_empty > 2):
                    check_empty = 0
                    wells_id += 1

            # if there's no fish add the tracker empty by 1
            if (fish_center_coords == []):
                check_empty += 1

            # check the location of fish center points
            prev_center_pts = fish_center_coords.copy()

            _skip_frames += 30  # i.e. at 30 fps, this advances one second
            _frame_index += 30
            cap.set(1, _skip_frames)

            if cv2.waitKey(1) == ord('q'):
                # reset the fish wells_id
                wells_id = 0
                break

        cap.release()
        cv2.destroyAllWindows()


def ViewVideo(fish, fish_center, id, scale, name, img):
    """Additional: to see the video while it is processing"""
    # duplicate image so it doesn't corrupt the original
    main_frame = img.copy()
    height, width, channels = main_frame.shape
    # show objects
    if (len(fish) > 0):
        cv2.rectangle(main_frame, (fish[0], fish[1]), (fish[0] + fish[2], fish[1] + fish[3]), constant.fish_color, 2)
        cv2.circle(main_frame, fish_center[0], 3, constant.fish_color, -1)
        cv2.putText(main_frame, str(fish), (fish[0] + fish[2], fish[1] + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0,
                    constant.fish_color, 2)
    if (len(id) > 0):
        cv2.rectangle(main_frame, (id[0], id[1]), (id[0] + id[2], id[1] + id[3]), constant.id_color, 1)
    if (len(scale) > 0):
        cv2.rectangle(main_frame, (scale[0], scale[1]), (scale[0] + scale[2], scale[1] + scale[3]),
                      constant.scale_color, 2)
    # show center position of image
    # cv2.circle(main_frame, (int(width/2), int(height/2)), 3, (0,0,255), -1)
    cv2.line(main_frame, (0, int(height / 2)), (width, int(height / 2)), (0, 0, 255), 1)
    cv2.line(main_frame, ((int(width / 2), 0)), (int(width / 2), height), (0, 0, 255), 1)

    # display the window
    cv2.imshow(name, main_frame)


def MoveVideo(video):
    """Move the processed videos to completed folder so they will not run again"""
    # check if the directory exists
    if not os.path.exists('completed_videos/' + video):
        os.makedirs('completed_videos/' + video)
    shutil.move("./videos/" + video, 'completed_videos/' + video, copy_function=shutil.copy2)


def SaveImages(actual_frame, _frame_index, _video_name, _type):
    """Store images function"""
    # check if the directory exists
    if not os.path.exists('images/' + _video_name + '/' + _type):
        os.makedirs('images/' + _video_name + '/' + _type)
    # write to seperate folders for easier book-keeping
    cv2.imwrite('./images/' + _video_name + '/' + _type + '/' + str(_frame_index) + '.jpg',
                actual_frame)
