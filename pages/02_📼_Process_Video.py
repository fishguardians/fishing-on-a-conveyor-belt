import scripts.video_processing as video_processing  # Video processing scripts
import scripts.streamlit_scripts as st_scripts  # Custom streamlit scripts
from scripts.object_detection import ObjectDetection
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

try:

    # Session State Initialization
    # st.write('###')  # Line break
    # st.write('🐛 For Debugging 🐛', st.session_state)  # Displays session states
    if 'bool_have_videos' not in st.session_state:  # Bool to state whether there are videos in folder
        st.session_state.bool_have_videos = False
    if 'bool_start_processing' not in st.session_state:  # Bool to state whether video processing has started
        st.session_state.bool_start_processing = False

    # Initialize variables
    video_files = video_processing.GetVideoNames(constant.videos_location)
    cached_videos = st_scripts.load_videos_cache(video_files)  # Gets the data from cache for quick processing
    num_of_unprocessed_videos = st.empty()
    video_title = st.empty()
    video_player = st.empty()
    video_processing_warning = st.empty()
    video_processing_window = st.empty()

    ballooned = False
    processing_complete = False

    # Main Page Contents


    # Start of 1️⃣ Quick start guide section
    part1 = st.expander("Expand or Collapse", True)

    part1.write('###')  # Line break
    part1.markdown("""
        ### :one: Quick start guide:
        1. Please prepare the videos on your computer.
        2. Transfer the videos into the 'videos' folder of the application.
        3. Once your done, press the **'R'** key to refresh the app.
        4. You can then watch the preview of the video(s).
        5. Once you're ready to go hit the 'Start Processing Videos' button!
        """)

    # Checks for number of videos currently
    # If no videos inside 'videos' folder, prompt user to transfer some
    if len(cached_videos) == 0:
        part1.warning("""The video folder is currently **empty!**""")
        part1.warning(
            """
            \n Transfer the video(s) to the **'videos'** directory of the program. As illustrated the image below.
            """)
        part1.image('pages/assets/transfer_video_instructions.jpg')

    part1.write('###')  # Line break
    # End of 1️⃣ Quick start guide section


    # Start of 2️⃣ Processing videos from file location
    if len(cached_videos) != 0:

        part2 = st.container()
        part2.write('###')
        part2.markdown('### :two: Processing videos from file location:')

        # Show the button to start video phenotyping process
        num_of_unprocessed_videos = part2.markdown('Number of unprocessed videos: ' + str(len(cached_videos)) + '\n')
        st.session_state.bool_have_videos = True

        # For each video, display it and its name
        for v in cached_videos:
            video_name = f"""<style> p.a {{font: bold 1rem Source Sans Pro;}}</style> <p class="a">{v}</p>"""
            part2.write('###')
            video_title = part2.markdown(video_name, unsafe_allow_html=True)
            v = './videos/' + v
            video_file = open(v, 'rb')
            video = video_file.read()
            video_player = part2.video(video)
            part2.write('###')

    start_button = part2.empty()
    # Create start video processing button
    isclicked = start_button.button("Start Processing Videos")
    if isclicked:
        st.session_state.bool_start_processing = True
        start_button.empty()
        video_player.empty()
        num_of_unprocessed_videos.empty()

        # Video processing begins
        video_processing_warning = part2.warning("Video processing started...")
        od = ObjectDetection()  # Initialize Object Detection
        processing_complete = video_processing.CaptureImagesOnVideo(cached_videos, od)
    # End of 2️⃣ Processing videos from file location


    # Start of 3️⃣ After processing:

    # If video processing is done
    part3 = st.container()
    if processing_complete:
        st.session_state.bool_start_processing = False
        video_processing_warning.empty()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        part3.success("Video processing complete at " + current_time)

        if not ballooned:
            for i in count():
                if i == 0:
                    st.balloons()
                    ballooned = True
                    break

        part3.write('###')  # Line break
        part3.markdown("""
        ### :three: After processing:
        1. You can download the output CSV with the fish's ID, weight and dimensions (length and depth).
        2. Or go over to the Data Visualization page to view graphs and charts with the newly processed data.
        """)

        # Create table on the GUI
        os.chdir('output')
        file_list = glob.glob('*/**.csv')
        print('file_list: ', file_list)

        if len(file_list) == 0:
            part3.error(""" Output CSV data folder is currently empty!""")

        else:
            try:
                option = part3.selectbox(
                    'Which CSV file would you like to view?',
                    file_list)

                df = pd.read_csv(f"{option}")
                df = df.drop(columns=['frame', 'hypotenuse'])
                csv = st_scripts.convert_df(df)

                file_name = (str(option[0: option.index(".")]) + '.csv')

                AgGrid(df)

                part3.download_button(
                    "Press to Download",
                    csv,
                    file_name,
                    "text/csv",
                    key='download-csv'
                )

            except:
                part3.warning("This file is not a CSV file!")
    # End of 3️⃣  After processing

except Exception as e:
    print('Exception as e: ', e)
