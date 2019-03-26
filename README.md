This is a project which would, in theory, use pictures of license plates to query an AMBER Alert database to see if a car, which matches an AMBER alert description, has passed under a traffic camera.

It uses cv2 for image manipulation and pytesseract to convert the license plate to text in order to query the database.

## Notes on running the program.
This program requires several python packages in order to run. I recommend starting by downloading Tesseract from [the Tesseract Github page](https://github.com/tesseract-ocr/tesseract/wiki).
You will also need to install openCV, pytesseract, and matplotlib to run this.

    $ pip install opencv-python
    $ pip install matplotlib
    $ pip install pytesseract
    
Then run the program using a command such as this

    $ python cam.py image="day_color(small sample)/IMG_0383.jpg"
    
## Temporary notes on running the program.
Currently, the program is not cropping or coloring images on its own, so I recommend running it with the following script for now.

    $ python cam.py image="day_color(small sample)/IMG_0383_crop.jpg"
