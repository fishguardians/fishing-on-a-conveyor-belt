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
# st.set_page_config(
#     page_title="Process Video",
#     page_icon="📼",
# )

# Page Sidebar
st.title('📼 Process Video 📼')  # Page Title
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

# Checks if the video processing button is clicked
if st.session_state.bool_process_clicked:
    # preserve the info that you hit a button between runs
    st.session_state.bool_process_clicked = True

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
        st.error("""- ERROR: 'Results CSV data folder is currently empty'
                    \n - Please refresh the page and process some videos to see the video output data.""")

    else:
        try:
            option = st.selectbox(
                'Which CSV file would you like to view?',
                file_list)

            # Display the csv contents in table
            df = pd.read_csv(f"{option}")
            csv = st_scripts.convert_df(df)
            file_name = (str(option[0: option.index(".")]) + '.csv')
            AgGrid(df)

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
        part2.markdown('### :two: Processing videos from file location:')

        # Show the button to start video phenotyping process
        video_number = f"""<p><b>Number of unprocessed videos:</b> {str(len(video_files))}</p>"""
        num_of_unprocessed_videos = part2.markdown(video_number, unsafe_allow_html=True)
        st.session_state.bool_have_videos = True

        # For each video, display it and its name
        for v in video_files:
            __file__ = f"videos\\{v}"
            video_name = f"""<p><b>Video Title:</b> '{v}'</p>"""
            video_date = f"""<p><b>Recorded on:</b> {time.ctime(os.path.getctime(__file__))}</p>"""
            part2.write('###')
            part2.markdown(video_name, unsafe_allow_html=True)
            part2.markdown(video_date, unsafe_allow_html=True)
            v = './videos/' + v
            video_file = open(v, 'rb')
            video = video_file.read()
            part2.video(video)

        fish_selected_warning = part2.empty()
        fish_selected_warning.warning(
                '- As young red snappers have transparent tails, the image processing model is slightly different.\n'
                '- Hence, **if processing baby red snappers please select that option**.\n'
                '- Please avoid mixing barramundi with baby snappers in the video queue for best results.'
                )
        # fish_species_radio_button = part2.radio(
        #     "Which fish species does the video(s) have?",
        #     ('Default/Barramundi', 'Baby Red Snapper'),
        #     help='- If video processing has already started:\n'
        #          '- **Please do not click the options again.**\n'
        #          '- **It will stop the processing!**\n'
        #          '- We arent sure why, but we cant remove the button 🤷')
        # fish_selected = part2.empty()
        #
        # if fish_species_radio_button == 'Default/Barramundi':
        #     fish_selected.write('Default/Barramundi selected.')
        # else:
        #     fish_selected.write("Baby Red Snapper selected.")
        video_processing.show_fish_options()
        start_button = st.empty()

        # Create start video processing button
        isclicked = start_button.button("Start Processing Videos")
        if isclicked:
            st.session_state.bool_start_processing = True
            st.session_state.bool_process_clicked = True

            # Remove all previous sections in the gui
            start_button.empty()
            num_of_unprocessed_videos.empty()
            # fish_selected.empty()
            fish_selected_warning.empty()

            # TODO: Make it work or remove it
            # Sends type of fish to video processing function
            # def send_fish_species(fish_species):
            #     return fish_species
            #
            # if fish_species_radio_button == 'Baby Red Snapper':
            #     print('Baby red snapper selected ent to video processing module')
            #     send_fish_species(fish_species_radio_button)
            # else:
            #     print('Default fish sent to video processing module')
            #     send_fish_species(fish_species_radio_button)
            # TODO: Make it work or remove it

            # Video processing begins
            od = ObjectDetection()  # Initialize Object Detection
            video_processing_warning = part2.warning("**Video processing started...**")
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
        current_time = now.strftime("%I:%M %p")
        part3.success("Video processing complete at " + current_time)

        # Bool to check if balloon gif that states video processed success has been shown
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
