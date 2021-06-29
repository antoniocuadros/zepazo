#Python 3.8.2
##############################
#
#   tests_fsdator.py
#
##############################
import pytest
import cv2
import os
from src.Dators.fsdator import FSDator
from src.Analyzers.image_utilities import ImageAnalyzer
from src.Analyzers.video_utilities import VideoAnalyzer
from src.Impacts.impact import Impact

################################################
#
# Checks if we can create a FSDator instance
#
################################################
def test_if_dator_created_then_error(capfd):   
    dator = FSDator("test/example_video/")
    assert os.path.isdir("test/example_video/")
    assert dator.path == "test/example_video/"

################################################
#
# Checks saveFrame method
#
################################################
def test_if_frame_is_saved():
    dator = FSDator("test/example_video/")
    frame = cv2.imread('test/example_video/dilate1.png')
    
    dator.saveFrame("name", frame)
    assert os.path.isfile("test/example_video/name.png")
    os.remove("test/example_video/name.png")

################################################
#
# Checks saveSurroundingFrame method
#
################################################
def test_if_surroundingFrames_saved():
    dator = FSDator("test/example_video/")
    dator.saveSurroundingFrames(2, 0, "impact_0", "test/example_video/test.mp4")
    
    assert os.path.isfile("test/example_video/impact_0.0.png")
    os.remove("test/example_video/impact_0.0.png")
    
    assert os.path.isfile("test/example_video/impact_0.1.png")
    os.remove("test/example_video/impact_0.1.png")

    assert os.path.isfile("test/example_video/impact_0.3.png")
    os.remove("test/example_video/impact_0.3.png")
    
    assert os.path.isfile("test/example_video/impact_0.4.png")
    os.remove("test/example_video/impact_0.4.png")

################################################
#
# Checks saveLog method
#
################################################
def test_if_impactLog_saved():
    dator = FSDator("test/example_video/")
    video_analyzer = VideoAnalyzer(dator, 'test/example_video/test.mp4', True, None, None,None, None,1, None,None,None)
    cap = video_analyzer.videoCapture

    _, frame = cap.read()
    impact = Impact(frame, 0, 1)
    impact.setTime("00:00:00")
    impacts = []
    impacts.append(impact)

    dator.saveLog(impacts)
    assert os.path.isfile("test/example_video/log.json")

################################################
#
# Checks videoExists method
#
################################################
def test_if_video_exists():
    dator = FSDator("test/example_video/")

    assert dator.videoExists("test/example_video/test.mp4") == True
    assert dator.videoExists("test/example_video/test3.mp4") == False

################################################
#
# Checks logFileExists method
#
################################################
def test_if_logFile_exists():
    dator = FSDator("test/example_video/")

    assert dator.logFileExists("test/example_video/log.json") == True
    assert dator.logFileExists("test/example_video/log3.json") == False

################################################
#
# Checks loadLogFile method
#
################################################
def test_if_loads_impactLog():
    dator = FSDator("test/example_video/")

    json =  dator.loadLogFile("test/example_video/log.json")

    assert json != None
    assert json[0]['impact_frame_number'] == 1
    assert json[0]['impact_number'] == 0
    assert json[0]['impact_time'] == "00:00:00"

    os.remove("test/example_video/log.json")


################################################
#
# Checks saveCoincidenceLog method
#
################################################
def test_if_save_coincideces_works():
    dator = FSDator("test/example_video/")
    video_analyzer = VideoAnalyzer(dator, 'test/example_video/test.mp4', True, None, None,None, None,1, None,None,None)
    cap = video_analyzer.videoCapture
    _, frame = cap.read()
    impact = Impact(frame, 0, 1)
    impact.setTime("00:00:00")
    impacts = []

    dator.saveCoincidenceLog("test/example_video/log1", "test/example_video/log2", "test/example_video/log3.json", [{'log_1_impact': "2",'log_2_impact': "3", 'sub':"4"}])
    json =  dator.loadLogFile("test/example_video/log3.json")

    assert os.path.isfile("test/example_video/log3.json")
    assert json[0]['difference'] == "4"
    assert json[0]['log_1_impact'] == "2"
    assert json[0]['log_2_impact'] == "3"
    assert json[0]['path_to_log1'] == "test/example_video/log1"
    assert json[0]['path_to_log2'] == "test/example_video/log2"
    
    os.remove("test/example_video/log3.json")

################################################
#
# Checks correctPathToSaveJSON method
#
################################################
def test_if_correct_path_to_save_json():
    dator = FSDator("test/example_video/")

    assert dator.correctPathToSaveJSON("test/example_video/log_test.json") == True
    assert dator.correctPathToSaveJSON("test/example_video/log_test.jsson") == False