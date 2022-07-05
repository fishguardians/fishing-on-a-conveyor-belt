import scripts.video_processing as video_processing  # Video processing scripts
import scripts.streamlit_scripts as st_scripts  # Custom streamlit scripts
import constant  # Constant Variables

from datetime import datetime
import streamlit as st
import time

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

FINISHED = False

# TODO: For multiple videos have state management to track status of each video
#   - TODO: Add queue system in sidebar to show current video process queue
#   - TODO: On start processing st.empty to clear all videos (Queue will be moved to the sidebar)
#   - TODO: Add progress bar to the video currently processing
# TODO: Move start button below 'num of unprocessed videos'

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
    video_processing.CaptureImagesOnVideo(cached_videos)

# If video processing is done
# TODO: MAKE IT WORKK!!!!!!!

if True:
    video_processing_warning.empty()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    st.success("Video processing complete at " + current_time)
    st.balloons()
    # st.markdown("""
    # TODO: Buttons to export the CSV Data
    # TODO: Redirect user to Data Visualization page to view exported CSV data
    # """)

    st.write('###')  # Line break
    st.markdown("""
    ### :three: After processing:
    1. You can download the output CSV with the fishID, fish's weight fish's dimensions (length and depth)
    2. Or go over to the Data Visualization page to view graphs and charts with the newly processed data
    """)

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
