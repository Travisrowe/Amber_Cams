from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
import cv2
import os #for getting project file path
import matplotlib.pyplot as plt #for showing images
import sys #for reading args
import pprint

def plot_image_array(images, title = "title", subtitle = "subtitle"):
    fig = plt.figure(title)
    plt.suptitle(subtitle)

    i = 1
    for img in images:
        # show img
        ax = fig.add_subplot(1, 2, i)
        plt.imshow(img, cmap = plt.cm.gray)
        plt.axis("off")
        i = i + 1

    plt.show()

#####################################################################
# Code starts here ##################################################
#####################################################################

# This assumes arguments are like: key1=val1 key2=val2 (with NO spaces between key equal val!)
args = {} #dictionary of arguments passed into the program
img_filepaths = []
images = []

for arg in sys.argv[1:]:
    if(arg[0] != '/'):
        arg = '/' + arg
    img_filepaths.append(arg)
pprint.pprint(img_filepaths)

#make sure image path starts with a /
# if(args["image"][0] != '/'):
#     args["image"] = '/' + args["image"]

#read image into img and convert to RGB
for im_fp in img_filepaths:
    fp = os.path.dirname(os.path.abspath(__file__)) + im_fp
    img = cv2.imread(fp)
    #convert image to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    images.append(img)
for im in images:
    lp = pytesseract.image_to_string(im)
    print(lp)
plot_image_array(images, subtitle=lp)

#print(pytesseract.image_to_string(Image.open(fp)))