#Python 3.8.2
##############################
#
#   video_utilities.py
#
##############################

import cv2
import numpy as np

class VideoAnalizer:
    videoPath = None

    #Constructor
    #Gets the video path
    def __init__(self, videoPath):
        self.videoPath = videoPath


    #Analize the video frame per frame
    def analyze(self):
        cap=cv2.VideoCapture(self.videoPath)
        while(cap.isOpened()):
            ret, frame=cap.read() #read a single frame, ret will be true if frame captured
            cv2.imshow('output', frame)
            
            if(cv2.waitKey(1) & 0xFF == ord('q')):
                play = False

        cap.release()
        cv2.destroyAllWindows()