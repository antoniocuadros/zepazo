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
def test_if_load_video_works(app, qtbot):
    
    app.videoPath = "../../test/example_video/test.mp4"
    
    app.loadVideo() 

    assert ntpath.basename(app.videoPath) == "test.mp4"
    assert app.first_frame.all != None
    assert app.centralPanel.pixmap != None

################################################
#
# Checks if videos loads correctly
#
################################################
def test_if_circleLimitSelection_works(app, qtbot):
    
    app.videoPath = "../../test/example_video/test.mp4"
    
    app.spinBoxDetectionLimit.setValue(33)

    assert app.detectionLimit == 33
    assert app.spinBoxDetectionLimit.value() == 33