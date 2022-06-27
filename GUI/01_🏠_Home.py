#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''gui.py: The Graphical user interface of the application. Built on Streamlit app framework.
    @Author: "Nicholas Bingei"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)

"""
Run this line:
streamlit run .\GUI\01_🏠_Home.py
"""

import streamlit as st

st.set_page_config(
    page_title="Fishing on a Conveyor Belt",
    page_icon="🎣",
)

st.write("# 🎣 Welcome to Fishing on a Conveyor Belt 🐟")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Fishing on a Conveyor Belt is a web application that automates data collection from
    a conveyor belt fish phenotyping station.
    
    **👈 Select a demo from the sidebar** to see some explore what the app can do!
    
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
        
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)
