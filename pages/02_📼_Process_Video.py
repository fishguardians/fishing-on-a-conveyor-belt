import scripts.video_processing as video_processing  # Video processing scripts
import scripts.streamlit_scripts as st_scripts  # Custom streamlit scripts
import constant  # Constant Variables
import streamlit as st
import os
import glob
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid
from itertools import count

# Page Configs

st.set_page_config(
    page_title="Process Video",
    page_icon="📼",
)

# Page Sidebar
st.sidebar.success("Select a demo above.")  # Page Sidebar
st.write('# 📼 Process Video 📼')  # Page Title

# Session State Initialization
st.write('###')  # Line break
st.write('🐛 For Debugging 🐛', st.session_state)  # Displays session states
if 'bool_have_videos' not in st.session_state:  # Bool to state whether there are videos in folder
    st.session_state.bool_have_videos = False
if 'bool_start_processing' not in st.session_state:  # Bool to state whether video processing has started
    st.session_state.bool_start_processing = False

# Page Main Contents
st.write('###')  # Line break
st.markdown("""
### :one: Quick start guide:
1. Please prepare the videos on your computer
2. Transfer the videos into the 'videos' folder of the application
3. If its currently empty, it will show instructions on how to do it
4. When videos are inside, you can watch the preview of the videos
5. Once you're ready to go hit the 'Start Processing Videos' button
""")

st.write('###')
st.markdown('### :two: Processing videos from file location...')

# Initialize variables
video_files = video_processing.GetVideoNames(constant.videos_location)
cached_videos = st_scripts.load_videos_cache(video_files)  # Gets the data from cache for quick processing
num_of_unprocessed_videos = st.empty()
video_title = st.empty()
video_player = st.empty()
start_button = st.empty()
video_processing_warning = st.empty()
video_processing_window = st.empty()

ballooned = False
processing_complete = False

# Checks for number of videos currently
# If no videos inside 'videos' folder, prompt user to transfer some
if len(cached_videos) == 0:
    st.error("""Video folder is currently **empty!**""")
    st.error("""Please transfer video file(s) to the 'videos' folder of the application.""")
    st.image('pages/assets/transfer_video_instructions.jpg')
    st.write("""As illustrated in the picture above.""")

else:
    # Show the button to start video phenotyping process
    num_of_unprocessed_videos = st.markdown('Number of unprocessed videos: ' + str(len(cached_videos)) + '\n')
    st.session_state.bool_have_videos = True
    if start_button.button("Start Processing Videos"):
        video_processing_warning = st.warning("Video processing started")
        num_of_unprocessed_videos.empty()
        start_button.empty()  # Remove the button once processing has started
        st.session_state.bool_start_processing = True

    # For each video, display it and write the name belowqq
    for v in cached_videos:
        video_name = f"""<style> p.a {{font: bold 1rem Source Sans Pro;}}</style> <p class="a">{v}</p>"""
        st.write('###')
        video_title = st.markdown(video_name, unsafe_allow_html=True)
        v = './videos/' + v
        video_file = open(v, 'rb')
        video = video_file.read()
        video_player = st.video(video)
        st.write('###')

# Video processing begins
if st.session_state.bool_start_processing:
    video_player.empty()
    processing_complete = video_processing.CaptureImagesOnVideo(cached_videos)

# Video Processing KPIs
# create three columns
# kpi1, kpi2, kpi3 = st.columns(3)
#
# # fill in those three columns with respective metrics or KPIs
# kpi1.metric(
#     label="Processing Percentage ⏳",
#     # value=f"{round(percentage)}%",
#     # delta=round(avg_age) - 10,
# )
#
# kpi2.metric(
#     label="Fish Caught 🎣",
#     # value=int(x),
#     # delta=-10 + count_married,
# )
#
# kpi3.metric(
#     label=" ＄",
#     # value=f"{round(x)} ",
#     # delta=-round(balance / count_married) * 100,
# )


# If video processing is done
if processing_complete:
    video_processing_warning.empty()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    st.success("Video processing complete at " + current_time)

    if not ballooned:
        for i in count():
            if i == 0:
                st.balloons()
                ballooned = True
                break

    st.write('###')  # Line break
    st.markdown("""
    ### :three: After processing:
    1. You can download the output CSV with the fish's ID, weight and dimensions (length and depth).
    2. Or go over to the Data Visualization page to view graphs and charts with the newly processed data.
    """)

    # Create table on the GUI
    os.chdir('output')
    file_list = glob.glob('*/**.csv')
    print('file_list: ', file_list)

    if len(file_list) == 0:
        st.error(""" Output CSV data folder is currently empty!""")

    else:
        try:
            option = st.selectbox(
                'Which CSV file would you like to view?',
                file_list)

            df = pd.read_csv(f"{option}")
            df = df.drop(columns=['frame', 'hypotenuse'])
            csv = st_scripts.convert_df(df)

            AgGrid(df)

            st.download_button(
                "Press to Download",
                csv,
                "text.csv",
                "text/csv",
                key='download-csv'
            )

        except:
            st.text("This file is not a CSV file!")


# st.write('###')
# st.markdown('### Upload video to start processing')
# uploaded_video = st.file_uploader("Choose a file")
# if uploaded_video is not None:
#     # To read file as bytes:
#     bytes_data = uploaded_video.getvalue()
#     st.write(bytes_data)
#     # To convert to a string based IO:
#     stringio = StringIO(uploaded_video.getvalue().decode("utf-8"))
#     st.write(stringio)
#     # To read file as string:
#     string_data = stringio.read()
#     st.write(string_data)
#     # Can be used wherever a "file-like" object is accepted:
#     dataframe = pd.read_csv(uploaded_video)
#     st.write(dataframe)
# st.video(uploaded_video)
# st.write('###')
#
# if "shared" not in st.session_state:
#     st.session_state["shared"] = True
