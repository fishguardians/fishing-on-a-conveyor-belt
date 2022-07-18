import cv2

"""This is a unit test for the entire project module."""

import scripts.digit_recognition as dr
import scripts.generate_csv as gc
import scripts.fish_measurement as fm
import scripts.object_detection as ob
import scripts.text_recognition as tr
import scripts.video_processing as vp
import scripts.streamlit_scripts as st

def test_digit_recognition():
    """Test the digit recognition module."""
    print(dr.digit_recognition(cv2.imread('testing_folder/106.jpg')))
    print(dr.get_roi(cv2.imread('testing_folder/106.jpg')))
#     # assert dr.digit_recognition('') == 0
