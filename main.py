#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''main.py: Main module that runs the fish phenotyping process
    @Author: "Muhammad Abdurraheem, Chen Dong, Nicholas Bingei, Yao YuJing and Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''
# import if necessary (built-in, third-party, path, own modules)

import sys
from streamlit import cli as stcli
import streamlit as st
import reset_folders

def main():
    """
    Main Start Function to execute the scripts
    TODO: *Include more documentation*
    """
    print(
        """\nFishing on a Conveyor Belt \nAn integrative team project done by students of SIT \nIn collaboration with James Cook University\n""")

if __name__ == "__main__":
    print('Checking if file are corrupted...')
    reset_folders.reset_folders()
    if st._is_running_with_streamlit:
        main()
    else:

        # sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.argv = ["streamlit", "run", "01_🏠_Home.py"]
        # print('sys.argv[0]: ', sys.argv[0])
        sys.exit(stcli.main())
