#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''object_detection.py: Module that uses YOLOv4 dnn model to detect objects from given frames
    @Author: "Nicholas Bingei"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)
import scripts.video_processing as video_processing  # Video processing script
import constant  # Constant Variables
import streamlit as st

"""
Function that sends unprocessed videos from input video folder to cache
"""

@st.cache
def load_videos_cache(video_files):
    video_files = video_processing.GetVideoNames(constant.videos_location)
    return video_files

def convert_df(df):
   return df.to_csv().encode('utf-8')
