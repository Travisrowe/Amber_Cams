import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
import cv2
import os #for getting project file path
import matplotlib.pyplot as plt #for showing images
import sys #for reading args
import pprint
from LPEX import Extraction #used to crop to license plate
import mysql.connector
        
class CarPicture():
    img = 0
    lp_img = 0
    lp = ""
    def __init__(self, im):
        self.img = im
        self.process_image()

    def process_image(self):
         #Crop image to only license plate using neural network
        self.img,self.lp_img = Extraction.Extract(self.img)
        self.lp_img = cv2.cvtColor(self.lp_img, cv2.COLOR_RGB2GRAY)
        (thresh, img_bw) = cv2.threshold(self.lp_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        #cv2.imshow('original', img_bw)

        #convert image to string
        self.lp = pytesseract.image_to_string(img_bw)
        self.lp = self.remove_non_alphanum_chars(self.lp)
        if(self.lp == ""):
            print("Neural Network model did not detect a license plate")
            return
        rowList = self.query_license_plate(self.lp)
        if(len(rowList) > 0):
            print("Query for license plate # " + self.lp + " returned the following results:")
            print(rowList)
            # cv2.imshow('original', self.img)
            # cv2.imshow('license plate', self.lp_img)
        else:
            print("Query for license plate # " + self.lp + " did not return any results")
        cv2.imshow('original', self.img)
        cv2.imshow('license plate', self.lp_img)
        cv2.waitKey(0)

    def remove_non_alphanum_chars(self, s):
        for i in range(0, len(s) - 1):
            c = s[i]
            asciVal = ord(c)
            if(not ((asciVal >= 48 and asciVal <= 59) or (asciVal >= 65 and asciVal <= 90))):
                s = s[:i] + s[i+1:]
        return s

    def plot_image_array(self, images, title = "title", subtitle = "subtitle"):
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

    def query_license_plate(self,lp):
        cnx = mysql.connector.connect(host='127.0.0.1',database='amber_alerts', user="", password="", auth_plugin='mysql_native_password')
        cursor = cnx.cursor()
        rowList = set()

        for i in range(0, len(lp) - 1):
            lp_copy = lp #this is the license plate with some SQL wildcards replacing characters
            lp_copy = lp_copy[:i] + '%' + lp_copy[i + 1:]
            for j in range(i, len(lp) - 1):
                lp_copy = lp_copy[:j] + '%' + lp_copy[j + 1:]
                #query using LIKE lp_copy
                query = ("SELECT * from tblAmberAlerts WHERE LicensePlate LIKE '" + lp_copy + "'")
                cursor.execute(query)
                for row in cursor:
                    rowList.add(row)
        cnx.close()
        return rowList


#####################################################################
# Main starts here ##################################################
#####################################################################

# This assumes arguments are like: key1=val1 key2=val2 (with NO spaces between key equal val!)
args = {} #dictionary of arguments passed into the program
img_filepaths = []
images = []

for arg in sys.argv[1:]:
    if(arg[0] != '/'):
        arg = '/' + arg
    img_filepaths.append(arg)

#make sure image path starts with a /
# if(args["image"][0] != '/'):
#     args["image"] = '/' + args["image"]

#read image into img and convert to RGB
for im_fp in img_filepaths:
    fp = os.path.dirname(os.path.abspath(__file__)) + im_fp
    img = cv2.imread(fp)
    #convert image to RGB
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    CarPicture(img)

# for im in images:

#     #Crop image to only license plate using neural network
#     im,lp_img = Extraction.Extract(im)
#     lp_img = cv2.cvtColor(lp_img, cv2.COLOR_RGB2GRAY)
#     (thresh, im_bw) = cv2.threshold(lp_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#     cv2.imshow('original', im_bw)

#     #convert image to string
#     lp = pytesseract.image_to_string(im_bw)
#     lp = remove_non_alphanum_chars(lp)
#     rowList = query_license_plate(lp)
# plot_image_array(images, subtitle=lp)

# #print(pytesseract.image_to_string(Image.open(fp)))