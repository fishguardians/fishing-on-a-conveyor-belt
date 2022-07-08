import scripts.video_processing as video_processing  # Video processing script
import constant  # Constant Variables
import streamlit as st

"""
Function that sends unprocessed videos from input video folder to cache
"""

# @st.cache
def load_videos_cache(video_files):
    video_files = video_processing.GetVideoNames(constant.videos_location)
    return video_files

@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')
