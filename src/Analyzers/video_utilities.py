#Python 3.8.2
##############################
#
#   video_utilities.py
#
##############################

from cv2 import cv2
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
        self.imageAnalizer = ImageAnalyzer(args.detectionlimit)

        # -> Mask points
        self.mask_points = []

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

            #Apply the mask for each frame
            if(len(self.mask_points) > 0 and len(self.mask_points) % 2 == 0):
                for i in range(len(self.mask_points)//2):
                    cv2.rectangle(frame, (self.mask_points[2*i][0],self.mask_points[2*i][1]), (self.mask_points[2*i+1][0],self.mask_points[2*i+1][1]), (0,0,255), -1)
                    cv2.rectangle(frame2, (self.mask_points[2*i][0],self.mask_points[2*i][1]), (self.mask_points[2*i+1][0],self.mask_points[2*i+1][1]), (0,0,255), -1)


            #If there are frames left
            if ret == True:    
                frame = (self.imageAnalizer).getDifferences(frame, frame2)
                moon_center_x, moon_center_y, ellipse = self.imageAnalizer.moonEnclosingCircle(frame)
                cv2.ellipse(frame, ellipse,(0, 255, 255), 2)

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
        return frame
        
    def showVideoInfo(self):
        """
        Displays a general information about the video.
        """

        print("Video Path:         ", self.videoPath)
        print("FPS:                ", self.fps)
        print("Total Frames:       ", self.frames)
        print("Duration: ", str(datetime.timedelta(seconds=self.seconds)))
        

    def getInitialFrame(self):
        """
        Gets initial frame from a source video
        
        :return: Returns first frame
        :rtype: numpy.ndarray
        """
        ret, frame = self.videoCapture.read()
        
        if( ret ):
            return frame
        else:
            return False

    def selectAndApplyMask(self, num_masks, points=None):
        """
        Gets points as attribute to use while analyzing

        :param: num_masks: number of masks to get coordinates
        :type: num_masks: int


        :param: points: points to use as masks
        :type: points: list
        """

        if(points == None): #Came from mousemask
            self.mask_points = self.imageAnalizer.selectMaskLocation(self.getInitialFrame(), num_masks)
            
        else:
            #We have a list of points
            for i in range(len(points)//2):
                self.mask_points.append( [ points[2*i], points[2*i+1] ] )