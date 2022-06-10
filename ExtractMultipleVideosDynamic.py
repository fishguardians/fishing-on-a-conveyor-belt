import cv2
import os
import glob

# returns a list of all the file names at that location
path = 'C:\\Users\\rahee\\Desktop\\Raheem Stuff\\SIT Software Engineering\\Trimester 2.3 ITP\\videos\\*.*'

file_list = glob.glob(path)  # A list containing all video paths
increment = 0  # counter to keep track and break out of the while loop when all files have been processed

while increment < len(file_list):
    count = 0  # count variable is used for the frame capturing interval. Will catch every 30th frame
    incrementFrame = 0  # used for jpeg naming convention. Eg. frame0.jpeg, frame1.jpeg
    currentVideo = file_list[increment]  # CurrentVideo variable keeps track of the current video path

    if not os.path.exists(
            'frames' + '_' + currentVideo[
                             86:]):  # if data folder does not exist,then make a new directory called frames + the video file name
        os.makedirs('frames' + '_' + currentVideo[86:])

    cap = cv2.VideoCapture(currentVideo)  # Capture the video that needs to have frames extracted
    print(f'Video {currentVideo[86:]} is processing...')

    while cap.isOpened():
        ret, frame = cap.read()  # ret is a boolean regarding whether there was a return at all, at the frame is
        # each frame that is returned

        if ret:
            cv2.imwrite('./frames' + '_' + currentVideo[86:] + '/frame' + str(incrementFrame) + '.jpg',
                        frame)  # save image in data folder
            count += 30  # i.e. at 30 fps, this advances one second
            incrementFrame += 1
            cap.set(1, count)
        else:
            print(f'Video {currentVideo[86:]} process complete.')
            increment += 1
            incrementFrame += 0
            break

print("All videos successfully processed")
