#Python 3.8.2
##############################
#
#   image_utilities.py
#
##############################

import cv2
import numpy as np
import os.path
from .argument import Argument

import pytest
import sys
import  argparse
import numpy as np
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

    image_analyzer = ImageAnalyzer
    arguments = Argument('videos/test.mp4', 'True')
    video_analyzer = VideoAnalyzer(arguments)
    cap = video_analyzer.videoCapture

    ret, frame = cap.read()

    image_analyzer.saveImage(frame, 'test_image')  