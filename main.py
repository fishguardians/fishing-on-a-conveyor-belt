#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''main.py: Main module that runs the fish phenotyping process
    @Author: "Muhammad Abdurraheem, Chen Dong, Nicholas Bingei, Yao YuJing and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)

import scripts.video_processing as video_processing
import constant

from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

video_files = []


def main():
    """
    Main Start Function to execute the scripts
    TODO: *Include more documentation*
    """
    print("""\nFishing on a Conveyor Belt \nAn integrative team project done by students of SIT \nIn collaboration with James Cook University\n""")
    
    print('Retrieving file names from "videos" folder...')
    video_files = video_processing.GetVideoNames(constant.videos_location)
    print('Files: ' + str(video_files) +'\n')

    
    print('Unprocessed videos found: '+str(len(video_files))+'\n')
    video_processing.CaptureImagesOnVideo(video_files)
    
    print("End of video image capture process: ", current_time)

if __name__ == "__main__":
    main()
