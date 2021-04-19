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


################################################
#
# US: 5
#
# Checks if an image is saved
#
################################################
def test_if_image_is_saved():

    image_analyzer = ImageAnalyzer(50, None, None)
    video_analyzer = VideoAnalyzer('test/example_video/test.mp4', True, None, None)
    cap = video_analyzer.videoCapture

    ret, frame = cap.read()
    image_analyzer.saveImage(frame, 'test_image')  
    assert os.path.isfile('test_image.png') == True
    os.remove("test_image.png")

################################################
#
#
#
# Checks if an image is obtained as two frame difference
#
################################################

def test_if_difference_image_is_ok():

    image_analyzer = ImageAnalyzer(50, None, None)
    video_analyzer = VideoAnalyzer('test/example_video/test.mp4', True, None, None)
    cap = video_analyzer.videoCapture

    ret, frame = cap.read()
    resulting_frame = image_analyzer.getDifferences(frame, frame)  
    assert np.max(resulting_frame[0][0]) <= 1