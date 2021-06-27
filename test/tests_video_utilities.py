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
from src.Impacts.impact import Impact
from src.Dators.fsdator import FSDator
from .argument import Argument
import os


################################################
#
# US: 1
#
# Checks if the videopath is correctly obtained
#
################################################
def test_if_object_is_created_ok():
    dator = FSDator('test/example_video/test.mp4')
    video_analizer = VideoAnalyzer(dator,'test/example_video/test.mp4', 'False', None, None, None, None, None, None,None,None)

    assert video_analizer.videoPath == 'test/example_video/test.mp4'  

################################################
#
# [US1]
#
# Checks if the path does not exist fails
#
################################################
def test_if_object_is_created_with_error():
    
    with pytest.raises(Exception) as e:
        
        dator = FSDator("test5.mp4")
        video_analiyzer = VideoAnalyzer(dator,'test/example_video/test5.mp4', 'False', None, None, None, None, None, None,None,None)

    assert str(e.value) == "Video could not be found on this path or incorrect file type"

################################################
#
# [US1]
#
# Checks if the videoCap object is working so its returns initial frame
#
################################################
def test_if_video_is_loaded_correctly():
    
        
    dator = FSDator("test5.mp4")
    video_analiyzer = VideoAnalyzer(dator,'test/example_video/test.mp4', 'False', None, None, None, None, None, None,None,None)

    ret, frame = video_analiyzer.videoCapture.read()


    assert ret == True
    assert frame.all() != None

################################################
#
# [US2]
#
# Checks if the current time method works
#
################################################
def test_if_current_time_ok():
    dator = FSDator('test/example_video/test.mp4')
    video_analyzer = VideoAnalyzer(dator,'test/example_video/test.mp4', 'False', None, None, None, None, None, None,None,None)

    assert video_analyzer.getCurrentTime(0) == '0:00:00'
    assert video_analyzer.getCurrentTime(100) == '0:00:04.347826'


################################################
#
# [US3]
#
# Checks if the video is displaying
#
################################################
def test_if_video_shows():
    dator = FSDator('test/example_video/test.mp4')
    video_analyzer = VideoAnalyzer(dator,'test/example_video/test.mp4', 'True', None, None, None, None, None, None,None,None)
    cap = video_analyzer.videoCapture

    ret, frame = cap.read()

    assert ret == True
    assert type(video_analyzer.showFrame(frame)) is np.ndarray

################################################
#
# [US5]
#
# Checks if an image is being saved in default location
#
################################################
def test_if_image_is_saved():

    image_analyzer = ImageAnalyzer(50, None, None, None,"test.mp4", None, None)
    dator = FSDator('.')
    video_analyzer = VideoAnalyzer(dator, 'test/example_video/test.mp4', True, None, None,None, None,None, None,None,None)
    cap = video_analyzer.videoCapture

    _, frame = cap.read()
    impact = Impact(frame, 0, 1)

    video_analyzer.impacts.append(impact)

    video_analyzer.saveAllImpacts()
    
    assert os.path.isfile('test.mp4_0.png') == True
    os.remove("test.mp4_0.png")

################################################
#
# [US6]
#
# Checks if the stats are ok
#
################################################
def test_if_stats_are_ok():
    dator = FSDator('test/example_video/test.mp4')
    video_analyzer = VideoAnalyzer(dator,'test/example_video/test.mp4', 'False', None, None, None, None, None, None,None,None)

    assert video_analyzer.frames == 29.0
    assert video_analyzer.fps == 23
    assert video_analyzer.seconds == 1

################################################
#
# [US9]
#
# Checks point list are correctly being transformed
# Transformed list must be half the size of the original
#
################################################
def test_if_mask_points_ok():
    dator = FSDator('test/example_video/test.mp4')
    video_analyzer = VideoAnalyzer(dator,'test/example_video/test.mp4', 'False', None, None, None, None, None, None,None,None)
    
    points = [1,2,3,4]
    
    video_analyzer.selectAndApplyMask(points)

    assert len(video_analyzer.mask_points)== len(points) / 2

################################################
#
# [US9]
#
# Checks if the has been placed by checking its
# color, black.
#
################################################
def test_is_masks_are_being_placed():
    dator = FSDator('test/example_video/test.mp4')
    video_analyzer = VideoAnalyzer(dator,'test/example_video/test.mp4', 'False', None, None, None, None, None, None,None,None)
    
    points = [1,2,3,4]

    cap = video_analyzer.videoCapture
    _, frame = cap.read()

    video_analyzer.selectAndApplyMask(points)
    video_analyzer.applyMasks(frame, frame)

    assert np.any(frame[3,3] == 0)

################################################
#
# [US21]
#
# Checks if pre and post frames are being saved in default location
#
################################################
def test_if_pre_post_images_are_saved():

    image_analyzer = ImageAnalyzer(50, None, None, None,"test.mp4", None, None)
    dator = FSDator('.')
    video_analyzer = VideoAnalyzer(dator, 'test/example_video/test.mp4', True, None, None,None, None,1, None,None,None)
    cap = video_analyzer.videoCapture

    _, frame = cap.read()
    impact = Impact(frame, 0, 1)

    video_analyzer.impacts.append(impact)

    video_analyzer.saveAllImpacts()
    
    assert os.path.isfile('test.mp4_0.0.png') == True
    assert os.path.isfile('test.mp4_0.png') == True
    assert os.path.isfile('test.mp4_0.2.png') == True
    os.remove("test.mp4_0.0.png")
    os.remove("test.mp4_0.png")
    os.remove("test.mp4_0.2.png")

################################################
#
# [US22]
#
# Checks if log is being saved in default location
#
################################################
def test_if_log_is_saved():
    dator = FSDator('.')
    video_analyzer = VideoAnalyzer(dator, 'test/example_video/test.mp4', True, None, None, None, None, None, None, None, None)
    video_analyzer.saveLogFile()
    assert os.path.isfile('log.json') == True
    os.remove("log.json")


################################################
#
# [US22]
#
# Checks if log is being saved
#
################################################
def test_if_log_is_saved():
    dator = FSDator('test/example_video')
    video_analyzer = VideoAnalyzer(dator, 'test/example_video/test.mp4', True, None, None, None, 'test/example_video/', None, None, None, None)
    video_analyzer.saveLogFile()
    assert os.path.isfile('test/example_video/log.json') == True
    os.remove("test/example_video/log.json")