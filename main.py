#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''main.py: Main module that runs the fish phenotyping process
    @Author: "Muhammad Abdurraheem, Chen Dong, Nicholas Bingei, Yao YuJing and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)
import time
import reset_folders
print('Checking if file are corrupted...')
reset_folders.reset_folders()

import scripts.video_processing as video_processing
import scripts.generate_csv as generate_csv
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

    start = time.perf_counter()  # To measure time taken to complete video processing

    print(
        """\nFishing on a Conveyor Belt \nAn integrative team project done by students of SIT \nIn collaboration with James Cook University\n""")

    print('Checking if file are corrupted...')
    reset_folders.reset_folders()

    print('Retrieving file names from "videos" folder...')
    video_files = video_processing.GetVideoNames(constant.videos_location)
    print('Files: ' + str(video_files) + '\n')

    print('Unprocessed videos found: ' + str(len(video_files)) + '\n')
    video_processing.CaptureImagesOnVideo(video_files)
    response = generate_csv.WriteDataOutput(video_files)

    print('Is files able to generate? :'+ response)
    
    print("End of video image capture process: ", current_time)

    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} seconds(s)')

if __name__ == "__main__":
    main()
    
