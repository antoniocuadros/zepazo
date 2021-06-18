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
from pathlib import Path
import mimetypes
import os
import os.path, time
from .image_utilities import ImageAnalyzer


class VideoAnalyzer:
    """
    This class will represent a Video Analizer with multiple tools for working with video.
    """

    #Constructor
    #Gets the video path
    def __init__(self, dator, video, show, detectionlimit, circlelimit, masks, folder, num_frames_save, dilate, startingFrame, endingFrame):
        """
        Inits VideoAnalyzer with the data of the selected video.

        :param args: arguments given by user.
        """

        if(dator.videoExists(video)):
            # -> VideoPath: video to analize
            # -> VideoCaputre: cv2 object to analize the video
            self.videoPath = video
            self.videoCapture = cv2.VideoCapture(self.videoPath)
            self.showVideo = show

            self.folder = folder
            self.num_frames_save = num_frames_save
            self.current_frame = 0

            self.impacts = []
            self.dator = dator
            self.startingFrame = startingFrame
            self.endingFrame = endingFrame

            if(self.startingFrame != None):
                self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES, self.startingFrame)
                self.current_frame = self.startingFrame 

            if not (self.videoCapture).isOpened():
                raise Exception("Video could not be found on this path")

            # -> Object to work with images
            if(detectionlimit != None):
                self.imageAnalizer = ImageAnalyzer(detectionlimit, circlelimit, show, self.folder, self.videoPath, self.num_frames_save, dilate)
            else:
                self.imageAnalizer = ImageAnalyzer(None, circlelimit, show,self.folder, self.videoPath, self.num_frames_save, dilate)

            # -> Mask points
            if(masks != None):
                self.mask_points = masks
            else:
                self.mask_points = []

            #Gets: 
            # -> frames
            # -> fps
            # -> seconds
            self.__getGeneralVideoStats(self.videoCapture)

            #Show info about the video
            if(self.showVideo != True):
                self.showVideoInfo()
        else:
            raise Exception("Video could not be found on this path or incorrect file type")




    def checkVideo(self, path):
        file = Path(path)
        if(file.is_file() == False):
            return False
        else:
            try:
                if(mimetypes.guess_type(path)[0].startswith('video') == False):
                    return False
            except:
                return False
            else:
                return True

    #Analize the video frame per frame
    def analyze(self, fps, num_frames_show):
        """
        Analyzes the video to detect lunar impacts.
        """
        cap = self.videoCapture
        play = True

        if(fps == None and num_frames_show == None):
            fps = 10
            num_frames_show = self.frames

        while(cap.isOpened() and play):
            if(self.endingFrame != None and self.endingFrame <= self.current_frame):
                play = False

            num_frames_show = num_frames_show - 1
            ret, frame=cap.read() #read a single frame, ret will be true if frame captured
            ret, frame2=cap.read()

            frame, frame2 = self.applyMasks(frame, frame2)


            #If there are frames left
            if ret == True:    
                frame, impact = (self.imageAnalizer).getDifferences(frame, frame2, self.current_frame)

                if(impact != None and len(impact) > 0):
                    for i in impact:
                        self.impacts.append(i)

                if self.showVideo: 
                    resized_frame = cv2.resize(frame, (1600,900))
                    self.showFrame(resized_frame)

                if(cv2.waitKey(fps) & 0xFF == ord('q')):
                    play = False
            
            #No more frames, exit loop
            else:
                play = False
            self.current_frame = self.current_frame + 1
        
        cap.release()
        cv2.destroyAllWindows()


        #We save all impacts
        self.saveAllImpacts()

        #Generate logfile
        self.saveLogFile()

    
    def saveAllImpacts(self):
        for impact in self.impacts:

            impact.setTime(self.getRealImpactTime(impact.frame_number))

            #self.imageAnalizer.saveImage(impact.frame, os.path.basename(self.videoPath) + "_" + str(impact.impact_number), self.num_frames, impact.frame_number)
            name = os.path.basename(self.videoPath) + "_" + str(impact.impact_number)
            if(self.dator != None):
                self.dator.saveFrame(name, impact.frame)
                
                if(self.num_frames_save != None):
                    self.dator.saveSurroundingFrames(self.num_frames_save, impact.frame_number, name, self.videoPath)

    
    def saveLogFile(self):
        if(self.dator != None):
            self.dator.saveLog(self.impacts)


    def applyMasks(self, frame, frame2):
        #Apply the mask for each frame
        if(len(self.mask_points) > 0):
            if(len(self.mask_points) > 0 and len(self.mask_points) % 2 == 0):
                for i in range(len(self.mask_points)//2):
                    #IMPORTANT: Masks now in black color due to dilate argument
                    cv2.rectangle(frame, (self.mask_points[2*i][0],self.mask_points[2*i][1]), (self.mask_points[2*i+1][0],self.mask_points[2*i+1][1]), (0,0,0), -1)
                    cv2.rectangle(frame2, (self.mask_points[2*i][0],self.mask_points[2*i][1]), (self.mask_points[2*i+1][0],self.mask_points[2*i+1][1]), (0,0,0), -1)
        return frame, frame2

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
    
    def getCurrentTime(self, current_frame):
        """
        Gets the current time of a of a video playing when is called.

        :param current_frame: current frame to get the time.
        """

        return str(datetime.timedelta(seconds = current_frame*2 / self.fps))

    def getRealImpactTime(self, current_frame):
        creation_file_time = os.path.getmtime(self.videoPath)
        #Moment of creation
        #Format: XX:XX:XX
        creation_file_time_formated = str(datetime.datetime.fromtimestamp(creation_file_time).strftime('%H:%M:%S'))
        creation_file_time_formated_H = creation_file_time_formated[0] + creation_file_time_formated[1]
        creation_file_time_formated_M = creation_file_time_formated[3] + creation_file_time_formated[4]
        creation_file_time_formated_S = creation_file_time_formated[6] + creation_file_time_formated[7]

        #Moment of impact
        #Format:X:XX:XX
        moment_impact = self.getCurrentTime(current_frame)

        moment_impact_H = moment_impact[0]
        moment_impact_M = moment_impact[2] + moment_impact[3]
        moment_impact_S = moment_impact[5] + moment_impact[6]

        #Video length
        #Format:X:XX:XX
        video_time = str(datetime.timedelta(seconds=self.seconds))
        video_time_H = video_time[0]
        video_time_M = video_time[2] + video_time[3]
        video_time_S = video_time[5] + video_time[6]
        
        #Substract the file creation time the duration time to get the initial time when the recording started
        substract_H = int(creation_file_time_formated_H) - int(video_time_H)
        substract_M = int(creation_file_time_formated_M) - int(video_time_M)
        substract_S = int(creation_file_time_formated_S) - int(video_time_S)

        #We have the original time, now add the impact time

        add_H = int(substract_H) + int(moment_impact_H)
        add_M = int(substract_M) + int(moment_impact_M)
        add_S = int(substract_S) + int(moment_impact_S)

        return str(add_H) + ":" + str(add_M) + ":" + str(add_S)

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

    def selectAndApplyCircleLimitArgment(self, circlelimit, first_frame):
        frame = first_frame
        frame_result, limit = self.imageAnalizer.selectCircleLimitArgument(circlelimit, frame)
        return frame_result, limit

    
    def showASample(self):
        frames = self.frames
        fps = self.fps
        if(fps >= 100):
            fps = 25
        seconds = 20
        
        frames = self.frames
        fps = self.fps
        if(fps >= 100):
            fps = 25
        seconds = 20
        
        #We want to display a sample of 20 seconds
        num_frames_show = seconds * fps
        
        self.analyze(fps, num_frames_show)
