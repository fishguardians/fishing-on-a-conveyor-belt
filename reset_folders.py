#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''reset_folders.py: Module check if folders exist and replace any corrupted folders
    @Author: "Yip Hou Liang"
    @Credit: ["Muhammad Abdurraheem", "Chen Dong", "Nicholas Bingei", "Yao Yujing", "Yip Hou Liang"]'''

from os import makedirs
from os.path import dirname
from os.path import exists
import gdown
import csv
import zipfile
import shutil
from distutils.dir_util import copy_tree


def reset_folders():
    # check if necessary folders exists, if not get from backup
    with open('./errorlogs.txt', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header for errors
        writer.writerow(['Severity#', 'Title', 'Message', 'Action'])

    # open the file in the write mode
    errorfile = open('./errorlogs.txt', 'a', encoding='UTF8')
    writer = csv.writer(errorfile)

    # check if backup exists, use backup to overwrite errors
    if not exists('./backup/'):
        makedirs('./backup/')
        writer.writerow(['Serious', 'Missing Folder Error' , 'Missing Backup Folder', 'Downloading Backup from Google Drive'])
        try: 
            gdown.download('https://drive.google.com/uc?id=11B2FQ0he-vcsL4xARHxLOVnhGQFfk-5j', './backup/project.zip', quiet=False)
            with zipfile.ZipFile("./backup/project.zip","r") as zip_ref:
                zip_ref.extractall("./")
            writer.writerow(['Resolved', 'Backup Folder Restored' , 'Fixed Backup Folder', 'Program functioning as expected'])
        except:
            writer.writerow(['Fatal', 'Backup Download Failed' , 'No Backup Available to download', 'Please check your internet connection and retry'])

    if not exists('./Tesseract-OCR/'):
        makedirs('./Tesseract-OCR')
        writer.writerow(['Serious', 'Missing Folder Error' , 'Missing Tesseract Folder', 'Downloading Tesseract from Google Drive'])
        try: 
            gdown.download('https://drive.google.com/uc?id=1ZF3FlYdyqGX2FCddUO_02BPh5KUU0Z7W', './Tesseract-OCR.zip', quiet=False)
            with zipfile.ZipFile("./Tesseract-OCR.zip","r") as zip_ref:
                zip_ref.extractall("./")
            writer.writerow(['Resolved', 'Tesseract Folder Restored' , 'Fixed Tesseract Folder', 'Program functioning as expected'])
        except:
            writer.writerow(['Fatal', 'Tesseract Download Failed' , 'No Tesseract Available to download', 'Please check your internet connection and retry'])

    # check if the important component exists
    if not exists('./pages/'):
        makedirs('./pages/')
        writer.writerow(['Serious', 'Missing Folder Error' , 'No GUI Folder Found', 'Attenpting to restore GUI folder from backup'])
        try: 
            copy_tree("./backup/pages/", "./pages/") 

            writer.writerow(['Resolved', 'Frontend Folder Restored' , 'Fixed Frontend Folder', 'Program functioning as expected'])
        except:
            writer.writerow(['Fatal', 'Project Corrupted' , 'No Backup Available', 'Recreate the project by downloading the folder and unzipping it'])

    if not exists('./scripts/'):
        makedirs('./scripts/')
        writer.writerow(['Serious', 'Missing Folder Error' , 'No Scripts Folder', 'Attenpting to restore Scripts folder from backup'])
        try:
            copy_tree("./backup/scripts/", "./scripts/") 

            writer.writerow(['Resolved', 'Scripts Folder Restored' , 'Fixed Scripts Folder', 'Program functioning as expected'])
        except:
            writer.writerow(['Fatal', 'Project Corrupted' , 'No Backup Available', 'Recreate the project by downloading the folder and unzipping it'])

    if not exists('./testing/'):
        makedirs('./testing/')
        writer.writerow(['Serious', 'Missing Folder Error' , 'No Testing Folder', 'Attenpting to restore Testing folder from backup'])
        try:
            copy_tree("./backup/testing/", "./testing/") 

            writer.writerow(['Resolved', 'Testing Folder Restored' , 'Fixed Testing Folder', 'Program functioning as expected'])
        except:
            writer.writerow(['Fatal', 'Project Corrupted' , 'No Backup Available', 'Recreate the project by downloading the folder and unzipping it'])

    if exists('./dnn_model/'):
        shutil.rmtree('./dnn_model/')
                    
    if not exists('./dnn_model/'):
        makedirs('./dnn_model/')
        try:
            copy_tree("./backup/dnn_model/", "./dnn_model/") 
        except:
            writer.writerow(['Fatal', 'Project Corrupted' , 'No Backup Available', 'Recreate the project by downloading the folder and unzipping it'])

    if not dirname('./constants.py'):
        writer.writerow(['Serious', 'Missing Script Error' , 'Missing Constants Script', 'Attempting to restore constants script from backup'])
        try:
            shutil.copy('./backup/constants.py', './constants.py')
            
            writer.writerow(['Resolved', 'Constants Script Restored' , 'Fixed Constants Script', 'Program functioning as expected'])
        except:
            writer.writerow(['Fatal', 'Project Corrupted' , 'No Backup Available', 'Recreate the project by downloading the folder and unzipping it'])

    # check if the directory exists
    if not exists('./output/'):
        makedirs('./output/')

    if not exists('./output/sample/'):
        makedirs('./output/sample/')
        try:
            copy_tree('./backup/testing/sample/', './output/sample/')
            
            writer.writerow(['Resolved', 'Sample Output Restored' , 'Fixed Sample Output', 'Program functioning as expected'])
        except:
            writer.writerow(['Fatal', 'Project Corrupted' , 'No Backup Available', 'Recreate the project by downloading the folder and unzipping it'])

    if not exists('./results/'):
        makedirs('./results/')

    if not exists('./images/'):
        makedirs('./images/')

    if not exists('./completed_videos/'):
        makedirs('./completed_videos/')

    if not exists('./videos/'):
        makedirs('./videos/')
        
    errorfile.close()
