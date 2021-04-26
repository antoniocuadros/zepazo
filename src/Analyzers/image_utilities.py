#Python 3.8.2
##############################
#
#   image_utilities.py
#
##############################
from cv2 import cv2
import numpy as np
import os.path
import math

class ImageAnalyzer:
    """
    This class will represent an Image Analizer with multiple tools for working with images.
    """
    def __init__(self, limit, circlelimit, debug, folder, videoName, num_frames):
        self.mouse_click_count = 0
        self.masks = []
        self.videoName = videoName
        self.num_frames = num_frames

        self.folder = folder
        
        if(debug != None):
            self.debug = debug
        else:
            self.debug = None
            
        if(limit != None):
            self.limit = limit
        else:
            self.limit = 50

        self.circlelimit = circlelimit

        self.impact_count = 0

    
    def saveImage(self, image, name, num_frames, current_frame):
        """
        Save an image in the current working directory.
        :param: image: the image to save.
        :type: image: numpy.ndarray.

        :param: name: name of the image to save.
        :type: frame1: str.

        :return: Returns true if the image is saved correctly.
        :rtype: Boolean.
        """
        path_to_image = ""

        if(self.folder != None):
            if(self.folder[-1] != "/"):
                path_to_image = path_to_image + self.folder + "/" + name
            else:
                path_to_image = path_to_image + self.folder + name
        
        else:
            path_to_image = path_to_image + name

        cv2.imwrite(path_to_image , image)

        print(image["frameNumber"])

    def getDifferences(self, frame1, frame2, current_frame):
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
        _, threshed_img = cv2.threshold(np.array(difference, dtype=np.uint8), self.limit, 255, cv2.THRESH_BINARY)

        #We obtain the contours of the image
        contours, _ = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        

        
        _, ellipse = self.moonEnclosingCircle(frame1)
        
        copy_frame = frame1.copy()
        if(self.debug == True):
            cv2.ellipse(copy_frame, ellipse,(0, 255, 255), 2)

        #for each contour finded we draw a rectangle and we save the image
        if (len(contours) > 0):
            
            for c in contours:
                x, y, w, h = cv2.boundingRect(c)
                if(ellipse != None):
                    if(self.inside_moon(ellipse, x, y, frame1)):                                #Possible impact! Inside Moon
                        cv2.rectangle(copy_frame, (x-10, y-10), (x+w+10, y+h+10), (0, 0, 255), 2)
                        if(self.debug != True):
                            self.saveImage(copy_frame, os.path.basename(self.videoName) + "_" + str(self.impact_count) + ".png", self.num_frames, current_frame)
                            self.impact_count = self.impact_count + 1
                    else:                                                                     #False positive! Discarded
                        cv2.rectangle(copy_frame, (x-10, y-10), (x+w+10, y+h+10), (255, 0, 255), 2)
                else:                                                                                   #No ellipse obtained, Possible impact!
                    cv2.rectangle(copy_frame, (x-10, y-10), (x+w+10, y+h+10), (0, 255, 0), 2)
                    if(self.debug != True):
                        self.saveImage(copy_frame, self.videoName + "_" + str(self.impact_count) + ".png", self.num_frames, current_frame)
                        self.impact_count = self.impact_count + 1
                #cv2.imwrite(self.videoPath + "_" + str(impact_count) + ".png", frame1)
                
        if(self.debug):
            return copy_frame
        else:
            return frame1


    def moonEnclosingCircle(self, frame):
        """
        Gets moon center as X,Y coordinates
        :param: frame: video frame.
        :type: frame1: numpy.ndarray.


        :return: Returns moon center as X,Y coordinates
        :rtype: Integer
        """
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #We get the moon thresed with the moon in white and the rest in black
        #variate 25         

        if(self.circlelimit != None):
            umbral = int(self.circlelimit)
        else:
            umbral = np.average(grayFrame) - np.std(grayFrame)
    
        _, threshed_moon = cv2.threshold(np.array(grayFrame, dtype=np.uint8), umbral, 255, cv2.THRESH_BINARY)

        #With the threshed image of the moon we can obtain the moon contour
        moon_contour, _ = cv2.findContours(threshed_moon, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        
        #With the previous contour now we try to get the circle containing the moon 
        c = []
        if(len(moon_contour) > 0):
            c = max(moon_contour, key=cv2.contourArea)

        if(len(c) > 5):
            ellipse = cv2.fitEllipse(c)
        

        #Uncomment to see the centter
        #cv2.circle(grayFrame, (int(ellipse[0][0]), int(ellipse[0][1])), 6, (0, 0, 255), -1)

        #Uncomment to see the ellipse around the moon
        #cv2.ellipse(grayFrame, ellipse,(0, 255, 255), 2)
        if(len(c) > 5):
            centerX = ellipse[0][0]
            centerY = ellipse[0][1]
            return umbral, ellipse
        else:
            return 0, None

    def selectMaskLocation(self, first_frame, num_masks):
        """
        Gets masks points and show masks util a key is pressed
        :param: first_frame: video frame.
        :type: first_frame: numpy.ndarray.

        :param: num_masks: number of masks to apply.
        :type: num_masks: int.


        :return: Returns masks as coordinates
        :rtype: list
        """
        #We show the first frame in order to let the user decide where to place the mask
        cv2.imshow("Select top-left corner and bottom-right corner to apply a mask",first_frame)

        cv2.setMouseCallback('Select top-left corner and bottom-right corner to apply a mask', self.get_mouse_click_coordinates, [first_frame,num_masks])

        #Waits for a key event
        cv2.waitKey(0)

        #Closes the window
        cv2.destroyAllWindows()

        return self.masks


    def get_mouse_click_coordinates(self, event, x, y, flags, params):
        """
        Tracks mouse click event to get x,y coordinates in order to create masks
        :param: event: event object to track mouse click.
        :type: event: event object.

        :param: x: x coordinate of mouse click.
        :type: x: int.


        :param: y: y coordinate of mouse click.
        :type: y: int.

        :param: flags: flags to control envents.
        :type: flags: flag.


        :param: params: list of params like frame or num_masks
        :type: params: list.
        """
        frame = params[0]
        num_masks = params[1]

        num_clicks = num_masks * 2

        if ( event == cv2.EVENT_LBUTTONDOWN ):
            #Add 1 to mouse clicks
            self.mouse_click_count = self.mouse_click_count + 1
            
            if(self.mouse_click_count < num_clicks):
                #Places a circular indicator in clicked point
                cv2.circle(frame, (x,y),3,(0,0,255),-1)
                #Shows the image with that point
                cv2.imshow("Select top-left corner and bottom-right corner to apply a mask",frame)

                self.masks.append([x,y])

                if(self.mouse_click_count % 2 == 0 and self.mouse_click_count != 0) :
                    cv2.rectangle(frame, 
                    (self.masks[self.mouse_click_count-2][0], self.masks[self.mouse_click_count-2][1]),
                     (self.masks[self.mouse_click_count-1][0], self.masks[self.mouse_click_count-1][1]),
                      (0,0,255), -1)
                    cv2.imshow("Select top-left corner and bottom-right corner to apply a mask",frame)


            else:
                if(self.mouse_click_count == num_clicks):
                    #Places a circular indicator in clicked point
                    cv2.circle(frame, (x,y),3,(0,0,255),-1)
                    #Shows the image with that point
                    cv2.imshow("Select top-left corner and bottom-right corner to apply a mask",frame)
                    
                    #Gets last point
                    self.masks.append([x,y])

                    cv2.rectangle(frame, 
                    (self.masks[self.mouse_click_count-2][0], self.masks[self.mouse_click_count-2][1]),
                     (self.masks[self.mouse_click_count-1][0], self.masks[self.mouse_click_count-1][1]),
                      (0,0,255), -1)

                    cv2.imshow("Select top-left corner and bottom-right corner to apply a mask",frame)

    def inside_moon(self, ellipse, point_x,point_y, frame):
        """
        Checks if a point is inside an rotated ellipse
        :param: ellipse: ellipse object that shapes moon.
        :type: ellipse: cv2.ellipse.

        :param: point_x: x coordinate of a point.
        :type: point_x: int.

        :param: point_y: y coordinate of a point.
        :type: point_y: int.

        :return: Returns true if point is inside the rotated ellipse, otherwise false
        :rtype: bool.
        """
        axis1 = ellipse[1][0]
        axis2 = ellipse[1][1]

        centerX = ellipse[0][0]
        centerY = ellipse[0][1]

        if(axis1 > axis2):
            minor_axis = axis2
            mayor_axis = axis1
        else:
            minor_axis = axis1
            mayor_axis = axis2

        angle = math.radians(ellipse[2])
        
        x = (pow((math.cos(angle)*(point_x - centerX) + math.sin(angle)*(point_y - centerY)), 2) / pow(axis1/2,2)) + (pow((math.sin(angle)*(point_x - centerX) - math.cos(angle)*(point_y - centerY)), 2) / pow(axis2/2,2))

        if(x <= 1):
            return True
        else:
            return False


    def selectCircleLimitArgument(self, circlelimit, first_frame):
        copy_frame = first_frame.copy()
        
        if(circlelimit != None):
            self.circlelimit = int(circlelimit)
        else:
            self.circlelimit = None
            umbral, ellipse = self.moonEnclosingCircle(copy_frame)
            self.circlelimit = umbral

        _, ellipse = self.moonEnclosingCircle(copy_frame)
        cv2.ellipse(copy_frame, ellipse,(0, 255, 255), 2)
        return copy_frame, self.circlelimit