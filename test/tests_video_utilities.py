#Python 3.8.2
##############################
#
#   tests_image_utilities.py
#
##############################
import pytest
import sys
sys.path.append("..")
from src.Analyzers.image_utilities import ImageAnalyzer
from src.Analyzers.video_utilities import VideoAnalyzer



def test_if_object_is_created_ok():
    args['video'] =  '../videos/test.mp4'
    video_analizer = VideoAnalizer(args)

    assert video_analizer.videoPath == '../videos/test.mp4'  
