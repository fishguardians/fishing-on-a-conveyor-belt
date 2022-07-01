import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="About",
    page_icon="🐠",
)

st.write('# 🐠 About 🐠')

st.sidebar.success("Select a demo above.")

st.markdown(
    """
Fishing on a Conveyor Belt. An integrative team project done by students of Singapore Institute of Technology.
In collaboration with James Cook University (Singapore).
"""
)

st.write("***") # Horizontal line in Markdown
