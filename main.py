import os, os.path
from PIL import Image
from fish_remove_bg import remove_background


if __name__ == "__main__":

    valid_formats = [".jpg", ".png"]

    #get alpha and beta values
    alpha, beta =2, -420

    # get directory path where the images are stored
    image_dir = "/path/to/image read directory/"

    # get directory path where you want to save the images
    output_dir = "/path/to/image write directory/"

    #iterate through all the files in the image directory
    for _, _, image_names in os.walk(image_dir):

        #iterate through all the files in the image_dir
        for image_name in image_names:
            # check for extension .jpg
                if image_name.lower() not in valid_formats:
                    continue
                # get image read path(path should not contain spaces in them)
                filepath = os.path.join(image_dir, image_name)
                # get image write path
                dstpath = os.path.join(output_dir, image_name)
                print(filepath, dstpath)

                # # read the image
                # image = cv2.imread(filepath)
                # # do your processing
                # image2 = cv2.addWeighted(image, alpha,np.zeros_like(image),0,beta)
                # hsv = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
                # # write the image in a different path with the same name
                # cv2.imwrite(dstpath, hsv)
                # print(image.shape, image2.shape, hsv.shape)

# Imports fish images to be processed
# imgs = []
# path = "images/import"
# valid_images = [".jpg", ".png"]
# for f in os.listdir(path):
#     ext = os.path.splitext(f)[1]
#     if ext.lower() not in valid_images:
#         continue
#     imgs.append(Image.open(os.path.join(path, f)))

# print(imgs)

# Remove the background of fish images
# (Leaves only conveyor belt area of image)
# remove_background(imgs)

