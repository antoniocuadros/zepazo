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

@pytest.fixture
def app(qtbot):
    return ZepazoParams()
    


def test_if_load_video_works(app):
    app.videoPath = "test/example_video/test.mp4"

    assert app.videoPath == "test/example_video/test.mp4"