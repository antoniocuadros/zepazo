#Python 3.8.2
##############################
#
#   video_utilities.py
#
##############################

import cv2
import numpy as np
import datetime 
import ntpath

class VideoAnalizer:
    videoPath = None
    fps = None
    frames = None
    seconds = None

    #Constructor
    #Gets the video path
    def __init__(self, videoPath):
        self.videoPath = videoPath


    #Analize the video frame per frame
    def analyze(self):
        #Play the video
        cap = cv2.VideoCapture(self.videoPath)
        
        #If we dont find the file, error
        if (cap.isOpened()== False): 
            print("Video could not be found on this path")

        #We find the file
        else:

            play = True

            while(cap.isOpened() and play):
                ret, frame=cap.read() #read a single frame, ret will be true if frame captured
                
                #If there are frames left
                if ret == True:
                    cv2.imshow(ntpath.basename(self.videoPath),frame)
                    if(cv2.waitKey(1) & 0xFF == ord('q')):
                        play = False
                #No more frames, exit loop
                else:
                    play = False
            
            cap.release()
            cv2.destroyAllWindows()


        


        