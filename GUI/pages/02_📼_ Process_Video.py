import streamlit as st
import pandas as pd
from io import StringIO
import numpy as np

# Page Configs
st.set_page_config(
    page_title="Process Video",
    page_icon="📼",
)

# Page Sidebar
st.sidebar.success("Select a demo above.")

# Page Title
st.write('# 📼 Process Video 📼')

# Line break
st.write('###')

st.markdown("""
### There are 2 methods of processing the video.
1. Processing the videos locally (Recommended)
2. Processing the videos online via server
""")

st.write('###')

st.markdown('### Upload video to start processing')

uploaded_video = st.file_uploader("Choose a file")
if uploaded_video is not None:
    # To read file as bytes:
    bytes_data = uploaded_video.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_video.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_video)
    st.write(dataframe)

st.video(uploaded_video)

st.write('###')

# TODO: Integrate imagecapture.py to Streamlit

st.markdown(
    """
Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard 
dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen 
book.
"""
)

if "shared" not in st.session_state:
    st.session_state["shared"] = True
