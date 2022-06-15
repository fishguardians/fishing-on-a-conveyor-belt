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
import numpy as np
import constant
# from threading import Thread

# Load Yolo
net = cv2.dnn.readNet("yolov3_training_last.weights", "yolov3.cfg")

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(3, 3))

classes = ["Barramundi","Id","Scale"]

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
            
            # ViewVideo(_video_name, frame)
            # TODO: Check for the fish centered before saving
            DetectFish(frame)

            #TODO: Check Fish ID
            # CheckFishID()

            # SaveImages(frame, _frame_index, video)
            
            _frame_index += 1
            _skip_frames += 30  # i.e. at 30 fps, this advances one second
            cap.set(1, _skip_frames)
            
            if cv2.waitKey(1) == ord('q'):
                _frame_index = 0
                _skip_frames = 0
                break

        cap.release()
        cv2.destroyAllWindows()

def ViewVideo(name, actual_frame):
    """Additional: to see the video while it is processing"""
    main_frame = cv2.resize(actual_frame, None, fx=0.4, fy=0.4)
    # display the window
    cv2.imshow(name, main_frame)

def DetectFish(img):
    # Loading image
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Object detected
                print(class_id)
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    print(indexes)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(constant.classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 2)
            #center point of the frame
            cx = int((x + x + w)/2)
            cy = int((y+y+h)/2)
            cv2.circle(img, (cx, cy), 3, (255,0,0))

    #(width, height)
    cv2.line(img, (0, int(height/2)), (width, int(height/2)), (0,0,255), 2)
    cv2.line(img, (int(width/2), 0), (int(width/2), height), (0,0,255), 2)
    cv2.imshow("Image", img)
#     key = cv2.waitKey(0)
# cv2.destroyAllWindows()


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
