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
        video = cv2.VideoCapture('videoPath')

        while(video.isOpened()):
            frame = cap.read()
            cv2.imshow("frame", frame)
            
        cap.release()
        cv2.destroyAllWindows()