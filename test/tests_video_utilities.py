#Python 3.8.2
##############################
#
#   tests_image_utilities.py
#
##############################
import pytest
import sys
import  argparse

from src.Analyzers.image_utilities import ImageAnalyzer
from src.Analyzers.video_utilities import VideoAnalyzer

class Argument:
    def __init__(self, videopath, show):
        self.video = videopath
        self.show = show

def test_if_object_is_created_ok():

    arguments = Argument('videos/test.mp4', 'False')

    video_analizer = VideoAnalyzer(arguments)

    assert video_analizer.videoPath == 'videos/test.mp4'  
