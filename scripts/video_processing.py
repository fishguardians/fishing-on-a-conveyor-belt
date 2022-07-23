#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''video_processing.py: Video capture module that takes the images of the fish
    @Author: "Muhammad Abdurraheem and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)
import os
import shutil
import csv
import cv2
import math
import numpy as np
from imutils.video.count_frames import count_frames_manual
import constant
import pytesseract
import streamlit as st
import time

if (os.name == 'nt'):
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"  # Path of where pytesseract.exe is located

# Read the scale
from scripts.digit_recognition import digit_recognition
from scripts.fish_measurement import fish_measurement
from scripts.text_recognition import text_recognition
from scripts.generate_csv import write_data_output
from scripts.object_detection import ObjectDetection

# open the file in the write mode
errorfile = open('./errorlogs.txt', 'a', encoding='UTF8')
errwriter = csv.writer(errorfile)


def GetVideoNames(path):
    """ # 1 - directory of stored videos """

    folder = os.listdir(path)
    videos_array = []

    print("FOLDER", folder)

    for file in folder:
        _, file_extension = os.path.splitext(file)
        # Add required txt files
        if (file != '.gitignore' and file != '.DS_Store'):
            # check if the directory exists
            if not os.path.exists('output/' + file):
                os.makedirs('output/' + file)
            with open('output/' + file + '/images.txt', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header for hypothenuse
                writer.writerow(['#', 'Fish#', 'Frame', 'Hypothenuse'])
            with open('output/' + file + '/dimensions.txt', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header for dimension
                writer.writerow(['#', 'Fish#', 'Frame', 'Length', 'Depth'])
            with open('output/' + file + '/ids.txt', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header for id
                writer.writerow(['#', 'Fish#', 'Frame', 'Value'])
            with open('output/' + file + '/weights.txt', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write the header for weight
                writer.writerow(['#', 'Fish#', 'Frame', 'Weight'])

        # Add to list of videos to be processed
        if file_extension.lower() == '.mov':
            videos_array.append(file.lower())
        elif file_extension.lower() == '.mp4':
            videos_array.append(file.lower())
        else:
            # TODO: For each errwriter get it to display in the GUI sidebar
            errwriter.writerow(['Warning', 'Unsupported Video Format', 'Video Not MP4 or MOV',
                                'Please check ' + str(file) + ' for supported formats'])
            continue
    return videos_array


def CaptureImagesOnVideo(videos_to_be_processed, od):
    """# 2 - Process the videos [batch processing]"""
    # check for smallest distance
    hypo_threshold = 90
    # center points curr
    prev_center_pts = []
    # check if last 3 frames has a fish
    check_empty = 3
    # allocate the id for the fish
    wells_id = 0

    # Initalize line break
    video_processing_line_break = st.empty()
    # Initalize title of video being processed
    video_processing_title = st.empty()
    # Initialize video processing window in GUI
    video_processing_window = st.empty()

    # Create the progress bar
    progress_bar = st.empty()
    progress_bar.progress(0)

    # Initialize metrics
    metrics = st.empty()

    for _video_index, _video_name in enumerate(videos_to_be_processed):
        print('Processing video ' + str(_video_index + 1) + '...\n')
        # use to capture 1 frame per second
        _skip_frames = 0
        # use for naming frames in case id cannot be detected
        _frame_index = 0
        # ids for tracking in txt files
        _fish_id, _id_id, _scale_id = 0, 0, 0
        # Class for video capturing from video files, image sequences or cameras
        cap = cv2.VideoCapture(constant.videos_location + _video_name)
        # Get the number of frames in video
        num_of_frames = count_frames(constant.videos_location + _video_name)

        seconds_left = round(num_of_frames/30)

        if (cap.isOpened() == False):
            print("Error opening video stream or file")
            errwriter.writerow(['Serious', 'Video Corrupted Error', 'Video Cannot Process',
                                'Skipping Video, please check if video is correct'])

        while (cap.isOpened()):

            ret, frame = cap.read()

            # exact frame counts
            _frame_index += 1

            # when stream ends
            if not ret:
                cap.release()
                # Generate final csv file and then move the file to completed
                try: 
                    response = write_data_output(_video_name)
                except:
                    errwriter.writerow(['Serious', 'CSV Output Corrupted Error' , 'Fail to Create CSV', 'Skipping Video, please check if data is inside'])
                MoveVideo(_video_name)
                print(f'Video {_video_index + 1} process complete.')
                break

            # Loading image
            img = frame.copy()  # 1080 1920 original image
            img = cv2.resize(img, None, fx=0.4, fy=0.4)

            og_img = frame.copy()

            # Width & Height of img
            height, width, channels = img.shape
            # center point location of img
            posY = int(height / 2)
            posX = int(width / 2)

            # display location of objects
            fish_coords = []
            fish_center_coords = []
            id_coords = []
            scale_coords = []

            # Detect objects on frame
            (class_ids, scores, boxes) = od.detect(img)

            # check if can save img
            _has_image = False

            # print(class_ids, prev_center_pts, check_empty)

            # if there's no fish add the tracker empty by 1
            if (prev_center_pts == []):
                check_empty += 1

            for (index, box) in enumerate(boxes):
                x, y, w, h = box

                # check if 2 objects are in the image [id tag, fish]
                if class_ids[index] == 0: # Detected that id tag is found
                    id_coords = box
                    _id_id += 1

                    # Work with a copy of the smaller version of image
                    id_image = img.copy()
                    # Give some padding to ensure values are read properly
                    if y - 10 < 0 or y + h + 10 > height or x - 10 < 0 or x + w + 10 > width:
                        id_image = id_image[y:y + h, x:x + w]
                    else:
                        id_image = id_image[y - 10:y + h + 10, x - 10:x + w + 10]

                    # Save for reference checking
                    SaveImages(id_image, _frame_index, _video_name, 'id')

                    # Call the id tag scripts
                    words = text_recognition(id_image)

                    # Call the id tag scripts
                    words = text_recognition(id_image)

                    if len(words) < 7:
                        errwriter.writerow(['Warning', 'ID Tag Not Found' , 'Request User Validation', 'Please check frame ' + str(_frame_index) + '.jpg in /images/' + _video_name + '/id/'])

                    # open the file to write
                    with open('output/' + _video_name + '/ids.txt', 'a', encoding='UTF8') as f:
                        # create the csv writer
                        writer = csv.writer(f)
                        # ['#', 'Fish#', 'Frame', 'Value']
                        writer.writerow([_id_id, wells_id, _frame_index, words])
                elif class_ids[index] == 1:  # Detected the barramundi fish
                    fish_coords = box
                    # center point of the fish
                    cx = int((x + x + w) / 2)
                    cy = int((y + y + h) / 2)
                    fish_center_coords.append((cx, cy))

                    hypothenuse = round(math.hypot(cx - posX, cy - posY))
                    # print(hypothenuse, hypo_threshold)

                    if (prev_center_pts == [] and check_empty >= 2):
                        # check if the previous 3 frames are empty if not it is the same fish
                        wells_id += 1

                    # distance lesser than previous distance
                    if (hypothenuse < hypo_threshold):
                        _fish_id += 1
                        hypo_threshold = hypothenuse
                        _has_image = True

                        # Save for reference checking
                        SaveImages(frame, _frame_index, _video_name, 'actual')

                        # open the file to write
                        with open('output/' + _video_name + '/images.txt', 'a', encoding='UTF8') as f:
                            # create the csv writer
                            writer = csv.writer(f)
                            # ['#', 'Fish#', 'Frame', 'Hypothenuse']
                            writer.writerow([_fish_id, wells_id, _frame_index, hypothenuse])

                    # reset checker
                    else:
                        hypo_threshold = 90  # Try to another fish that is closer

                    check_empty = 0

                    if (_has_image):
                        # get fish dimensions using image
                        fish_length, fish_depth, cropped_img, flag = fish_measurement(frame.copy())
                        # open the file to write
                        # error checking for fish dimensions
                        if len(flag) > 0:
                            errwriter.writerow(['Warning', 'Fish Dimension Not Found' , 'Request User Validation', 'Please check frame ' + str(_frame_index) + '.jpg in /images/' + _video_name + '/actual/'])
                        with open('output/' + _video_name + '/dimensions.txt', 'a', encoding='UTF8') as f:
                            writer = csv.writer(f)
                            # write the header

                            """
                            '#' - fish_id is the # unique key for the data
                            'Fish#' - current num of fish that's passing through the conveyor belt
                            'Frame' - the num value of the frame of the video image taken
                            'Length' - length of the fish (From head to tail)
                            'Depth' - the length of the depth of the fish (Widest point of the fish)
                            """
                            # writer.writerow(['#', 'Fish#', 'Frame', 'Length', 'Depth'])
                            writer.writerow([_fish_id, wells_id, _frame_index, fish_length, fish_depth, flag])

                        SaveImages(cropped_img, _frame_index, _video_name, 'fish')
                        
                else:
                    continue

            if (_has_image == True):
                _scale_id += 1

                # retreives the weight from the scale
                scale_reading = digit_recognition(frame)

                # error checking for scale reading
                if(scale_reading == 'N.A'):
                    errwriter.writerow(['Warning', 'Scale Reading Not Found' , 'Request User Validation', 'Please check frame ' + str(_frame_index) + '.jpg in /images/' + _video_name + '/scale/'])
                    
                # open the file to write
                with open('output/' + _video_name + '/weights.txt', 'a', encoding='UTF8') as f:
                    # create the csv writer
                    writer = csv.writer(f)
                    # ['#', 'Fish#', 'Frame', 'Weight']
                    writer.writerow([_scale_id, wells_id, _frame_index, scale_reading])

            # View Video
            view_video_output = ViewVideo(fish_coords, fish_center_coords, id_coords, scale_coords, _video_name,
                                            img)

            # For streamlit to display video
            video_processing_line_break.markdown('***')
            video_processing_title.info('**Video currently processing:** ' + _video_name)
            video_processing_window.image(view_video_output, channels='BGR', use_column_width=True)

            # check the location of fish center points
            prev_center_pts = fish_center_coords.copy()

            _skip_frames += 30  # i.e. at 30 fps, this advances one second
            _frame_index += 29
            cap.set(1, _skip_frames)

            if cv2.waitKey(1) == ord('q'):
                # reset the fish wells_id
                wells_id = 0
                break

            # Create percentage bar based on the number of frames progressed
            current_percent = int((_frame_index / num_of_frames) * 100)
            if current_percent >= 100:
                progress_bar.progress(100)
            else:
                progress_bar.progress(current_percent)

            #TODO: Maybe can combine the lenghts of the videos to calculate the total percentage and estimated time for processing.

            seconds_left -= 1
            metric_percent = str(round(current_percent)) + '%'
            mins_shown = round(seconds_left//60)
            seconds_shown = str(seconds_left - (mins_shown*60))
            metric_time_left = str(mins_shown) + ' mins ' + seconds_shown + ' s'
            metric_fishes = str(wells_id) + '🐠'

            if current_percent >= 100:
                metric_percent = '100%'
                metric_time_left = 'Done'

            if seconds_left <= 0:
                metric_percent = '100%'
                metric_time_left = 'Done'

            with metrics.container():
                col1, col2, col3 = st.columns(3)
                col1.metric(label="✔ Completion Percentage: ✔", value=metric_percent, help='Percentage of completion '
                                                                                           'of processing the current'
                                                                                           ' video.')
                col2.metric(label="⌛ Estimated Time Left: ⌛", value=metric_time_left, help='Typically takes same '
                                                                                           'amount of time as the '
                                                                                           'length of the video.')
                col3.metric(label="🎣 Fish Caught: 🎣", value=metric_fishes, help='Total number of fish processed '
                                                                                  'from the videos.')
                time.sleep(0.01)

        cap.release()
        cv2.destroyAllWindows()

    metric_percent = 0  # Percentage of processing competition
    metric_time_left = 0  # Estimated time left for processing
    metric_fishes = 0  # Number of fish found in the video

    return True

def ViewVideo(fish, fish_center, id, scale, name, img):
    """Additional: to see the video while it is processing"""
    try:
        # duplicate image so it doesn't corrupt the original
        main_frame = img.copy()
        height, width, channels = main_frame.shape
        # show objects
        if (len(fish) > 0):
            cv2.rectangle(main_frame, (fish[0], fish[1]), (fish[0] + fish[2], fish[1] + fish[3]), constant.fish_color,
                          2)
            cv2.circle(main_frame, fish_center[0], 3, constant.fish_color, -1)
            cv2.putText(main_frame, str(fish), (fish[0] + fish[2], fish[1] + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0,
                        constant.fish_color, 2)
        if (len(id) > 0):
            cv2.rectangle(main_frame, (id[0], id[1]), (id[0] + id[2], id[1] + id[3]), constant.id_color, 1)
        if (len(scale) > 0):
            cv2.rectangle(main_frame, (scale[0], scale[1]), (scale[0] + scale[2], scale[1] + scale[3]),
                          constant.scale_color, 2)
        # show center position of image
        # cv2.circle(main_frame, (int(width/2), int(height/2)), 3, (0,0,255), -1)
        cv2.line(main_frame, (0, int(height / 2)), (width, int(height / 2)), (0, 0, 255), 1)
        cv2.line(main_frame, ((int(width / 2), 0)), (int(width / 2), height), (0, 0, 255), 1)

        # display the window
        # cv2.imshow(name, main_frame)

        return main_frame

    except:
        errwriter.writerow(['Serious', 'ViewVideo Function Error', 'Fail to View Videos', 'Request technical support'])


def MoveVideo(video):
    """Move the processed videos to completed folder so they will not run again"""
    try:
        shutil.rmtree('completed_videos/' + video + '/')
        # check if the directory exists
        if not os.path.exists('completed_videos/' + video):
            os.makedirs('completed_videos/' + video)
            shutil.move("./videos/" + video, 'completed_videos/' + video, copy_function=shutil.copy2)
        else:
            os.remove('videos/' + video)
    except:
        errwriter.writerow(['Warning', 'Same Video Re-Processed', 'Deliberate User Action',
                            'Processing same videos will use up unnecessary computer resources'])


def SaveImages(actual_frame, _frame_index, _video_name, _type):
    """Store images function"""
    try:
        # check if the directory exists
        if not os.path.exists('images/' + _video_name + '/' + _type):
            os.makedirs('images/' + _video_name + '/' + _type)
        # write to seperate folders for easier book-keeping
        cv2.imwrite('./images/' + _video_name + '/' + _type + '/' + str(_frame_index) + '.jpg', actual_frame)
    except:
        errwriter.writerow(['Serious', 'SaveImages Function Error', 'Fail to Save Images', 'Request technical support'])

# Count the total number of frames in a video with OpenCV and Python
def count_frames(path, override=False):
    # grab a pointer to the video file and initialize the total
    # number of frames read
    video = cv2.VideoCapture(path)
    total = 0
    # if the override flag is passed in, revert to the manual
    # method of counting frames
    if override:
        total = count_frames_manual(video)

    # otherwise, let's try the fast way first
    else:

        try:
            total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        # uh-oh, we got an error -- revert to counting manually
        except:
            total = count_frames_manual(video)

    # release the video file pointer
    video.release()
    # return the total number of frames in the video
    return total
