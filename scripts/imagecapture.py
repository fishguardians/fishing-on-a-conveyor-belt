#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''camera.py: Video capture module that takes the images of the fish
    @Author: "Muhammad Abdurraheem and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
#import if necessary (built-in, third-party, path, own modules)
import os
import cv2 
import numpy as np
import constant

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
    # declare frame dimensions and positions to take capture images
    frame_size = constant.frame_dimension
    # use to capture 1 frame per second
    skip_frames = 0
    # use for naming frames 
    frame_index = 0
    for index, video in enumerate(videos_to_be_processed):
        print('Processing video ' + str(index+1) + '...\n')
        
        cap = cv2.VideoCapture(constant.videos_location+video)

        if (cap.isOpened()== False):
            print("Error opening video stream or file")

        while (cap.isOpened()):
            ret, frame = cap.read()
            # width = int(cap.get(3)) # 1920p
            # height = int(cap.get(4)) # 1080p
            
            # when stream ends
            if not ret:
                print(f'Video {index + 1} process complete.')
                frame_index = 0
                break
            
            scale_position = frame[242:650,1600:1720]
            conveyor_position = frame[0:1080, 372:1300]
            id_position = frame[360:640, 560:860]
            # resize the image
            actual_video = cv2.resize(frame, (frame_size[1],frame_size[0]//2)) # same as cv2.resize(frame, (0,0), fy=0.25, fx=0.25)
            # [top:bottom, left:right] layout
            scale = cv2.resize(cv2.rotate(scale_position, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE), (0,0), fy=0.25, fx=0.25)
            conveyor_belt = cv2.resize(conveyor_position, (270,232)) 
            # ruler adjacent to the conveyorbelt [142:1058, 0:1300] #height of 916p = 29cm, therefore avg = 31.59p per cm
            fish_id = cv2.resize(cv2.rotate(id_position, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE), (0,0), fy=0.5, fx=0.5)

            # ViewVideo(frame_size, actual_video, conveyor_belt, scale, fish_id, video)
            # TODO: Check for the highest weight before saving
            # CheckWeight(scale) Function
            SaveImages(actual_video, fish_id, conveyor_belt, scale, frame_index, video)
            
            frame_index += 1
            skip_frames += 30  # i.e. at 30 fps, this advances one second
            cap.set(1, skip_frames)
            
            if cv2.waitKey(1) == ord('q'):
                frame_index = 0
                break

        cap.release()
        cv2.destroyAllWindows()

def ViewVideo(frame_size, actual_video, conveyor_belt, scale, fish_id, video):
    """Additional: to see the video while it is processing"""
    # create a main frame
    main_frame = np.zeros(frame_size, np.uint8)
    # add the items into the main frame
    # top (actual video)
    main_frame[:270, :480] = actual_video
    # bottom-left {conveyor belt}
    main_frame[270:502, :270] = conveyor_belt
    # bottom-middle {scale}
    main_frame[270:300, 270:372] = scale
    # bottom-right {fish_id}
    main_frame[350: 500, 270: 410] = fish_id
    # display the window
    cv2.imshow(video, main_frame)

def SaveImages(actual_video, fish_id, conveyor_belt, scale, frame_index, video):
    """Store images function"""
    # check if the directory exists
    if not os.path.exists('images/' + video):  
        os.makedirs('images/' + video + '/actual')
        os.makedirs('images/' + video + '/id')
        os.makedirs('images/' + video + '/fish')
        os.makedirs('images/' + video + '/weight')
    # write to seperate folders for easier book-keeping
    cv2.imwrite('./images/' + video + '/actual/' + str(frame_index) + '.jpg',
                actual_video) 
    cv2.imwrite('./images/' + video + '/id/' + str(frame_index) + '.jpg',
                fish_id) 
    cv2.imwrite('./images/' + video + '/fish/' + str(frame_index) + '.jpg',
                conveyor_belt) 
    cv2.imwrite('./images/' + video + '/weight/' + str(frame_index) + '.jpg',
                scale)