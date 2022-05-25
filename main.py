#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''main.py: Main module that runs the fish phenotyping process
    @Author: "Muhammad Abdurraheem, Chen Dong, Nicholas Bingei, Yao YuJing and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
#import if necessary (built-in, third-party, path, own modules)
import camera

video_files = []

def main():
    """
    Main Process
    TODO: *Include more documentation*
    """
    print("""\nFishing on a Conveyor Belt \nAn integrative team project done by students of SIT \nIn collaboration with James Cook University\n""")

    print('Retrieving file names from "videos" folder...')
    print('Files: ' + str(camera.GetVideoNames()) +'\n')
    video_files = camera.GetVideoNames()

    print('Unprocessed videos found: '+str(len(video_files))+'\n')
    camera.CaptureImagesOnVideo(video_files)





if __name__ == "__main__":
    main()