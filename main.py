#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''main.py: Main module that runs the fish phenotyping process
    @Author: "Muhammad Abdurraheem, Chen Dong, Nicholas Bingei, Yao YuJing and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)

import scripts.imagecapture as imagecapture
import scripts.fish_remove_bg as script_remove_bg
import scripts.fish_crop_belt as script_process_crop
import scripts.fish_dimensions as script_get_dimensions

from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

video_files = []


def main():
    """
    Main Start Function to execute the scripts
    TODO: *Include more documentation*
    """
    # print("""\nFishing on a Conveyor Belt \nAn integrative team project done by students of SIT \nIn collaboration with James Cook University\n""")
    #
    # print('Retrieving file names from "videos" folder...')
    # print('Files: ' + str(imagecapture.GetVideoNames()) +'\n')
    # video_files = imagecapture.GetVideoNames()
    #
    # print('Unprocessed videos found: '+str(len(video_files))+'\n')
    # imagecapture.CaptureImagesOnVideo(video_files)
    #
    # print("End of video image capture process: ", current_time)

    """
    Fish Dimension Functions
    """

    print("1. Running Fish background removal functions")
    print('Retrieving files from "images" folder...')

    # Step 1
    # Remove background and export the output
    print('2. Removing background from fish images...')
    image_list = script_remove_bg.get_image_names()
    remove_bg_output = script_remove_bg.remove_background(image_list)
    print('Background removal complete!')

    # Step 2
    # Crop out the yellow belt areas
    print('3. Cropping out yellow belt areas of images...')
    crop_belt_output = script_process_crop.crop_belt(remove_bg_output)
    print('Conveyor belt cropped out!')

    # Step 3
    # Measure the dimensions of the fish
    print('4. Measuring dimensions of the fish...')
    fish_dimensions = script_get_dimensions.get_dimensions(crop_belt_output)
    # Output the dimensions into a CSV file
    script_get_dimensions.output_dimensions(fish_dimensions)

if __name__ == "__main__":
    main()
