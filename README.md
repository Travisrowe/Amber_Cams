This is a proof-of-concept project which would, in theory, use pictures of license plates to query an AMBER Alert database to see if a car, which matches an AMBER alert description, has passed under a traffic camera.

It uses cv2 for image manipulation and pytesseract to convert the license plate to text in order to query our local, mock database.

## Notes on running the program.

This program requires several python packages in order to run. I recommend starting by downloading Tesseract from [the Tesseract Github page](https://github.com/tesseract-ocr/tesseract/wiki) and following their instructions on installation.
You will also need to install several python packages to run this. I recommend using pip, like so.

    $ pip install opencv-python
    $ pip install matplotlib
    $ pip install pytesseract
    $ pip install mysql-connector-python
    $ pip install email
    
Then run the program using a command with file paths relative to the directory which contains cam.py. For example

    $ python cam.py "day_color(small sample)/IMG_0378.jpg"
    
### Extraction.py credit

Credit and thanks to Link009 and Chris Dahms for the neural network which crops these car images down to just the license plates.
Chris Dahms developed the code which Link009 modified. You can find [Link009's repository here](https://github.com/Link009/LPEX), and [Chris Dahm's repository here](https://github.com/MicrocontrollersAndMore/OpenCV_3_License_Plate_Recognition_Python)

### Developer credit

Credit also goes to Ernest Hernandez and Keona Rollerson for this project. 