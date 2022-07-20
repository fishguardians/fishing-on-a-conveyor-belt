#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''main.py: Main module that runs the fish phenotyping process
    @Author: "Muhammad Abdurraheem, Chen Dong, Nicholas Bingei, Yao YuJing and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)

import reset_folders
import streamlit
import sys
from streamlit import cli as stcli
import scripts.video_processing as video_processing
from scripts.object_detection import ObjectDetection
import constant
import streamlit as st

from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

video_files = []


def main():
    """
    Main Start Function to execute the scripts
    TODO: *Include more documentation*
    """
    print(
        """\nFishing on a Conveyor Belt \nAn integrative team project done by students of SIT \nIn collaboration with James Cook University\n""")

    print('Checking if file are corrupted...')
    reset_folders.reset_folders()

    print('Retrieving file names from "videos" folder...')
    video_files = video_processing.GetVideoNames(constant.videos_location)
    print('Files: ' + str(video_files) + '\n')

    print('Unprocessed videos found: ' + str(len(video_files)) + '\n')
    # Initialize Object Detection
    od = ObjectDetection()
    video_processing.CaptureImagesOnVideo(video_files, od)
    
    print("End of video image capture process: ", current_time)


if __name__ == "__main__":
    # main()
    # st.header("Hello world")
    if streamlit._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]] # To auto run
        # sys.argv = ["streamlit", "run", "01_🏠_Home.py"] # Manually click the button to run
        sys.exit(stcli.main())
