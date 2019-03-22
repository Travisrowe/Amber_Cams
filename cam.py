from PIL import Image
import pytesseract
import cv2
import os #for getting project file path
import matplotlib.pyplot as plt #for showing images
import sys #for reading args

def plot_image_array(images, title = "title", subtitle = "subtitle"):
    fig = plt.figure(title)
    plt.suptitle(subtitle)

    i = 0
    for img in images:
        # show img
        ax = fig.add_subplot(1, 2, 1)
        plt.imshow(img, cmap = plt.cm.gray)
        plt.axis("off")
        i = i + 1

    plt.show()

# This assumes arguments are like: key1=val1 key2=val2 (with NO spaces between key equal val!)
args = {}
images = []

for arg in sys.argv[1:]:
    k,v = arg.split('=')
    args[k] = v

#make sure image path starts with a /
if(args["image"][0] != '/'):
    args["image"] = '/' + args["image"]
if(args["folder"][0] != '/'):
    args["folder"] = '/' + args["folder"]

#read image into img and convert to RGB
fp = os.path.dirname(os.path.abspath(__file__)) + args["folder"] + args["image"]
img = cv2.imread(fp)
#convert image to RGB
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
images.append(img)
lp = pytesseract.image_to_string(img)
plot_image_array(images, subtitle=lp)

#print(pytesseract.image_to_string(Image.open(fp)))