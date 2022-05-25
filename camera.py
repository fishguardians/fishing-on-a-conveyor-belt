#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''constant.py: Stores the constant values of the project
    @Author: "Yip Hou Liang"
    @Credit: ["Abdulraheem", "Chen Dong", "Nicholas Binged", "Yao Yujing", "Yip Hou Liang"]'''
#import if necessary (built-in, third-party, path, own modules)
import os
from cv2 import ROTATE_90_COUNTERCLOCKWISE
import numpy as np
import cv2 
import constant

video_files = []

def main():
    """
    Main Process
    TODO: *Include more documentation*
    """
    print("""\nFishing on a Conveyor Belt \nAn integrative team project done by students of SIT \nIn collaboration with James Cook University\n""")

    print('Retrieving file names from "videos" folder...')
    print('Files: ' + str(GetVideoNames()) +'\n')
    video_files = GetVideoNames()

    print('Process videos...\n')
    CaptureImagesOnVideo(video_files)



def GetVideoNames():
    """ # 1 - directory of stored videos """
    folder = os.listdir(constant.videos_location)
    videos_to_be_processed = []

    for file in folder:
        file_name, file_extension = os.path.splitext(file)

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
    for video in videos_to_be_processed:
        cap = cv2.VideoCapture(constant.videos_location+video)

        while True:
            ret, frame = cap.read()
            width = int(cap.get(3)) # 1920p
            height = int(cap.get(4)) # 1080p

            # declare frame dimensions and positions to take capture images
            frame_size = constant.frame_dimension
            scale_position = frame[242:650,1600:1720]
            conveyor_position = frame[0:1080, 372:1300]

            # create a main frame
            main_frame = np.zeros(frame_size, np.uint8)
            
            # resize the image
            actual_video = cv2.resize(frame, (frame_size[1],frame_size[0]//2)) # same as cv2.resize(frame, (0,0), fy=0.25, fx=0.25)
            # [top:bottom, left:right] layout
            scale = cv2.resize(cv2.rotate(scale_position, ROTATE_90_COUNTERCLOCKWISE), (0,0), fy=0.25, fx=0.25)
            conveyor_belt = cv2.resize(conveyor_position, (270,232)) 
            # ruler adjacent to the conveyorbelt [142:1058, 0:1300] #height of 916p = 29cm, therefore avg = 31.59p per cm
            # fish_id = frame[]

            # add the items into the main frame
            # top (actual video)
            main_frame[:270, :480] = actual_video
            # bottom-left (conveyor belt)
            main_frame[270:502, :270] = conveyor_belt
            # bottom-right (scale)
            main_frame[270:300, 270:372] = scale


            cv2.imshow('video processing', main_frame)

            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()



if __name__ == "__main__":
    main()