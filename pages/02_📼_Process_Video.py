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
import platform

# Page Configs
st.set_page_config(
    page_title="Process Video",
    page_icon="🐠",
)

# Page Sidebar
st.title('📼 Process Video 📼')  # Page Title
st.sidebar.info("This page allows you to process the fish phenotyping conveyor belt video recordings")

# Session State Initialization
if 'bool_have_videos' not in st.session_state:  # Bool to state whether there are videos in folder
    st.session_state.bool_have_videos = False
if 'bool_start_processing' not in st.session_state:  # Bool to state whether video processing has started
    st.session_state.bool_start_processing = False
if 'bool_process_clicked' not in st.session_state:  # Bool to state whether video processing has started
    st.session_state.bool_process_clicked = False
if 'bool_balloons' not in st.session_state:  # Bool to state whether video processing success balloons has been shown
    st.session_state.bool_balloons = False
if 'bool_ video_processing_complete' not in st.session_state: # Bool to state whether video processing is completed
    st.session_state.video_processing_complete = False
if 'persistent_error_log' not in st.session_state:  # List kept in statement for persistent error log
    st.session_state.persistent_error_log = []

# Initialize variables
video_files = video_processing.GetVideoNames(constant.videos_location)
num_of_unprocessed_videos = st.empty()
video_title = st.empty()
video_player = st.empty()
video_processing_warning = st.empty()
video_processing_window = st.empty()
part1 = st.empty()  # Quick start guide section
part2 = st.empty()  # Processing videos from file location
part3 = st.empty()  # After video processing

# error_log = video_processing.show_error_log

# Main Page Contents:
# Start of 1️⃣ Quick start guide section
part1 = st.expander("Expand or Collapse", True)
part1.write('###')  # Line break
part1.markdown("""
        ### :one: Quick start guide:
        1. Please prepare the videos on your computer.
        2. Transfer the videos into the 'videos' folder of the application.
        3. After transferring, press the **'R'** key to refresh the app.
        4. Once you're ready to go hit the 'Start Processing Videos' button!
        """)

# Checks for number of videos currently
# If no videos inside 'videos' folder, prompt user to transfer some
if len(video_files) == 0 and not st.session_state.bool_process_clicked:
    part1.write('###')  # Line break
    part1.warning("""The video folder is currently **empty!**""")
    part1.warning(
        """
        \n Transfer the video(s) to the **'videos'** folder of the program's directory. As illustrated the image below.
        """)
    part1.image('pages/assets/transfer_video_instructions.jpg')

part1.write('###')  # Line break
# End of 1️⃣ Quick start guide section


