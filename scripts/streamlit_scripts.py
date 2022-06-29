import scripts.video_processing as video_processing  # Video processing script
import constant  # Constant Variables

import pandas as pd
from io import StringIO
import numpy as np
import os
import sys
import streamlit as st
import cv2
import time
import asyncio

"""
Function that sends unprocessed videos from input video folder to cache
"""


@st.cache
def load_videos_cache(videos):
    video_files = video_processing.GetVideoNames(constant.videos_location)
    return video_files


def get_video_length(filename):  # Get video length in seconds for progress bar
    vidcapture = cv2.VideoCapture(filename)
    fps = vidcapture.get(cv2.CAP_PROP_FPS)
    totalNoFrames = vidcapture.get(cv2.CAP_PROP_FRAME_COUNT)
    durationInSeconds = int(float(totalNoFrames) / float(fps))
    print("durationInSeconds: ", durationInSeconds, "s")
    return durationInSeconds


def show_progress_bar(video_length, progress_bar):  # Show the progress of the video processing
    for percent_complete in range(100):
        speed = video_length / 100
        time.sleep(speed)
        progress_bar.progress(percent_complete + 1)
