#Python 3.8.2
##############################
#
#   image_utilities.py
#
##############################

import cv2
import numpy as np
import os.path

class ImageAnalyzer:
    """
    This class will represent an Image Analizer with multiple tools for working with images.
    """
    def __init__(self):
        self.mouse_click_count = 0
        self.masks = []
    
    def saveImage(image, name):
        """
        Save an image in the current working directory.
        :param: image: the image to save.
        :type: image: numpy.ndarray.

        :param: name: name of the image to save.
        :type: frame1: str.

        :return: Returns true if the image is saved correctly.
        :rtype: Boolean.
        """

        #Check if filename exists
        if (os.path.isfile(name +'.png')):
            return False
        else: 
            cv2.imwrite(name + ".png", image)
            return True

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

            #cv2.imwrite(self.videoPath + "_" + str(impact_count) + ".png", frame1)
            impact_count = impact_count + 1

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
        ret, threshed_moon = cv2.threshold(np.array(grayFrame, dtype=np.uint8), 35, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 5),np.uint8)

        #With the threshed image of the moon we can obtain the moon contour
        moon_contour, hier = cv2.findContours(threshed_moon, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        
        #With the previous contour now we try to get the circle containing the moon 
        c = max(moon_contour, key=cv2.contourArea)
        
        ellipse = cv2.fitEllipse(c)
        

        #Uncomment to see the centter
        #cv2.circle(grayFrame, (int(ellipse[0][0]), int(ellipse[0][1])), 6, (0, 0, 255), -1)

        #Uncomment to see the ellipse around the moon
        #cv2.ellipse(grayFrame, ellipse,(0, 255, 255), 2)

        centerX = ellipse[0][0]
        centerY = ellipse[0][1]
        
        
        return centerX, centerY, ellipse

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
