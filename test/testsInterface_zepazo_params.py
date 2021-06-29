#Python 3.8.2
##############################
#
#   tests_zepazo_params.py
#
##############################
import pytest
import cv2
import numpy as np
from PyQt5.QtTest import QTest
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QSizePolicy, QMessageBox, QComboBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

from src.Analyzers.image_utilities import ImageAnalyzer
from src.Analyzers.video_utilities import VideoAnalyzer
from src.Impacts.impact import Impact
from src.Dators.fsdator import FSDator
from src.Interface.zepazo_params import ZepazoParams
import os
import ntpath

@pytest.fixture
def app(qtbot):
    return ZepazoParams()
    

################################################
#
# Checks if videos loads correctly
#
################################################
def test_if_load_video_works(app):
    
    app.videoPath = "../../test/example_video/test.mp4"
    
    app.loadVideo() 

    assert ntpath.basename(app.videoPath) == "test.mp4"
    assert app.first_frame.all != None
    assert app.centralPanel.pixmap != None

################################################
#
# [US15]
#
# Checks if detectionLimit argument correctly set
#
################################################
def test_if_detectionLimitSelection_works(app):
    
    app.videoPath = "../../test/example_video/test.mp4"
    app.loadVideo() 
    
    app.spinBoxDetectionLimit.setValue(33)

    assert app.detectionLimit == 33
    assert app.spinBoxDetectionLimit.value() == 33

################################################
#
# [US10]
#
# Checks if circleLimit argument correctly set
#
################################################
def test_if_circleLimitSelection_works(app):
    app.videoPath = "../../test/example_video/test.mp4"
    app.loadVideo() 

    app.spinboxEllipse.setValue(33)
    
    assert app.ellipse == 33
    assert app.spinboxEllipse.value() == 33
    assert app.frame_ellipse.all != None
    assert app.checkBoxEllipse.isChecked() == False

################################################
#
# [US10]
#
# Checks if circleLimit argument correctly set when auto is checked
#
################################################
def test_if_circleLimitSelection_works(app):
    app.videoPath = "../../test/example_video/test.mp4"
    app.loadVideo() 

    
    app.checkBoxEllipse.setChecked(True)
    
    assert app.ellipse == None
    assert app.spinboxEllipse.value() == 1
    assert app.frame_ellipse.all != None
    assert app.checkBoxEllipse.isChecked() == True

################################################
#
# [US12]
#
# Checks if parameters preview is working
#
################################################
def test_if_previewAll_works(app):
    app.videoPath = "../../test/example_video/test.mp4"
    app.loadVideo() 

    frame1 = app.first_frame

    app.spinboxEllipse.setValue(33)
    app.adjustEllipse()

    frame2 = app.showAllParams()

    assert (np.bitwise_xor(frame1, frame2).any())