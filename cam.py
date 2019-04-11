#from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
import cv2
import os #for getting project file path
import matplotlib.pyplot as plt #for showing images
import sys #for reading args
import pprint
#import imutils
#import importlib
from LPEX import Extraction #used to crop to license plate

# """
# parameters:
#     c - a contour of a shape
# """
# def detect_shape(c):
#     # initialize the shape name and approximate the contour
#     shape = "unidentified"
#     peri = cv2.arcLength(c, True)
#     approx = cv2.approxPolyDP(c, 0.04 * peri, True)

#     # if the shape has 4 vertices, it is either a square or
#     # a rectangle
#     if len(approx) == 4:
#         # compute the bounding box of the contour and use the
#         # bounding box to compute the aspect ratio
#         (x, y, w, h) = cv2.boundingRect(approx)
#         ar = w / float(h)

#         # a square will have an aspect ratio that is approximately
#         # equal to one, otherwise, the shape is a rectangle
#         return "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

#     # return the name of the shape
#     return

# def img_to_license_plate_text(im):
#     alpr = Alpr("us", "/path/to/openalpr.conf", "/path/to/runtime_data")
#     if not alpr.is_loaded():
#         print("Error loading OpenALPR")
#         sys.exit(1)
        
#     alpr.set_top_n(20)
#     alpr.set_default_region("md")

#     results = alpr.recognize_file("/path/to/image.jpg")

#     i = 0
#     for plate in results['results']:
#         i += 1
#         print("Plate #%d" % i)
#         print("   %12s %12s" % ("Plate", "Confidence"))
#         for candidate in plate['candidates']:
#             prefix = "-"
#             if candidate['matches_template']:
#                 prefix = "*"

#             print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))

#     # Call when completely done to release memory
#     alpr.unload()

# """
# uses functions: detect_shape
# """
# def crop_to_license_plate(im):
#     # load the image and resize it to a smaller factor so that
#     # the shapes can be approximated better
#     resized = imutils.resize(im, width=300)
#     ratio = im.shape[0] / float(resized.shape[0])
    
#     # convert the resized image to grayscale, blur it slightly,
#     # and threshold it
#     gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#     thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
    
#     # find contours in the thresholded image and initialize the
#     # shape detector
#     cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
#         cv2.CHAIN_APPROX_NONE)
#     cnts = imutils.grab_contours(cnts)

#     # loop over the contours
#     for c in cnts:
#         # compute the center of the contour, then detect the name of the
#         # shape using only the contour
#         M = cv2.moments(c)
#         cX = int((M["m10"] / M["m00"]) * ratio)
#         cY = int((M["m01"] / M["m00"]) * ratio)
#         shape = detect_shape(c)
    
#         # multiply the contour (x, y)-coordinates by the resize ratio,
#         # then draw the contours and the name of the shape on the image
#         c = c.astype("float")
#         c *= ratio
#         c = c.astype("int")
#         cv2.drawContours(im, [c], -1, (0, 255, 0), 2)
#         cv2.putText(im, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
#             0.5, (255, 255, 255), 2)
    
#         # show the output image
#         cv2.imshow("Image", im)
        

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
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    images.append(img)
for im in images:

    im,lp_img = Extraction.Extract(im)
    lp_img = cv2.cvtColor(lp_img, cv2.COLOR_RGB2GRAY)
    (thresh, im_bw) = cv2.threshold(lp_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow('original', im_bw)

    lp = pytesseract.image_to_string(im_bw)
    print(lp)
plot_image_array(images, subtitle=lp)

#print(pytesseract.image_to_string(Image.open(fp)))