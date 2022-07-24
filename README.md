# Fish phenotyping project
Video recording and image analysis of fishes to automate and increase the efficiency of fish phenotyping, and bolster posterior analysis to improve farm production and management.

## Getting Started
Git clone this repository or download the whole zip package from [Github](https://github.com/fishguardians/fishing-on-a-conveyor-belt.git)
```git clone https://github.com/fishguardians/fishing-on-a-conveyor-belt.git```

### Prerequisites
Install Python v@3.10 using this [Windows_x64](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe), [Windows_x32](https://www.python.org/ftp/python/3.10.0/python-3.10.0.exe), [macOS](https://www.python.org/ftp/python/3.10.0/python-3.10.0post2-macos11.pkg) or navigate to [Downloads](https://www.python.org/downloads/release/python-3100/) 


Install Pip v@21.2.3 with command  ```python -m pip install pip==21.2.3```

### Installation
Install required python libraries  ```pip install -r requirements.txt```

### Usage
For educational and research purposes. 

## Contributing
For further details or development, email:
pureskill714[Raheem] - [raheemrocker@gmail.com](mailto:raheemrocker@gmail.com)
nbinged[Nicholas] - [nbingei@gmail.com](mailto:nbingei@gmail.com)
Don-Whis[Chen Dong] - [chen809490819@gmail.com](mailto:chen809490819@gmail.com)
yaoyujing - [yujing1314276@gmail.com](mailto:yujing1314276@gmail.com)
SageSG[Henry] - [mailstohenry@gmail.com](mailto:mailstohenry@gmail.com)

## License

## Contact
Please contact [Singapore Institute of Technology](https://www.singaporetech.edu.sg/connect/contact-us) & [James Cook University](https://www.jcu.edu.sg/current-students/campus-maps-And-information/contact-us) for further enquiries.

### Acknowledgements
Many thanks to the researchers at James Cook University for their hospitality and assistance. 
Special thanks to the Academic Professor, Kirwan Ryan Fraser and Industry Supervisor, Jose Domingos and his assistant Joseph Angelo.

<hr/>

## Documentations
Darknet (For YOLOv3 and YOLOv4 convolunsional network) [github link](https://github.com/AlexeyAB/darknet)

Streamlit (Graphic User Interface) [streamlit docs](https://docs.streamlit.io/)

Pandas (Data Visualisation) [pandas docs](https://pandas.pydata.org/pandas-docs/stable/)

## Tutorials

Tesseract tutorial (Fish ID Detection) [youtube link 1](https://www.youtube.com/watch?v=JkzFjj2hjtw&t=894s), [youtube link 2](https://www.youtube.com/watch?v=PY_N1XdFp4w&t=164s), [configs](https://stackoverflow.com/questions/44619077/pytesseract-ocr-multiple-config-options)

Google Colab (Object Tracking and YOLOv3) [youtube link](https://www.youtube.com/watch?v=O3b8lVF93jU&t=14s)

LabelMe Library (Create Clean Datasets) [link](https://roboflow.com/convert/labelme-json-to-yolo-darknet-txt)

YOLOv3 Tutorial (Train Images) [link](https://pysource.com/2020/04/02/train-yolo-to-detect-a-custom-object-online-with-free-gpu/)

OpenCV (Digit Recognition) [url_name]()

OpenCV (Fish Dimension) [url_name]()

## Links
Read files by directory - [link](https://realpython.com/working-with-files-in-python/)

Unittest - [link](https://machinelearningmastery.com/a-gentle-introduction-to-unit-testing-in-python/)

## Troubleshooting
Troubleshooting document [doc_link]()

<hr/>

## Project Structure

| # | {Path}  | Description | Commands |
| --- | --- | --- | --- |
| 1 | ./backup | Stores a duplicate of the project | -runs from main.py- |
| 2 | ./completed_videos | Stores the completed videos | -runs from video_processing.py- |
| 3 | ./dnn_model | Stores the trained object detection model | -runs from main.py- |
| 4 | ./images | Stores the images for verification | -runs from video_processing.py- |
| 5 | ./output | Stores the unedited results from the processed videos | -runs from multiple scripts- |
| 6 | ./pages | Stores the frontend streamlit pages | -runs from main.py- |
| 7 | ./scripts | Stores all the scripts being used for video processing | -runs from main.py- |
| 8 | ./testing | Stores the examples for testing | -runs from test_project.py- |
| 9 | ./videos | Allow users to store unprocessed videos | -runs from main.py- |
| 10 | ./constant.py | Stores the variables in use | -runs from main.py- |
| 11 | ./errorlogs.txt | Stores the errors that is caught | -runs from main.py- |
| 12 | ./reset_folders | Check for corrupted folders | -runs from main.py- |
| 13 | ./main.py | Starts the program | -runs from main.py- |
| 14 | ./test_project.py | Unit Testing for the program | -can run by itself- |

## Scripts 

| # | Scripts  | Description |
| --- | --- | --- |
| 1 | main.py | Starts the program, check for errors, initalise object detection, run video processing |
| 2 | video_processing.py | Get videos, skip frames, detect objects from frames, check hypothenuse of fish to centre of frame, save images, move videos, view video with streamlit |
| 3 | reset_folders.py | Check if the folders are in the project |
| 4 | test_project.py | Test if sub functions are working properly |
| 5 | object_detection.py | Uses the yolov4 model, configs and classes to detect image |
| 6 | digit_recognition.py | Retrieve fish weight reading from the image |
| 7 | fish_measurement.py | Calls upon image enchancers to scrubbing data from image |
| 8 | generate_csv.py | Perform data cleaning, using median, mode and IQR |
| 9 | streamlit_scripts.py | Cache unprocessed videos |
| 10 | text_recognition.py | Use pytesseract to detect fish id tags |
| 11 | constants.py | Stores the variables used throughout the project |

<hr/>