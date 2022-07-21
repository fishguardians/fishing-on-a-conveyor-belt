import scripts.video_processing as video_processing  # Video processing scripts
import scripts.streamlit_scripts as st_scripts  # Custom streamlit scripts
from scripts.object_detection import ObjectDetection
import constant  # Constant Variables
import streamlit as st
import time
import glob
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid
from itertools import count
import os.path


# Page Configs
st.set_page_config(
    page_title="Process Video",
    page_icon="📼",
)

# Page Sidebar
st.write('# 📼 Process Video 📼')  # Page Title
st.sidebar.info("This page allows you to process the fish phenotyping conveyor belt video recordings")

# Session State Initialization
# st.write('###')  # Line break
# st.write('🐛 For Debugging 🐛', st.session_state)  # Displays session states
if 'bool_have_videos' not in st.session_state:  # Bool to state whether there are videos in folder
    st.session_state.bool_have_videos = False
if 'bool_start_processing' not in st.session_state:  # Bool to state whether video processing has started
    st.session_state.bool_start_processing = False
if 'bool_process_clicked' not in st.session_state:  # Bool to state whether video processing has started
    st.session_state.bool_process_clicked = False
if 'bool_balloons' not in st.session_state:  # Bool to state whether video processing success balloons has been shown
    st.session_state.bool_balloons = False

# Initialize variables
video_files = video_processing.GetVideoNames(constant.videos_location)
num_of_unprocessed_videos = st.empty()
video_title = st.empty()
video_player = st.empty()
video_processing_warning = st.empty()
video_processing_window = st.empty()
fish_species_radio_button = st.empty()
part1 = st.empty()  # Quick start guide section
part2 = st.empty()  # Processing videos from file location
part3 = st.empty()  # After video processing

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
if len(video_files) == 0 and not st.session_state.bool_process_clicked:
    part1.write('###')  # Line break
    part1.warning("""The video folder is currently **empty!**""")
    part1.warning(
        """
        \n Transfer the video(s) to the **'videos'** directory of the program. As illustrated the image below.
        """)
    part1.image('pages/assets/transfer_video_instructions.jpg')

part1.write('###')  # Line break
# End of 1️⃣ Quick start guide section


if st.session_state.bool_process_clicked:
    st.session_state.bool_process_clicked = True  # preserve the info that you hit a button between runs

    st.write('###')
    st.markdown('### :two: Processing videos from file location:')
    st.warning('If you are seeing this, that means you have reached the end of processing the videos. \n'
               '\nPlease feel free to continue to view, edit or download the output data.')

    st.write('###')  # Line break
    st.markdown("""
                ### :three: After processing:
                1. You can download the output CSV with the fish's ID, weight and dimensions (length and depth).
                2. Or go over to the Data Visualization page to view graphs and charts with the newly processed data.
                3. Lastly if you would like to process more videos, please refresh the page or hit **'F5'** key to restart the application.
                """)
    st.write('###')  # Line break

    # Create table on the GUI
    # os.chdir('./results')
    file_list = glob.glob('results/**.csv')
    print('file_list: ', file_list)

    if len(file_list) == 0:
        st.error(""" Results CSV data folder is currently empty!""")

    else:
        try:
            option = st.selectbox(
                'Which CSV file would you like to view?',
                file_list)

            df = pd.read_csv(f"{option}")
            csv = st_scripts.convert_df(df)
            file_name = (str(option[0: option.index(".")]) + '.csv')
            AgGrid(df)

            st.download_button(
                "Press to Download",
                csv,
                file_name,
                "text/csv",
                key='download-csv'
            )

        except:
            st.warning("This file is not a CSV file!")

else:
    # Start of 2️⃣ Processing videos from file location
    if len(video_files) != 0:

        part2 = st.container()
        part2.write('###')
        part2.markdown('### :two: Processing videos from file location:')

        # Show the button to start video phenotyping process
        num_of_unprocessed_videos = part2.markdown('Number of unprocessed videos: ' + str(len(video_files)) + '\n')
        st.session_state.bool_have_videos = True

        for video_name in video_files:
            __file__ = f"videos\\{video_name}"
            part2.markdown(f"{video_name} created on  : {time.ctime(os.path.getctime(__file__))}")

        # For each video, display it and its name
        for v in video_files:
            video_name = f"""<style> p.a {{font: bold 1rem Source Sans Pro;}}</style> <p class="a">{v}</p>"""
            part2.write('###')
            part2.markdown(video_name, unsafe_allow_html=True)
            v = './videos/' + v
            video_file = open(v, 'rb')
            video = video_file.read()
            part2.video(video)
            part2.write('###')

        videos_container = st.empty()
        start_button = st.empty()

        # st.warning("Currently the software does not support detection of the fish species. As young red snappers "
        #            "have slightly transparent tails, please make that selection as it requires a different model
        #            to process that fish")

        # fish_species_radio_button = st.radio(
        #     "Which fish species does the video have?",
        #     ('Default', 'Baby Red Snapper'))

        # if fish_species_radio_button == 'Barramundi':
        #     st.write('Barramundi selected.')
        # else:
        #     st.write("Baby Red Snapper selected.")

        # Create start video processing button
        isclicked = start_button.button("Start Processing Videos")
        if isclicked:
            st.session_state.bool_start_processing = True
            st.session_state.bool_process_clicked = True
            start_button.empty()
            num_of_unprocessed_videos.empty()
            videos_container = st.empty()

            # Video processing begins
            od = ObjectDetection()  # Initialize Object Detection
            video_processing_warning = part2.warning("**Video processing started...**")
            time.sleep(0.2)
            part2.write('###')  # Line break
            video_processing_warning.empty()
            processing_complete = video_processing.CaptureImagesOnVideo(video_files, od)
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
            3. Lastly if you would like to process more videos, please refresh the page or hit **'F5'** key to restart the application.
            """)
        part3.write('###')  # Line break

        # Create table on the GUI
        # os.chdir('./results')
        file_list = glob.glob('results/**.csv')
        print('file_list: ', file_list)

        if len(file_list) == 0:
            part3.error(""" Results CSV data folder is currently empty!""")

        else:
            try:
                option = part3.selectbox(
                    'Which CSV file would you like to view?',
                    file_list)

                df = pd.read_csv(f"{option}")
                csv = st_scripts.convert_df(df)
                file_name = (str(option[0: option.index(".")]) + '.csv')
                AgGrid(df)

                # TODO: Make the tables editable

                # df = pd.read_csv(f"{option}")
                # grid_return = AgGrid(df, editable=True)
                # new_df = grid_return['data']
                # AgGrid(new_df)
                #
                # csv = st_scripts.convert_df(new_df)
                # file_name = (str(new_df) + '.csv')

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
