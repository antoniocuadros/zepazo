#Python 3.8.2
##############################
#
#   tests_zepazo_crop.py
#
##############################
import pytest
import cv2
import os
import runpy
import  argparse
from src.Dators.fsdator import FSDator

################################################
#
# [US24]
#
# Checks if we get an error if we dont specify a video
#
################################################
def test_if_no_given_video_it_fails(capfd):
    os.system('python3 src/zepazoCrop.py')
    captured = capfd.readouterr()
    assert "Original video to crop (-vo) must be defined." in captured.err 

################################################
#
# [US24]
#
# Checks if we get an error if the video is wrong
#
################################################
def test_if_wrong_given_video_it_fails(capfd):
    os.system('python3 src/zepazoCrop.py -vo test/example_video/test5.mp4')
    captured = capfd.readouterr()
    assert "Original video to crop (-vo) must exists." in captured.err 

################################################
#
# [US24]
#
# Checks if we get an error if we dont specify a cropped video path
#
################################################
def test_if_no_cropped_video_path_given_it_fails(capfd):
    os.system('python3 src/zepazoCrop.py -vo test/example_video/test.mp4')
    captured = capfd.readouterr()
    assert "Cropped video path/name (-vc) must be defined." in captured.err 

################################################
#
# [US24]
#
# Checks if we get an error if the cropped video is wrong
#
################################################
def test_if_wrong_cropped_video_path_given(capfd):
    os.system('python3 src/zepazoCrop.py -vo test/example_video/test.mp4 -vc test/example_video/test.mp4')
    captured = capfd.readouterr()
    assert "Cropped video (-vc) error, there is another file with the same name." in captured.err 

################################################
#
# [US24]
#
# Checks if we get an error if no second start specified
#
################################################
def test_if_second_start_given(capfd):
    os.system('python3 src/zepazoCrop.py -vo test/example_video/test.mp4 -vc test/example_video/testCropped.mp4')
    captured = capfd.readouterr()
    assert "Second start (-ss) and Second end (-se) must be specified" in captured.err 

################################################
#
# [US24]
#
# Checks if we get an error if no second end specified
#
################################################
def test_if_second_start_given(capfd):
    os.system('python3 src/zepazoCrop.py -vo test/example_video/test.mp4 -vc test/example_video/testCropped.mp4 -ss 0')
    captured = capfd.readouterr()
    assert "Second start (-ss) and Second end (-se) must be specified" in captured.err

################################################
#
# [US24]
#
# Checks if no error with all parameters, so it crops the video
#
################################################
def test_if_second_start_given(capfd):
    os.system('python3 src/zepazoCrop.py -vo test/example_video/test.mp4 -vc test/example_video/testCropped.mp4 -ss 0 -se 1')
    captured = capfd.readouterr()
    
    assert os.path.isfile('test/example_video/testCropped.mp4') == True
    os.remove("test/example_video/testCropped.mp4")