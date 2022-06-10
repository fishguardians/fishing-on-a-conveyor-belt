#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''main.py: Main module that runs the fish phenotyping process
    @Author: "Muhammad Abdurraheem, Chen Dong, Nicholas Bingei, Yao YuJing and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
#import if necessary (built-in, third-party, path, own modules)
import scripts.imagecapture as imagecapture

video_files = []

def main():
    """
    Main Start Function to execute the scripts
    TODO: *Include more documentation*
    """
    print("""\nFishing on a Conveyor Belt \nAn integrative team project done by students of SIT \nIn collaboration with James Cook University\n""")

    print('Retrieving file names from "videos" folder...')
    print('Files: ' + str(imagecapture.GetVideoNames()) +'\n')
    video_files = imagecapture.GetVideoNames()

    print('Unprocessed videos found: '+str(len(video_files))+'\n')
    imagecapture.CaptureImagesOnVideo(video_files)

if __name__ == "__main__":
    main()