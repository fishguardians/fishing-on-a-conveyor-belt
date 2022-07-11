import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './googleaccount.json'
# Instantiates a client
client = vision.ImageAnnotatorClient()

testCase = ['181.jpg','481.jpg','781.jpg','1051.jpg','1441.jpg','1621.jpg','2041.jpg','2491.jpg','2641.jpg']

for names in testCase:
    # The name of the image file to annotate
    file_name = os.path.abspath('./images/20June_fishyy.mp4/id/'+ names)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    text_detection_response = client.text_detection(image=image)
    annotations = text_detection_response.text_annotations
    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ""
    # print("Extracted text {} from image ({} chars).".format(text, len(text)))
    print(text.replace(" ", ""))


# # Performs label detection on the image file
# response = client.label_detection(image=image)
# labels = response.label_annotations

# print('Labels:')
# for label in labels:
#     print(label.description)