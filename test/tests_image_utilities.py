#Python 3.8.2
##############################
#
#   image_utilities.py
#
##############################
import pytest

import cv2
import numpy as np
import os.path
from .argument import Argument
import sys
import  argparse
from src.Analyzers.image_utilities import ImageAnalyzer
from src.Analyzers.video_utilities import VideoAnalyzer
from src.Dators.fsdator import FSDator


################################################
#
# US: 5
#
# Checks if an image is saved
#
################################################
#def test_if_image_is_saved():
#
#    image_analyzer = ImageAnalyzer(50, None, None, None,"test.mp4", None, None)
#    dator = FSDator('.')
#    video_analyzer = VideoAnalyzer(dator, 'test/example_video/test.mp4', True, None, None,None, None,None, None,None,None)
#    cap = video_analyzer.videoCapture

#    ret, frame = cap.read()
#    image_analyzer.saveImage(frame, 'test_image',None,0)  
#    assert os.path.isfile('test_image.png') == True
#    os.remove("test_image.png")

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
    dator = FSDator("test/example_video/")
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
################################################
def test_if_dilate_is_working():
    dator = FSDator("test/example_video/")
    image_analyzer = ImageAnalyzer(50, None, None, None, "test.mp4",None, 8)

    frame1 = cv2.imread('test/example_video/dilate1.png')
    frame2 = cv2.imread('test/example_video/dilate2.png')

    _, detected_impact = image_analyzer.getDifferences(frame1, frame2, 2)

    assert len(detected_impact) == 0