#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''camera.py: Video capture module that takes the images of the fish
    @Author: "Muhammad Abdurraheem and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
#import if necessary (built-in, third-party, path, own modules)
import os
import shutil
import cv2 
import glob
import random
import math
import numpy as np
import constant
# from threading import Thread

from object_detection import ObjectDetection
# Initialize Object Detection
od = ObjectDetection()

def GetVideoNames():
    """ # 1 - directory of stored videos """
    folder = os.listdir(constant.videos_location)
    videos_to_be_processed = []

    for file in folder:
        _, file_extension = os.path.splitext(file)

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
    # use to capture 1 frame per second
    _skip_frames = 0
    # use for naming frames 
    _frame_index = 0
    # check for smallest distance
    hypothesis = 50
    for index, _video_name in enumerate(videos_to_be_processed):
        print('Processing video ' + str(index+1) + '...\n')
        
        cap = cv2.VideoCapture(constant.videos_location+_video_name)

        if (cap.isOpened()== False):
            print("Error opening video stream or file")

        while (cap.isOpened()):
            ret, frame = cap.read()
            # width = int(cap.get(3)) # 1920p
            # height = int(cap.get(4)) # 1080p
            
            # when stream ends
            if not ret:
                MoveVideo(_video_name)
                print(f'Video {index + 1} process complete.')
                _frame_index = 0
                _skip_frames = 0
                break
            
            # Loading image
            img = cv2.resize(frame, None, fx=0.4, fy=0.4)
            height, width, channels = img.shape
            # center point location of img
            posY = int(height/2)
            posX = int(width/2)

            # Detect objects on frame
            (class_ids, scores, boxes) = od.detect(img)

            # check if can save img
            _center_image = False

            # check if all 3 objects are in the image [fish, id, scale]
            if(len(class_ids)==3):
                for (index, box) in enumerate(boxes):
                    x, y, w, h = box
                    match(class_ids[index]):
                        case 0: # fish
                            # center point of the fish
                            cx = int((x + x + w)/2)
                            cy = int((y+y+h)/2)
                            cv2.rectangle(img, (x, y), (x + w, y + h), constant.fish_color, 2)
                            cv2.circle(img, (cx, cy), 3, (255,0,0), -1)
                            cv2.putText(img, "Fish", (x+w, y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, constant.fish_color, 2)
                            distance = math.hypot(cx - posX, cy - posY)
                            print(distance, hypothesis)
                            
                            # distance lesser than previous distance
                            if (distance < hypothesis):
                                _frame_index += 1
                                _center_image = True
                                # Save the images if fish is close to center point
                                SaveImages(frame, _frame_index, _video_name)
                                hypothesis = distance
                            elif((distance*1.2 < hypothesis) or (distance/1.2 < hypothesis)):
                                continue
                            # reset checker
                            else: 
                                hypothesis = 50
                        case 1: # id
                            cv2.putText(img, "Id", (x+w, y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, constant.id_color, 2)
                            cv2.rectangle(img, (x, y), (x + w, y + h), constant.id_color, 1)
                            print(_center_image)

                            #TODO: Read Fish ID before saving as img

                        case 2: # scale
                            buffer = [20,20,20,20]
                            cv2.rectangle(img, (x - buffer[0], y - buffer[1]), (x + w + buffer[2], y + h + buffer[3]), constant.scale_color, 2)
                            
                        case _:
                            continue
                    
            # View Video
            ViewVideo(_video_name, img)
            
            _skip_frames += 30  # i.e. at 30 fps, this advances one second
            cap.set(1, _skip_frames)
            
            if cv2.waitKey(1) == ord('q'):
                _frame_index = 0
                _skip_frames = 0
                break

        cap.release()
        cv2.destroyAllWindows()










def ViewVideo(name, main_frame):
    """Additional: to see the video while it is processing"""
    height, width, channels = main_frame.shape
    # show center position of image
    cv2.circle(main_frame, (int(width/2), int(height/2)), 3, (0,0,255), -1)
    # display the window
    cv2.imshow(name, main_frame)

def MoveVideo (video):
    """Move the processed videos to completed folder so they will not run again"""
    # check if the directory exists
    if not os.path.exists('completed_videos/' + video):  
        os.makedirs('completed_videos/' + video)
    shutil.move("./videos/"+video, 'completed_videos/' + video, copy_function = shutil.copy2)

def SaveImages(actual_frame, _frame_index, _video_name):
    """Store images function"""
    # check if the directory exists
    if not os.path.exists('images/' + _video_name):  
        os.makedirs('images/' + _video_name + '/actual')
    # write to seperate folders for easier book-keeping
    cv2.imwrite('./images/' + _video_name + '/actual/' + str(_frame_index) + '.jpg',
                actual_frame) 
