#Python 3.8.2
##############################
#
#   image_utilities.py
#
##############################

import cv2
import numpy as np
import os.path

class ImageAnalizer:
    """
    This class will represent an Image Analizer with multiple tools for working with images.
    """
    def __init__:
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