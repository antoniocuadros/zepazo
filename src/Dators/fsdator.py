#Python 3.8.2
##############################
#
#   dator.py
#
##############################

from dator import Dator
import os
from cv2 import cv2

class FSDator(Dator):
    """
    This class will implement Dator methods to save data in files and folders.
    """
    def __init__(self, path):
        #Checks if folder in path exists
        if(path !=None and os.path.exists(path) == False): #Folder doesn't exists, we create it
            os.mkdir(path)
        
        self.path = path



    
    def saveFrame(self, name, frame):
        path_to_image = ""
        if(self.path[-1] != "/"):
                path_to_image = path_to_image + self.path + "/" + name
        else:
            path_to_image = path_to_image + self.path + name

        cv2.imwrite(path_to_image + ".png", frame)
