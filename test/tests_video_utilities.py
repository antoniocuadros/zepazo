#Python 3.8.2
##############################
#
#   tests_video_utilities.py
#
##############################
import pytest
import sys
import  argparse
import numpy as np
from src.Analyzers.image_utilities import ImageAnalyzer
from src.Analyzers.video_utilities import VideoAnalyzer

class Argument:
    def __init__(self, videopath, show):
        self.video = videopath
        self.show = show

################################################
#
# US: 1
#
# Checks if the videopath is correctly obtained
#
################################################
def test_if_object_is_created_ok():

    arguments = Argument('videos/test.mp4', 'False')

    video_analizer = VideoAnalyzer(arguments)

    assert video_analizer.videoPath == 'videos/test.mp4'  

################################################
#
# US: 1
#
# Checks if the path does not exist fails
#
################################################
def test_if_object_is_created_with_error():

    arguments = Argument('videos/testttt.mp4', 'False')

    with pytest.raises(Exception) as e:
        video_analiyzer = VideoAnalyzer(arguments)

    assert str(e.value) == "Video could not be found on this path"

################################################
#
# US: 2
#
# Checks if the current time method works
#
################################################
def test_if_current_time_ok():
    arguments = Argument('videos/test.mp4', 'False')
    video_analyzer = VideoAnalyzer(arguments)
    cap = video_analyzer.videoCapture

    assert video_analyzer.getCurrentTime(cap) == '0:00:00'


################################################
#
# US: 3
#
# Checks if the video is displaying
#
################################################
def test_if_video_shows():
    arguments = Argument('videos/test.mp4', 'True')
    video_analyzer = VideoAnalyzer(arguments)
    cap = video_analyzer.videoCapture

    ret, frame = cap.read()

    assert ret == True
    assert type(video_analyzer.showFrame(frame)) is np.ndarray

################################################
#
# US: 6
#
# Checks if the stats are ok
#
################################################
def test_if_stats_are_ok():
    arguments = Argument('videos/test.mp4', 'False')
    video_analyzer = VideoAnalyzer(arguments)

    assert video_analyzer.frames == 29.0
    assert video_analyzer.fps == 23
    assert video_analyzer.seconds == 1

