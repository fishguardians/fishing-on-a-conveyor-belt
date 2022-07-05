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
