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
                #TODO: Move completed video to completed_folder
                # MoveVideo()
                print(f'Video {index + 1} process complete.')
                frame_index = 0
                skip_frames = 0
                break
            
            # [top:bottom, left:right] layout

            # ViewVideo(frame_size, actual_frame, video)
            # TODO: Check for the fish centered before saving
            # CheckFishCentered()

            #TODO: Check Fish ID
            # CheckFishID()

            SaveImages(frame, frame_index, video)
            
            frame_index += 1
            skip_frames += 30  # i.e. at 30 fps, this advances one second
            cap.set(1, skip_frames)
            
            if cv2.waitKey(1) == ord('q'):
                frame_index = 0
                skip_frames = 0
                break

        cap.release()
        cv2.destroyAllWindows()

def ViewVideo(frame_size, actual_frame, video):
    """Additional: to see the video while it is processing"""
    # create a main frame
    main_frame = np.zeros(frame_size, np.uint8)
    # add the items into the main frame
    # top (actual video)
    main_frame[:270, :480] = actual_frame
    # display the window
    cv2.imshow(video, main_frame)

def SaveImages(actual_frame, frame_index, video):
    """Store images function"""
    # check if the directory exists
    if not os.path.exists('images/' + video):  
        os.makedirs('images/' + video + '/actual')
    # write to seperate folders for easier book-keeping
    cv2.imwrite('./images/' + video + '/actual/' + str(frame_index) + '.jpg',
                actual_frame) 
