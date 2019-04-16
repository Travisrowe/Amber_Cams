import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
import cv2
import os #for getting project file path
import matplotlib.pyplot as plt #for showing images
import sys #for reading args
import pprint
import json
from LPEX import Extraction #used to crop to license plate
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
        
class CarPicture():
    filepath = ""
    img = 0
    lp_img = 0
    lp = ""
    def __init__(self, fp):
        self.filepath = fp
        self.img = cv2.imread(fp)

    """
    The meat of our class. This function fills our variables lp_img and lp.
    It uses those variables to query the database and determine if a notification should be
    emailed to police

    parameters:
        - self 
            - uses self.img, an image of the car 
            - self.lp_img, a neural-network-cropped image of just the license plate (ideally), returned by Extraction.Extract
            - self.lp, a string of license plate text, returned by pytesseract
    
    returns:
        rowList - a list of rows that have been returned from the database query
    """
    def process_image(self):
         #Crop image to only license plate using neural network
        self.img,self.lp_img = Extraction.Extract(self.img)
        self.lp_img_gray = cv2.cvtColor(self.lp_img, cv2.COLOR_RGB2GRAY)
        (thresh, img_bw) = cv2.threshold(self.lp_img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        #cv2.imshow('original', img_bw)

        #convert image to string
        self.lp = pytesseract.image_to_string(img_bw)
        self.lp = self.remove_non_alphanum_chars(self.lp)
        if(self.lp == ""):
            print("Neural Network model did not detect a license plate")
            return
        rowList = self.query_license_plate()
        if(len(rowList) > 0):
            print("Query for license plate # " + self.lp + " returned the following results:")
            print(rowList)
            self.send_email_notification(rowList)
            # cv2.imshow('original', self.img)
            # cv2.imshow('license plate', self.lp_img)
        else:
            print("Query for license plate # " + self.lp + " did not return any results")
        cv2.imshow('original', self.img)
        cv2.imshow('license plate', self.lp_img)
        cv2.waitKey(0)

    """
    Removes characters which are not in the alphabet, nor are they digits 0-9.
    This is used to clean up the license plate of obvious mistakes by the neural network

    parameters:
        - self (unused)
        - s - a string.
    
    returns:
        - s - a string, which has had non-alphanumeric characters removed
    """
    def remove_non_alphanum_chars(self, s):
        for i in range(0, len(s) - 1):
            c = s[i]
            asciVal = ord(c)
            if(not ((asciVal >= 48 and asciVal <= 59) or (asciVal >= 65 and asciVal <= 90))):
                s = s[:i] + s[i+1:]
        return s

    """
    Displays images in a plot typically with the license plate text as a subtitle

    parameters:
        - self (unused)
        - images - a list of images to be displayed
        - title - an optional title which goes on the top bar of the window
        - subtitle - an optional subtitle which is displayed above the images
    
    returns:
        rowList - a list of rows that have been returned from the database query
    """
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

    """
    Queries our mock database using the license plate text

    requires:
        config.json - a json file which has
            "host": the server your database is on (e.g. "localhost" or "127.0.0.1")
            "database": the name of your database (e.g. "amber_alerts")
            "username": a username with read access to your database
            "password": password that goes with the username

    parameters:
        - self 
            - uses self.lp, a string of the license plate text
    
    returns:
        rowList - a list of rows that have been returned from the database query
    """
    def query_license_plate(self):
        with open('config.json', 'r') as readFP:
            config = json.load(readFP)
            #note the auth_plugin parameter allows us to pass our password in a plain, non-encrypted way
            pprint.pprint(config)
            cnx = mysql.connector.connect(host=config["host"],database=config["database"], user=config["username"], password=config["password"], auth_plugin='mysql_native_password')
            cursor = cnx.cursor()
            rowList = set()

            for i in range(0, len(self.lp) - 1):
                lp_copy = self.lp #this is the license plate with some SQL wildcards replacing characters
                lp_copy = lp_copy[:i] + '%' + lp_copy[i + 1:]
                for j in range(i, len(self.lp) - 1):
                    lp_copy = lp_copy[:j] + '%' + lp_copy[j + 1:]
                    #query using LIKE lp_copy
                    query = ("SELECT * from tblAmberAlerts WHERE LicensePlate LIKE '" + lp_copy + "'")
                    cursor.execute(query)
                    for row in cursor:
                        rowList.add(row)
            cnx.close()
        return rowList

    """
    sends an email with an attached picture of the car in question. 
    This function only runs when a query returns at least 1 row, meaning the car might be in the AMBER alert db.

    parameters:
        - self
            - uses self.filepath
        - rowList - a list of data rows returned by query_license_plate
    returns:
        none, void
    """
    def send_email_notification(self, rowList):
        email_sender = 'afake3189@gmail.com'
        email_reciever = 'travisrowe18@gmail.com'
        subject = 'AMBER Alert - Vehicle Tagged!'

        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_reciever
        msg['Subject'] = subject

        #Text variable for license plate?
        body = 'This car may fit the description of one of these vehicles...\n'
        for row in rowList:
            body = body + str(row) + '\n'
        
        # print(body)
        # sys.exit()
        #Attach body to msg for email
        msg.attach(MIMEText(body, 'plain'))

        #Can be any file type (.txt, .jpeg, etc)
        attachment = open(self.filepath,'rb')

        filename = self.filepath.split('/')
        filename = filename[-1].split('\\')
        filename = filename[-1]
        
        #Encodes file to base64 for email then attaches
        part = MIMEBase('application','octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',"attachment; filename= "+ filename)
        msg.attach(part)

        #Converts msg to string
        text = msg.as_string()

        #Establish secure connection
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_sender,'-abc-123')

        #Send email and close connection
        server.sendmail(email_sender,email_reciever,text)
        server.quit()


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
    carPic = CarPicture(fp)
    carPic.process_image()

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