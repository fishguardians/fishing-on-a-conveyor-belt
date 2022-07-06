
from os import makedirs
from os.path import dirname
from os.path import exists
import gdown
import csv
import zipfile
import shutil
from distutils.dir_util import copy_tree

def reset_folders():

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

                    
    if not exists('./dnn_model/'):
        makedirs('./dnn_model/')
        writer.writerow(['Serious', 'Missing Folder Error' , 'No ML Model Folder', 'Attenpting to restore ML Model folder from backup'])
        try:
            copy_tree("./backup/dnn_model/", "./dnn_model/") 

            writer.writerow(['Resolved', 'Dnn Model Restored' , 'Fixed ML Model Folder', 'Program functioning as expected'])
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

    if not exists('./images/'):
        makedirs('./images/')

    if not exists('./completed_videos/'):
        makedirs('./completed_videos/')

    if not exists('./videos/'):
        makedirs('./videos/')
        
    errorfile.close()