# Start of 4️⃣ Editing the CSV table output
# Checks if the video processing button is clicked
if st.session_state.bool_process_clicked:
    # preserve the info that you hit a button between runs
    st.session_state.bool_process_clicked = True

    # Displays all the errors in error log
    for error in st.session_state.persistent_error_log:
        st.sidebar.warning(error)

    st.write('###')
    st.markdown('### :two: Processing video(s) from file location:')
    st.info('If you are seeing this, that means you have reached the end of processing the videos. \n'
               '\nPlease feel free to continue to view, edit or download the output data or explore the other pages.')

    st.write('###')  # Line break
    st.markdown("""
                ### :three: After processing:
                1. You can download the output CSV with the fish's ID, weight and dimensions (length and depth).
                2. Or go over to the Data Visualization page to view graphs and charts with the newly processed data.
                3. Lastly if you would like to process more videos, please **refresh** the page or hit the **'F5'** key to restart the application.
                """)
    st.write('###')  # Line break

    # Create table on the GUI
    file_list = glob.glob('results/**.csv')
    if len(file_list) == 0:
        st.error("""- ERROR: 'Results CSV data folder is currently empty'
                    \n - Please refresh the page and process some videos to see the video output data.
                    \n - Or check the sidebar error log if something went wrong with processing the output data.
                    """)
    # End of 4️⃣ Editing the CSV table output

    else:
        try:
            option = st.selectbox(
                'Which CSV file would you like to view?',
                file_list)

            # Display the csv contents in table
            df = pd.read_csv(f"{option}")
            grid_return = AgGrid(df, editable=False, enable_enterprise_modules=True, exportDataAsCsv=True,
                                 getDataAsCsv=True)
            new_df = grid_return['data']
            file_name = (str(option[0: option.index(".")]) + '.csv')
            csv = st_scripts.convert_df(new_df)
            # Show a download button to download the csv file
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
        part2.markdown('### :two: Processing video(s) from file location:')

        # Show the button to start video phenotyping process
        video_number = f"""<p><b>Number of unprocessed videos:</b> {str(len(video_files))}</p>"""
        num_of_unprocessed_videos = part2.markdown(video_number, unsafe_allow_html=True)
        st.session_state.bool_have_videos = True

        for video_name in video_files:
            if platform == "win32" or platform == "win64":
                __file__ = f"videos\\{video_name}"

            elif platform == "darwin":
                __file__ = f"videos/{video_name}"

            part2.markdown(f"{video_name} created on  : {time.ctime(os.path.getctime(__file__))}")

        user_ocr_whitelist = video_processing.users_ocr_whitelist()
        start_button = st.empty()

        # Create start video processing button
        isclicked = start_button.button("Start Processing Videos")
        if isclicked:
            st.session_state.bool_start_processing = True
            st.session_state.bool_process_clicked = True

            # Remove all previous sections in the gui
            start_button.empty()
            num_of_unprocessed_videos.empty()

            # Video processing begins
            od = ObjectDetection()  # Initialize Object Detection
            video_processing_note = part2.warning("**Video processing started...**")
            video_processing_note.empty()
            st.session_state.video_processing_complete = video_processing.CaptureImagesOnVideo(video_files, od, user_ocr_whitelist)
    # End of 2️⃣ Processing videos from file location


    # Start of 3️⃣ After processing:
    # If video processing is done
    part3 = st.container()
    if st.session_state.video_processing_complete:
        st.session_state.bool_start_processing = False
        video_processing_warning.empty()
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        part3.success("Video processing completed at " + current_time)

        # Bool to check if balloon gif that states video processed success has been shown
        if not st.session_state.bool_balloons:
            for i in count():
                if i == 0:
                    st.balloons()
                    st.session_state.bool_balloons = True
                    break

        part3.write('###')  # Line break
        part3.markdown("""
            ### :three: After processing:
            1. You can download the output CSV with the fish's ID, weight and dimensions (length and depth).
            2. If there any changes that need to be made, you can edit directly from the table by double clicking the cells.
            3. Or go over to the Data Visualization page to view graphs and charts with your newly processed data.
            4. Lastly if you would like to process more videos, please refresh the page or hit **'F5'** key to restart the application.
            """)
        part3.write('###')  # Line break

        # Create table on the GUI
        # os.chdir('./results')
        file_list = glob.glob('results/**.csv')
        # print('file_list: ', file_list)

        if len(file_list) == 0:
            part3.error(""" Results CSV data folder is currently empty!""")

        else:
            try:
                option = part3.selectbox(
                    'Which CSV file would you like to view?',
                    file_list)

                # Display the csv contents in table
                df = pd.read_csv(f"{option}")
                grid_return = AgGrid(df, editable=False, enable_enterprise_modules=True, exportDataAsCsv=True,
                                     getDataAsCsv=True)
                new_df = grid_return['data']
                file_name = (str(option[0: option.index(".")]) + '.csv')
                csv = st_scripts.convert_df(new_df)
                # Show a download button to download the csv file
                st.download_button(
                    "Press to Download",
                    csv,
                    file_name,
                    "text/csv",
                    key='download-csv'
                )

            except:
                print("This file is not a CSV file!")
    # End of 3️⃣  After processing
