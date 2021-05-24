#Python 3.8.2
##############################
#
#   fsdator.py
#
##############################

from .dator import Dator
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
                path_to_image =  self.path + "/" + name
        else:
            path_to_image =  self.path + name
            
        print(path_to_image)
        cv2.imwrite(path_to_image + ".png", frame)

    def saveSurroundingFrames(self, num_frames, current_frame, name,videopath):
        if(self.path[-1] != "/"):
                path_to_image =  self.path + "/" + name
        else:
            path_to_image =  self.path + name

        init_frame = current_frame - num_frames
        end_frame = current_frame + num_frames

        video_capturer = cv2.VideoCapture(videopath)

        count = init_frame
        video_capturer.set(cv2.CAP_PROP_POS_FRAMES, init_frame)
        name_count = 0
        while count<=end_frame:
            path_to_image2 = path_to_image
            path_to_image2 = path_to_image2 + "." + str(name_count)
            ret,frame = video_capturer.read()
            count+=1

            if(name_count != num_frames):
                cv2.imwrite(path_to_image2 + ".png", frame)

            name_count+=1
