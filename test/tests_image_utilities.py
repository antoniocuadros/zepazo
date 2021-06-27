#Python 3.8.2
##############################
#
#   image_utilities.py
#
##############################
import pytest

import cv2
import numpy as np
from src.Analyzers.image_utilities import ImageAnalyzer
from src.Analyzers.video_utilities import VideoAnalyzer
from src.Dators.fsdator import FSDator


################################################
#
#
#
# Checks if an image is obtained as two frame difference
#
################################################

def test_if_difference_image_is_ok():
    dator = FSDator("test.mp4")
    image_analyzer = ImageAnalyzer(50, None, None, None, "test.mp4",None, None)
    video_analyzer = VideoAnalyzer(dator, 'test/example_video/test.mp4', True, None, None,None, None,None, None,None,None)
    cap = video_analyzer.videoCapture

    ret, frame = cap.read()
    resulting_frame, impact = image_analyzer.getDifferences(frame, frame, 1)  
    assert np.max(resulting_frame[0][0]) <= 1

################################################
# 
# [US7] Getting frame differences
# Checks if two images with some differences
# returns possible impacts due to its differences
#
################################################
def test_if_difference_images_working():
    image_analyzer = ImageAnalyzer(50, None, None, None, "test.mp4",None, None)

    frame1 = cv2.imread('test/example_video/dilate1.png')
    frame2 = cv2.imread('test/example_video/dilate2.png')

    _, detected_impact = image_analyzer.getDifferences(frame1, frame2, 2)

    assert len(detected_impact) > 0



################################################
# 
# [US16] Dilate images
# Checks if dilate method if workig by dilating a
# problematic frame and substracting with a previous one
# impact count must be 0
#
################################################
def test_if_dilate_is_working():
    image_analyzer = ImageAnalyzer(50, None, None, None, "test.mp4",None, 8)

    frame1 = cv2.imread('test/example_video/dilate1.png')
    frame2 = cv2.imread('test/example_video/dilate2.png')

    _, detected_impact = image_analyzer.getDifferences(frame1, frame2, 2)

    assert len(detected_impact) == 0

################################################
# 
# [US26] Moon Enclosing ellipse
# Checks if in a typical frame we can obtain 
# the moon outline
#
################################################

def test_if_moon_outline_is_obtained():
    image_analyzer = ImageAnalyzer(50, None, 41, None, "test.mp4",None, None)
    frame1 = cv2.imread('test/example_video/ellipse.png')

    umb, ellipse = image_analyzer.moonEnclosingCircle(frame1)

    assert ellipse != None

################################################
# 
# [US26] Moon Enclosing ellipse
# Checks if in a non typical frame we can not obtain 
# the moon outline
#
################################################

def test_if_moon_outline_is_not_obtained():
    image_analyzer = ImageAnalyzer(50, None, None, None, "test.mp4",None, None)
    frame1 = cv2.imread('test/example_video/dilate1.png')

    umb, ellipse = image_analyzer.moonEnclosingCircle(frame1)

    assert ellipse == None

################################################
# 
# [US26] Moon Enclosing ellipse
# Checks if we define an threshold it uses that value
#
################################################

def test_if_defined_threshold_is_used():
    image_analyzer = ImageAnalyzer(50, 41, None, None, "test.mp4",None, None)
    frame1 = cv2.imread('test/example_video/ellipse.png')

    threshold, ellipse = image_analyzer.moonEnclosingCircle(frame1)

    assert threshold == 41


################################################
# 
# [US26] Moon Enclosing ellipse
# Checks if we dont define an threshold it calculate that value
#
################################################

def test_if_threshold_is_calculated():
    image_analyzer = ImageAnalyzer(50, None, None, None, "test.mp4",None, None)
    frame1 = cv2.imread('test/example_video/ellipse.png')

    threshold, ellipse = image_analyzer.moonEnclosingCircle(frame1)

    assert int(threshold) == 34

################################################
# 
# [US7.1] Marking impacts
# Checks if when an impact is detected it is marked
#
################################################
def test_if_marking_impacts_is_working():
    image_analyzer = ImageAnalyzer(50, None, None, None, "test.mp4",None, None)

    frame1 = cv2.imread('test/example_video/dilate1.png')
    frame2 = cv2.imread('test/example_video/dilate2.png')

    frame, detected_impact = image_analyzer.getDifferences(frame1, frame2, 2)

    #Impact detected so marked
    assert len(detected_impact) > 0

    #checks bit by bit if there are differences between marked and non marked
    assert (np.bitwise_xor(frame,frame2).any())


################################################
# 
# [US27] Checking if impacts takes place inside moon
# Checks if an impact is detected inside the moon surface
#
################################################
def test_if_impact_takes_place_inside_moon_is_deected():
    image_analyzer = ImageAnalyzer(50, None, None, None, "test.mp4",None, None)
    frame1 = cv2.imread('test/example_video/ellipse.png')

    _, ellipse = image_analyzer.moonEnclosingCircle(frame1)

    inside = image_analyzer.inside_moon(ellipse, 100,100)
    
    assert inside == True


################################################
# 
# [US27] Checking if impacts takes place inside moon
# Checks if an impact is detected outside the moon surface
#
################################################
def test_if_impact_doesnt_place_inside_moon_is_deected():
    image_analyzer = ImageAnalyzer(50, None, None, None, "test.mp4",None, None)
    frame1 = cv2.imread('test/example_video/ellipse.png')

    _, ellipse = image_analyzer.moonEnclosingCircle(frame1)

    inside = image_analyzer.inside_moon(ellipse, 1600,1600)
    
    assert inside == False