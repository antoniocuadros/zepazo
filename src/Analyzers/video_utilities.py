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
from .image_utilities import ImageAnalyzer


class VideoAnalyzer:
    """
    This class will represent a Video Analizer with multiple tools for working with video.
    """

    #Constructor
    #Gets the video path
    def __init__(self, args):
        """
        Inits VideoAnalyzer with the data of the selected video.

        :param args: arguments given by user.
        """

        # -> VideoPath: video to analize
        # -> VideoCaputre: cv2 object to analize the video
        self.videoPath = args.video
        self.videoCapture = cv2.VideoCapture(self.videoPath)
        self.showVideo = args.show

        if not (self.videoCapture).isOpened():
            raise Exception("Video could not be found on this path")

        # -> Object to work with images
        self.imageAnalizer = ImageAnalyzer()

        #Gets: 
        # -> frames
        # -> fps
        # -> seconds
        self.__getGeneralVideoStats(self.videoCapture)

        #Show info about the video
        self.showVideoInfo()

    #Analize the video frame per frame
    def analyze(self):
        """
        Analyzes the video to detect lunar impacts.
        """
        cap = self.videoCapture
        play = True

        while(cap.isOpened() and play):
            ret, frame=cap.read() #read a single frame, ret will be true if frame captured
            ret, frame2=cap.read()
            #If there are frames left
            if ret == True:    
                frame = (self.imageAnalizer).getDifferences(frame, frame2)
                if self.showVideo: 
                    self.showFrame(frame)

                if(cv2.waitKey(100) & 0xFF == ord('q')):
                    play = False
            #No more frames, exit loop
            else:
                play = False
        
        cap.release()
        cv2.destroyAllWindows()

    def __getGeneralVideoStats(self, cap):
        """
        Gets the values for 'frames', 'fps', 'seconds' and saves them as attributes.

        :param cap: videoCapture cv2 object.
        """
        #video total frames
        self.frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        #frames per second 
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))
        #video duration in seconds 
        self.seconds = int(self.frames / self.fps)
    
    def getCurrentTime(self, cap):
        """
        Gets the current time of a of a video playing when is called.

        :param cap: videoCapture cv2 object.
        """
        
        self.__getGeneralVideoStats(cap)
        current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        return str(datetime.timedelta(seconds = current_frame / self.fps))

    def showFrame(self, frame):
        """
        Displays a frame on screen.

        :param frame: video frame.
        """
        
        cv2.imshow(ntpath.basename(self.videoPath),frame)
        
    def showVideoInfo(self):
        """
        Displays a general information about the video.
        """

        print("Video Path:         ", self.videoPath)
        print("FPS:                ", self.fps)
        print("Total Frames:       ", self.frames)
        print("Duration: ", str(datetime.timedelta(seconds=self.seconds)))
        

