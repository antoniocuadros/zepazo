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
    """
    This class will represent a Video Analizer with multiple tools for working with video.
    """

    #Constructor
    #Gets the video path
    def __init__(self, args):
        """
        Inits VideoAnalizer with the data of the selected video.

        :param args: arguments given by user.
        """

        # -> VideoPath: video to analize
        # -> VideoCaputre: cv2 object to analize the video
        self.videoPath = args.video
        self.videoCapture = cv2.VideoCapture(self.videoPath)
        self.showVideo = args.show

        if not (self.videoCapture).isOpened():
            raise Exception("Video could not be found on this path")

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
                if self.showVideo: 
                    #self.showFrame(frame)
                    self.getDifferences(frame, frame2)

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
        self.frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) 
        self.fps = int(cap.get(cv2.CAP_PROP_FPS)) 
        self.seconds = int(self.frames / self.fps)
    
    def __getCurrentTime(self, cap):
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

            cv2.imwrite(self.videoPath + "_" + str(impact_count) + ".png", frame1)
            impact_count = impact_count + 1

        
        
        self.showFrame(frame1)