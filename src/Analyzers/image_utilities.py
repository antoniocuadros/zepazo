#Python 3.8.2
##############################
#
#   image_utilities.py
#
##############################

import cv2
import numpy as np
import os.path

class ImageAnalyzer:
    """
    This class will represent an Image Analizer with multiple tools for working with images.
    """
    def __init__(self):
        pass
    
    def saveImage(image, name):
        """
        Save an image in the current working directory.
        :param: image: the image to save.
        :type: image: numpy.ndarray.

        :param: name: name of the image to save.
        :type: frame1: str.

        :return: Returns true if the image is saved correctly.
        :rtype: Boolean.
        """

        #Check if filename exists
        if (os.path.isfile(name +'.png')):
            return False
        else: 
            cv2.imwrite(name + ".png", image)
            return True

    def getDifferences(self, frame1, frame2):
        """
        Subtract the two frames to get the differences.
        :param: frame1: video frame 1.
        :type: frame1: numpy.ndarray.

        :param: frame2: video frame 2.
        :type: frame1: numpy.ndarray.

        :return: Returns a new frame resulting from subtracting frame2 from frame1
        :rtype: numpy.ndarray.
        """
        
        #reserve memory for the resulting image
        difference = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

        #from RGB space to GrayScale space for simplicity
        grayFrame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        grayFrame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        #get the difference between frame1 and frame2
        difference = cv2.subtract(grayFrame1, grayFrame2, difference)

        #For each pixel, if the pixel value is smaller than a value (second argument: 50) 
        #it is set to 0 (white), if not the pixel is set to a maximum value (third argument) (black)
        ret, threshed_img = cv2.threshold(np.array(difference, dtype=np.uint8), 50, 255, cv2.THRESH_BINARY)

        #We obtain the contours of the image
        contours, _ = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        impact_count = 0
        #for each contour finded we draw a rectangle and we save the image
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x-10, y-10), (x+w+10, y+h+10), (0, 0, 255), 2)

            #cv2.imwrite(self.videoPath + "_" + str(impact_count) + ".png", frame1)
            impact_count = impact_count + 1

        return frame1