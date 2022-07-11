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
"""
)
