#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''gui.py: The Graphical user interface of the application. Built on Streamlit app framework.
    @Author: "Nicholas Bingei"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)

# """
# Run this line:
# streamlit run .\GUI\01_🏠_Home.py
# """

import streamlit as st

# Page configuration. Only can be written once. Follows the whole application.
st.set_page_config(
    page_title="Fishing on a Conveyor Belt",
    page_icon="🐠",
)

# Side bar
st.write("# 🎣 Welcome to Fishing on a Conveyor Belt 🐟")
st.sidebar.success("Select a page above!")

# Main page
st.markdown(
    """
    Fishing on a Conveyor Belt is a web application that automates data collection from
    a conveyor belt fish phenotyping station.
    
    **👈 Select a demo from the sidebar** to see some explore what the app can do!
    \n
    **❌ Click the cross icon** on the top right of the sidebar to hide the sidebar.
""")

st.markdown("***")

st.markdown("""##### **Useful Folders in Program's directory:**\n
\n **/completed_videos/** -> Where videos will be transfered to 
after processing. A folder will be created under each video's name, where the video will reside.

\n **/images/** -> Where video frames(images) output during processing are transferred to. Split into 3 parts, 'actual', 'fish' 
and 'id'. 'actual' for the full video frame extracted. 
'fish' for fish image being processed. And 'id' for the id tag being processed.

\n **/results/** -> Where CSVs are output after video processing is completed.

\n **/videos/** -> Where to transfer videos for processing.
""")
