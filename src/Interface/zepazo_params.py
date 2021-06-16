#from src.Analyzers.video_utilities import VideoAnalyzer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLabel, QSizePolicy, QMessageBox, QComboBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from cv2 import cv2
import json
import pyperclip

from os.path import dirname, join, abspath
import os, sys
sys.path.insert(0, abspath(join(dirname(__file__), '..')))
from Analyzers.video_utilities import VideoAnalyzer
sys.path.insert(0, abspath(join(dirname(__file__))))

class ZepazoParams(QMainWindow):
    def __init__(self):
        #Parameters
        self.detectionLimit = 50
        self.ellipse = None
        self.dilate = None
        self.masks = []
        self.videoPath = None
        self.first_frame = None
        self.addingMask = False
        self.deletingMask = False
        self.frame_ellipse = None
        self.frame_masks = None
        self.folder = None
        self.numFrames = None

        #Init main window
        super(ZepazoParams, self).__init__()
        self.setObjectName("ZepazoWindow")
        self.resize(1052, 765)
        self.setWindowTitle("Zepazo Params")
        self.setupUI()

    def loadVideo(self):
        try:
            self.addingMask = False
            self.deletingMask = False
            self.videoPath = QFileDialog.getOpenFileName(None, "Select a video", "", "Video files (*.*)")
            self.videoAnalyzer = VideoAnalyzer(None, self.videoPath[0], False, self.detectionLimit, self.ellipse, None, None, None, self.dilate, None, None)
            self.first_frame = self.videoAnalyzer.getInitialFrame()
            self.frame_ellipse = self.first_frame.copy()
            self.frame_masks = self.first_frame.copy()
            
            #Reset Params
            self.dilate = None
            self.folder = None
            self.numFrames = None
            self.masks = []
            self.addingMask = False
            self.spinBoxDetectionLimit.setValue(50)
            self.detectionLimit = 50
            frame, value = self.videoAnalyzer.selectAndApplyCircleLimitArgment(self.ellipse, self.first_frame)
            self.spinboxEllipse.setValue(int(value))
            self.spinboxEllipse.setEnabled(False)
            self.checkBoxEllipse.setChecked(True)
            self.adjustEllipse()
            self.spinBoxDilate.setValue(0)
            self.checkBoxDilate.setChecked(False)
            self.ellipse = None
            
            #Show Frame
            self.showFrame(self.first_frame)
            
        except:
            self.addMessage("Please select a correct video file")
            self.videoPath = None


    def showFrame(self, first_frame):
        first_frame_qt = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)
        height, width, ch = first_frame_qt.shape
        bytes_lines = ch * width
        qt_image = QtGui.QImage(first_frame_qt.data, width,height, bytes_lines, QtGui.QImage.Format_RGB888)
        qt_image_scaled = qt_image.scaled(int(width), int(height), Qt.KeepAspectRatio)
        self.centralPanel.setPixmap(QPixmap.fromImage(qt_image_scaled))
        self.centralPanel.setScaledContents(False)

    def addMessage(self, message):
        QMessageBox.about(self,"Error", message)

    def adjustEllipse(self):
        self.addingMask = False
        self.deletingMask = False
        

        if(self.videoPath == None):
            if(self.spinboxEllipse.value() != 33):
                self.addMessage("First select a video file")
            self.spinboxEllipse.setValue(33)
        else:
            self.ellipse = self.spinboxEllipse.value()
            frame, _ = self.videoAnalyzer.selectAndApplyCircleLimitArgment(self.ellipse, self.first_frame)
            self.frame_ellipse = frame
            self.showFrame(self.frame_ellipse)
    
    def adjustDetectionLimit(self):
        if(self.videoPath == None):
            if(self.spinBoxDetectionLimit.value() != 50):
                self.addMessage("First select a video file")
            self.spinBoxDetectionLimit.setValue(50)
        else:
            self.detectionLimit = self.spinBoxDetectionLimit.value()


    def checkAutoEllipse(self):
        self.addingMask = False
        self.deletingMask = False
        if(self.videoPath == None):
            if(self.checkBoxEllipse.isChecked()):
                self.addMessage("First select a video file")
                self.checkBoxEllipse.setChecked(False)
        else:
            if self.checkBoxEllipse.isChecked() == True:
                self.ellipse = None
                
                if(self.videoPath == None):
                    self.loadVideo()
                
                frame, value = self.videoAnalyzer.selectAndApplyCircleLimitArgment(self.ellipse, self.first_frame)
                self.ellipse = None
                self.frame_ellipse = frame
                self.spinboxEllipse.setValue(int(value))
                self.spinboxEllipse.setEnabled(False)
                self.showFrame(self.frame_ellipse)
            else:
                self.ellipse = self.spinboxEllipse.value()
                self.spinboxEllipse.setEnabled(True)


    def clickImage(self, event):
        x_pos = event.pos().x()
        y_pos = event.pos().y()

        if(self.addingMask):
            self.deletingMask = False

            self.masks.append([x_pos,y_pos])


            if(len(self.masks) % 2 == 0):
                self.addingMask = False
                self.deletingMask = False
                num_masks = len(self.masks)
                
                if(num_masks > 0):
                    cv2.rectangle(self.frame_masks, 
                            (self.masks[num_masks-2][0],self.masks[num_masks-2][1] ),
                            (self.masks[num_masks-1][0], self.masks[num_masks-1][1]),
                            (0,0,255), -1)

            self.showFrame(self.frame_masks)
        else: #Deleting mask
            if(self.deletingMask):
                self.deletingMask = False
                mask = self.inMask(x_pos, y_pos)

                if(mask != None):
                    self.masks.pop(mask*2)
                    self.masks.pop(mask*2)
                    
                    num_masks = len(self.masks) // 2
                    
                    self.frame_masks = self.first_frame.copy()
                    
                    for i in range(num_masks):
                                cv2.rectangle(self.frame_masks, (self.masks[2*i][0],self.masks[2*i][1]), (self.masks[2*i+1][0],self.masks[2*i+1][1]), (0,0,255), -1)
                    
                    self.showFrame(self.frame_masks)
                else:
                    self.addMessage("No mask selected")

    def deleteMask(self):
        self.addingMask = False
        self.deletingMask = True


    def inMask(self, x,y):
        num_masks = len(self.masks) // 2
        mask = None
    
        for i in range(num_masks):
            x1 = self.masks[2*i][0]
            y1 = self.masks[2*i][1] 
            x2 = self.masks[2*i+1][0]
            y2 = self.masks[2*i+1][1]

            for j in range(x1, x2):
                for k in range(y1,y2):
                    if(x == j and y == k):
                        mask = i

        return mask

            
        

    def addMask(self):
        if(self.videoPath == None):
            self.addMessage("First select a video file")
        else:
            self.showFrame(self.frame_masks)

            if(self.addingMask == False):
                self.addingMask = True
            
    def resetParams(self):
        if(self.videoPath != None):
            #Parameters
            self.folder = None
            self.masks = []
            self.addingMask = False
            self.deletingMask = False
            self.spinBoxDetectionLimit.setValue(50)
            self.spinBoxDilate.setValue(0)
            self.checkBoxDilate.setChecked(False)
            self.ellipse = None
            frame, value = self.videoAnalyzer.selectAndApplyCircleLimitArgment(self.ellipse, self.first_frame)
            self.spinboxEllipse.setValue(int(value))
            self.checkBoxEllipse.setChecked(True)
            self.spinboxEllipse.setEnabled(False)
            self.detectionLimit = 50
            self.dilate = None
            self.frame_ellipse = self.first_frame.copy()
            self.frame_masks = self.first_frame.copy()
            self.showFrame(self.first_frame)
            self.numFrames = None

    def resetMasks(self):
        if(self.videoPath == None):
            self.addMessage("First select a video file")
        else:
            self.addingMask = False
            self.deletingMask = False
            self.frame_masks = self.first_frame.copy()
            self.masks = []
            self.showFrame(self.frame_masks)

    def showAllParams(self):
        if(self.videoPath == None):
            self.addMessage("First select a video file")
        else:
            all_frame = self.frame_ellipse.copy()
            num_masks = len(self.masks)
            for i in range(num_masks//2):
                        cv2.rectangle(all_frame, (self.masks[2*i][0],self.masks[2*i][1]), (self.masks[2*i+1][0],self.masks[2*i+1][1]), (0,0,255), -1)
            self.showFrame(all_frame)

    def drawMasks(self, frame):
        num_masks = len(self.masks)
        for i in range(num_masks//2):
                        cv2.rectangle(frame, (self.masks[2*i][0],self.masks[2*i][1]), (self.masks[2*i+1][0],self.masks[2*i+1][1]), (0,0,255), -1)


    def showCommand(self):
        if(self.videoPath == None):
            self.addMessage("First select and configure a video file")
        else:
            message = "python3 zepazo.py "
            message = message + "-v " + self.videoPath[0]

            if(self.detectionLimit != None):
                message = message  + " -l " + str(self.detectionLimit) 
            
            if(self.ellipse != None):
                message = message + " -cl " + str(self.ellipse)

            if(self.dilate != None):
                message = message + " -dt " + str(self.dilate)

            if(len(self.masks) > 0):
                message = message + " -cm "
                
                for i in range(0,len(self.masks)):
                    message = message + str(self.masks[i][0]) + " " + str(self.masks[i][1]) + " "


            if(self.folder != None):
                message = message + " -f " + self.folder

            if(self.numFrames != None):
                message = message + " -ssf " + str(self.numFrames)

            QMessageBox.about(self,"Command", message)

            pyperclip.copy(message)

            QMessageBox.information(self, "Copied to clipboard", "Copied to clipboard")

    def saveParams(self):
        if(self.videoPath != None):
            json_args = {
                'detectionlimit':self.detectionLimit,
                'dilate':self.dilate,
                'coordinatesmask':self.masks,
                'circlelimit':self.ellipse,
                'folder':self.folder,
                'saveSurroundingFrames':self.numFrames
            }

            path = QFileDialog.getSaveFileName(None, "Save Parameters Configuration File",".json")
            
            if(path[0].endswith(".json") == False):
                path_file = path[0] + ".json"
            else:
                path_file = path[0]

            with open(path_file, 'w') as json_file:
                json.dump(json_args, json_file)
        else:
            self.addMessage("First select and configure a video file")

    def loadParams(self):
        if(self.videoPath == None):
            self.addMessage("First select a video file first")
        else:
            json_path = QFileDialog.getOpenFileName(None, "Select a Configuration File", "", "*.json")

            with open(json_path[0], 'r') as json_file:
                args = json.load(json_file)

            self.detectionLimit = args["detectionlimit"]
            self.dilate = args["dilate"]
            self.masks = args["coordinatesmask"]
            self.ellipse = args["circlelimit"]
            self.folder = args["folder"]
            self.numFrames = args["saveSurroundingFrames"]
            
            self.drawMasks(self.frame_masks)
            
            self.spinboxEllipse.setValue(self.ellipse)
            self.spinBoxDetectionLimit.setValue(self.detectionLimit)
            
            if(self.ellipse == None):
                self.checkBoxEllipse.setChecked(True)
            else:
                self.checkBoxEllipse.setChecked(False)

            self.showAllParams()
    
    def selectSaveImpactsFolder(self):
        folder_path = str(QFileDialog.getExistingDirectory(self, "Select a folder to save impact frames"))
        self.folder = folder_path

    def showVideoSample(self):
        if(self.videoPath != None):
            self.videoAnalyzer = VideoAnalyzer(None, self.videoPath[0], True, self.detectionLimit, self.ellipse, self.masks, None, None, self.dilate, None, None)
            self.videoAnalyzer.showASample()
        else:
            self.addMessage("First select a video file")

    def selectNumFrames(self):
        self.numFrames = self.spinBoxFrames.value()

    def setupUI(self):
        self.setUpCentralWidget()
        self.setSuperiorFrame()
        self.setCentralContent()
        self.setInferiorFrame()
        self.addMenu()

    def checkboxDilateClicked(self):
        if(self.videoPath != None):
            if(self.checkBoxDilate.isChecked()):
                self.spinBoxDilate.setEnabled(True)
            else:
                self.spinBoxDilate.setEnabled(False)
                self.dilate = None
        else:
            self.addMessage("First select a video file")

    def setDilateValue(self):
        self.dilate = self.spinBoxDilate.value()

    """
    This centralWidget contains all elements in the main window in a Grid Layout
    """
    def setUpCentralWidget(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.layoutVerticalTresPaneles = QtWidgets.QVBoxLayout()
        self.layoutVerticalTresPaneles.setObjectName("layoutVerticalTresPaneles")


    def setSuperiorFrame(self):
        #Creates a frame
        self.frame_superior = QtWidgets.QFrame(self.centralwidget)
        self.frame_superior.setMinimumSize(QtCore.QSize(800, 50))
        self.frame_superior.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_superior.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_superior.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_superior.setObjectName("frame_superior")

        #Defines top frame's layout
        self.layoutWidget = QtWidgets.QWidget(self.frame_superior)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 140, 32))
        self.layoutWidget.setObjectName("layoutWidget")

        #Defines an Horizontal Layout for items in the frame
        self.layoutSuperior = QtWidgets.QGridLayout(self.layoutWidget)
        self.layoutSuperior.setContentsMargins(0, 0, 0, 0)
        self.layoutSuperior.setObjectName("layoutSuperior")

        #Adds a button to preview parameters
        self.button_visualize_all = QtWidgets.QPushButton(self.layoutWidget)
        self.button_visualize_all.setMinimumSize(QtCore.QSize(30, 30))
        self.button_visualize_all.setMaximumSize(QtCore.QSize(30, 30))
        self.button_visualize_all.setText("")
        icon = QtGui.QIcon()
        os.chdir(abspath(join(dirname(__file__))))
        icon.addPixmap(QtGui.QPixmap("icons/visualize_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(QtGui.QIcon("icons/main.png"))
        self.button_visualize_all.setIcon(icon)
        self.button_visualize_all.setIconSize(QtCore.QSize(25, 25))
        self.button_visualize_all.setObjectName("button_visualize_all")
        self.layoutSuperior.addWidget(self.button_visualize_all, 0, 0, 1, 1)

        #Adds a button to reset all parameters
        self.button_reset_all = QtWidgets.QPushButton(self.layoutWidget)
        self.button_reset_all.setMinimumSize(QtCore.QSize(30, 30))
        self.button_reset_all.setMaximumSize(QtCore.QSize(30, 30))
        self.button_reset_all.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/reset_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_reset_all.setIcon(icon1)
        self.button_reset_all.setIconSize(QtCore.QSize(18, 18))
        self.button_reset_all.setObjectName("button_reset_all")
        self.layoutSuperior.addWidget(self.button_reset_all, 0, 1, 1, 1)

        #Adds a button to preview a video sample
        self.button_play = QtWidgets.QPushButton(self.layoutWidget)
        self.button_play.setMinimumSize(QtCore.QSize(30, 30))
        self.button_play.setMaximumSize(QtCore.QSize(30, 30))
        self.button_play.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/play_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_play.setIcon(icon2)
        self.button_play.setIconSize(QtCore.QSize(25, 25))
        self.button_play.setObjectName("button_play")
        self.layoutSuperior.addWidget(self.button_play, 0, 3, 1, 1)
        

        #Adds a button to get a command
        self.button_command = QtWidgets.QPushButton(self.layoutWidget)
        self.button_command.setMinimumSize(QtCore.QSize(30, 30))
        self.button_command.setMaximumSize(QtCore.QSize(30, 30))
        self.button_command.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/command.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_command.setIcon(icon2)
        self.button_command.setIconSize(QtCore.QSize(25, 25))
        self.button_command.setObjectName("button_command")
        self.layoutSuperior.addWidget(self.button_command, 0, 2, 1, 1)

        #Adds superior frame to general layout
        self.layoutVerticalTresPaneles.addWidget(self.frame_superior)

    def setCentralContent(self):

        self.scrollAreaImage = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollAreaImage.setWidgetResizable(True)
        self.scrollAreaImage.setObjectName("scrollAreaImage")
        self.scrollAreaWidgetContentsImage = QtWidgets.QWidget()
        self.scrollAreaWidgetContentsImage.setGeometry(QtCore.QRect(0, 0, 1030, 579))
        self.scrollAreaWidgetContentsImage.setObjectName("scrollAreaWidgetContentsImage")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContentsImage)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.centralPanel = QtWidgets.QLabel(self.scrollAreaWidgetContentsImage)
        self.centralPanel.setObjectName("labelImage")
        self.gridLayout_2.addWidget(self.centralPanel, 0, 0, 1, 1)
        self.scrollAreaImage.setWidget(self.scrollAreaWidgetContentsImage)
        self.layoutVerticalTresPaneles.addWidget(self.scrollAreaImage)

        
        #self.layoutVerticalTresPaneles.addWidget(self.centralPanel)

    def setInferiorFrame(self):
        #Adds Inferior Frame
        self.frame_inferior = QtWidgets.QFrame(self.centralwidget)
        self.frame_inferior.setMinimumSize(QtCore.QSize(800, 80))
        self.frame_inferior.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame_inferior.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_inferior.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_inferior.setObjectName("frame_inferior")

        #Adds Inferior's Frame Layout
        self.layoutWidget1 = QtWidgets.QWidget(self.frame_inferior)
        self.layoutWidget1.setGeometry(QtCore.QRect(21, 10, 605, 59))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayoutInferior = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayoutInferior.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutInferior.setObjectName("horizontalLayoutInferior")

        #Adds detection Limit 
        #Configure Font
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        font.setWeight(75)
        self.layoutDetectionLimit = QtWidgets.QVBoxLayout()
        self.layoutDetectionLimit.setObjectName("layoutDetectionLimit")
        #Adds a label
        self.labelDetectionLimit = QtWidgets.QLabel(self.layoutWidget1)
        self.labelDetectionLimit.setMinimumSize(QtCore.QSize(120, 0))
        self.labelDetectionLimit.setFont(font)
        self.labelDetectionLimit.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDetectionLimit.setObjectName("labelDetectionLimit")
        self.layoutDetectionLimit.addWidget(self.labelDetectionLimit)
        #Adds a SpinBox
        self.spinBoxDetectionLimit = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinBoxDetectionLimit.setMaximumSize(QtCore.QSize(120, 16777215))
        self.spinBoxDetectionLimit.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxDetectionLimit.setMinimum(1)
        self.spinBoxDetectionLimit.setMaximum(255)
        self.spinBoxDetectionLimit.setProperty("value", 50)
        self.spinBoxDetectionLimit.setObjectName("spinBoxDetectionLimit")
        self.layoutDetectionLimit.addWidget(self.spinBoxDetectionLimit)
        self.horizontalLayoutInferior.addLayout(self.layoutDetectionLimit)
        #Adds Delimiter line
        self.line = QtWidgets.QFrame(self.layoutWidget1)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayoutInferior.addWidget(self.line)

        #Adds ellipse option
        #Configure vertical layout
        self.layoutEllipse = QtWidgets.QVBoxLayout()
        self.layoutEllipse.setObjectName("layoutEllipse")
        #configure label
        self.labelELlipse = QtWidgets.QLabel(self.layoutWidget1)
        self.labelELlipse.setFont(font)
        self.labelELlipse.setAlignment(QtCore.Qt.AlignCenter)
        self.labelELlipse.setObjectName("labelELlipse")
        self.layoutEllipse.addWidget(self.labelELlipse)
        #Configure horizontal layout
        self.horizontalLayoutEllipse = QtWidgets.QHBoxLayout()
        self.horizontalLayoutEllipse.setObjectName("horizontalLayoutEllipse")
        #Adds SpinBox
        self.spinboxEllipse = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinboxEllipse.setEnabled(True)
        self.spinboxEllipse.setMaximumSize(QtCore.QSize(120, 16777215))
        self.spinboxEllipse.setAlignment(QtCore.Qt.AlignCenter)
        self.spinboxEllipse.setMinimum(1)
        self.spinboxEllipse.setMaximum(255)
        self.spinboxEllipse.setProperty("value", 33)
        self.spinboxEllipse.setObjectName("spinboxEllipse")
        self.horizontalLayoutEllipse.addWidget(self.spinboxEllipse)
        #Adds checkbox
        self.checkBoxEllipse = QtWidgets.QCheckBox(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxEllipse.sizePolicy().hasHeightForWidth())
        self.checkBoxEllipse.setSizePolicy(sizePolicy)
        self.checkBoxEllipse.setMinimumSize(QtCore.QSize(65, 30))
        self.checkBoxEllipse.setMaximumSize(QtCore.QSize(30, 30))
        self.checkBoxEllipse.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkBoxEllipse.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBoxEllipse.setStyleSheet("QCheckBox::indicator{width:20px; height:20px};")
        self.checkBoxEllipse.setIconSize(QtCore.QSize(30, 30))
        self.checkBoxEllipse.setChecked(False)
        self.checkBoxEllipse.setObjectName("checkBoxEllipse")
        self.horizontalLayoutEllipse.addWidget(self.checkBoxEllipse)
        self.layoutEllipse.addLayout(self.horizontalLayoutEllipse)
        self.horizontalLayoutInferior.addLayout(self.layoutEllipse)
        #Adds separator line
        self.line_2 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayoutInferior.addWidget(self.line_2)

        #Dilate
        #Sets vertical layout
        self.layoutDilate = QtWidgets.QVBoxLayout()
        self.layoutDilate.setObjectName("layoutDilate")
        #Sets label
        self.labelDilate = QtWidgets.QLabel(self.layoutWidget1)
        self.labelDilate.setFont(font)
        self.labelDilate.setAlignment(QtCore.Qt.AlignCenter)
        self.labelDilate.setObjectName("labelDilate")
        self.layoutDilate.addWidget(self.labelDilate)
        #Horizontal layout
        self.horizontalLayoutDilate = QtWidgets.QHBoxLayout()
        self.horizontalLayoutDilate.setObjectName("horizontalLayoutDilate")
        self.checkBoxDilate = QtWidgets.QCheckBox(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxDilate.sizePolicy().hasHeightForWidth())
        #Checkbox
        self.checkBoxDilate.setSizePolicy(sizePolicy)
        self.checkBoxDilate.setMinimumSize(QtCore.QSize(30, 30))
        self.checkBoxDilate.setMaximumSize(QtCore.QSize(30, 30))
        self.checkBoxDilate.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.checkBoxDilate.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBoxDilate.setStyleSheet("QCheckBox::indicator{width:20px; height:20px};")
        self.checkBoxDilate.setText("")
        self.checkBoxDilate.setIconSize(QtCore.QSize(30, 30))
        self.checkBoxDilate.setObjectName("checkBoxDilate")
        self.horizontalLayoutDilate.addWidget(self.checkBoxDilate)
        #SpinBox
        self.spinBoxDilate = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinBoxDilate.setEnabled(False)
        self.spinBoxDilate.setMaximumSize(QtCore.QSize(120, 16777215))
        self.spinBoxDilate.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxDilate.setObjectName("spinBoxDilate")
        self.horizontalLayoutDilate.addWidget(self.spinBoxDilate)
        self.layoutDilate.addLayout(self.horizontalLayoutDilate)
        self.horizontalLayoutInferior.addLayout(self.layoutDilate)
        #Separator Line
        self.line_3 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayoutInferior.addWidget(self.line_3)


        #Masks
        #Vertical layout
        self.layoutMasks = QtWidgets.QVBoxLayout()
        self.layoutMasks.setObjectName("layoutMasks")
        #label
        self.labelMasks = QtWidgets.QLabel(self.layoutWidget1)
        self.labelMasks.setFont(font)
        self.labelMasks.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMasks.setObjectName("labelMasks")
        self.layoutMasks.addWidget(self.labelMasks)
        #Horizontal layout
        self.horizontalLayoutMasks = QtWidgets.QHBoxLayout()
        self.horizontalLayoutMasks.setContentsMargins(-1, -1, -1, 3)
        self.horizontalLayoutMasks.setObjectName("horizontalLayoutMasks")
        #Button add mask
        self.buttonAddMask = QtWidgets.QPushButton(self.layoutWidget1)
        self.buttonAddMask.setMinimumSize(QtCore.QSize(25, 25))
        self.buttonAddMask.setMaximumSize(QtCore.QSize(25, 25))
        self.buttonAddMask.setStyleSheet("QPushButton { padding: 10px; }")
        self.buttonAddMask.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonAddMask.setIcon(icon3)
        self.buttonAddMask.setObjectName("buttonAddMask")
        self.horizontalLayoutMasks.addWidget(self.buttonAddMask)
        
        #Button delete mask
        self.buttonDeleteMask = QtWidgets.QPushButton(self.layoutWidget1)
        self.buttonDeleteMask.setMinimumSize(QtCore.QSize(25, 25))
        self.buttonDeleteMask.setMaximumSize(QtCore.QSize(25, 25))
        self.buttonDeleteMask.setStyleSheet("QPushButton { padding: 10px; }")
        self.buttonDeleteMask.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonDeleteMask.setIcon(icon3)
        self.buttonDeleteMask.setObjectName("buttonDeleteMask")
        self.horizontalLayoutMasks.addWidget(self.buttonDeleteMask)
        
        #Button reset mask
        self.buttonResetMask = QtWidgets.QPushButton(self.layoutWidget1)
        self.buttonResetMask.setMinimumSize(QtCore.QSize(25, 25))
        self.buttonResetMask.setMaximumSize(QtCore.QSize(25, 25))
        self.buttonResetMask.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/reset_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonResetMask.setIcon(icon1)
        self.buttonResetMask.setObjectName("buttonResetMask")
        self.horizontalLayoutMasks.addWidget(self.buttonResetMask)
        self.layoutMasks.addLayout(self.horizontalLayoutMasks)
        self.horizontalLayoutInferior.addLayout(self.layoutMasks)
        
        #Folder Save Impacts
        self.line_4 = QtWidgets.QFrame(self.layoutWidget1)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayoutInferior.addWidget(self.line_4)
        self.layoutSaveImpacts = QtWidgets.QVBoxLayout()
        self.layoutSaveImpacts.setObjectName("layoutSaveImpacts")
        self.labelSaveImpacts = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setBold(True)
        font.setWeight(75)
        self.labelSaveImpacts.setFont(font)
        self.labelSaveImpacts.setAlignment(QtCore.Qt.AlignCenter)
        self.labelSaveImpacts.setObjectName("labelSaveImpacts")
        self.layoutSaveImpacts.addWidget(self.labelSaveImpacts)
        self.horizontalLayoutSaveImpacts = QtWidgets.QHBoxLayout()
        self.horizontalLayoutSaveImpacts.setContentsMargins(-1, -1, -1, 3)
        self.horizontalLayoutSaveImpacts.setObjectName("horizontalLayoutSaveImpacts")
        #ButtonFolder
        self.buttonSaveImpacts = QtWidgets.QPushButton(self.layoutWidget1)
        self.buttonSaveImpacts.setMinimumSize(QtCore.QSize(25, 25))
        self.buttonSaveImpacts.setMaximumSize(QtCore.QSize(25, 25))
        self.buttonSaveImpacts.setStyleSheet("QPushButton { padding: 10px; }")
        self.buttonSaveImpacts.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonSaveImpacts.setIcon(icon3)
        self.buttonSaveImpacts.setObjectName("buttonSaveImpacts")
        self.horizontalLayoutSaveImpacts.addWidget(self.buttonSaveImpacts)
        #SpinBox
        self.spinBoxFrames = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinBoxFrames.setEnabled(True)
        self.spinBoxFrames.setMaximumSize(QtCore.QSize(120, 16777215))
        self.spinBoxFrames.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxFrames.setProperty("value", 0)
        self.spinBoxFrames.setMinimum(0)
        self.spinBoxFrames.setObjectName("spinBoxFrames")
        self.horizontalLayoutSaveImpacts.addWidget(self.spinBoxFrames)

        self.layoutSaveImpacts.addLayout(self.horizontalLayoutSaveImpacts)
        self.horizontalLayoutInferior.addLayout(self.layoutSaveImpacts)

        #Adding frame inferior to layoutVerticalTresPaneles
        self.layoutVerticalTresPaneles.addWidget(self.frame_inferior)
        self.gridLayout.addLayout(self.layoutVerticalTresPaneles, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)


    def addMenu(self):
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1052, 22))
        self.menubar.setObjectName("menubar")
        self.menuVideo = QtWidgets.QMenu(self.menubar)
        self.menuVideo.setObjectName("menuVideo")
        self.menuParameters = QtWidgets.QMenu(self.menubar)
        self.menuParameters.setObjectName("menuParameters")
        self.setMenuBar(self.menubar)
        self.actionLoad_Video = QtWidgets.QAction(self)
        self.actionLoad_Video.setObjectName("actionLoad_Video")
        self.actionOpen_file = QtWidgets.QAction(self)
        self.actionOpen_file.setObjectName("actionOpen_file")
        self.actionSave_file = QtWidgets.QAction(self)
        self.actionSave_file.setObjectName("actionSave_file")
        self.menuVideo.addAction(self.actionLoad_Video)
        self.menuParameters.addAction(self.actionOpen_file)
        self.menuParameters.addAction(self.actionSave_file)
        self.menubar.addAction(self.menuVideo.menuAction())
        self.menubar.addAction(self.menuParameters.menuAction())

        self.addTexts()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.actionLoad_Video.triggered.connect(lambda:self.loadVideo())
        self.spinboxEllipse.valueChanged.connect(self.adjustEllipse)
        self.checkBoxEllipse.clicked.connect(self.checkAutoEllipse)
        self.centralPanel.mousePressEvent = self.clickImage
        self.buttonAddMask.clicked.connect(self.addMask)
        self.button_reset_all.clicked.connect(self.resetParams)
        self.buttonResetMask.clicked.connect(self.resetMasks)
        self.button_visualize_all.clicked.connect(self.showAllParams)
        self.actionSave_file.triggered.connect(lambda:self.saveParams())
        self.button_play.clicked.connect(self.showVideoSample)
        self.spinBoxDetectionLimit.valueChanged.connect(self.adjustDetectionLimit)
        self.actionOpen_file.triggered.connect(self.loadParams)
        self.buttonDeleteMask.clicked.connect(self.deleteMask)
        self.button_command.clicked.connect(self.showCommand)
        self.buttonSaveImpacts.clicked.connect(self.selectSaveImpactsFolder)
        self.spinBoxFrames.valueChanged.connect(self.selectNumFrames)
        self.checkBoxDilate.clicked.connect(self.checkboxDilateClicked)
        self.spinBoxDilate.valueChanged.connect(self.setDilateValue)

    def addTexts(self):
        _translate = QtCore.QCoreApplication.translate
        self.button_visualize_all.setToolTip(_translate("ZepazoWindow", "Preview Params"))
        self.button_reset_all.setToolTip(_translate("ZepazoWindow", "Reset Params"))
        self.button_play.setToolTip(_translate("ZepazoWindow", "Play a sample"))
        self.button_command.setToolTip(_translate("ZepazoWindow", "Get command"))
        self.labelDetectionLimit.setText(_translate("ZepazoWindow", "Detection Limit"))
        self.labelELlipse.setText(_translate("ZepazoWindow", "Ellipse"))
        self.checkBoxEllipse.setText(_translate("ZepazoWindow", "Auto"))
        self.labelDilate.setText(_translate("ZepazoWindow", "Dilate"))
        self.labelMasks.setText(_translate("ZepazoWindow", "Masks"))
        self.buttonAddMask.setToolTip(_translate("ZepazoWindow", "Add Mask"))
        self.buttonDeleteMask.setToolTip(_translate("ZepazoWindow", "Delete Mask"))
        self.buttonResetMask.setToolTip(_translate("ZepazoWindow", "Reset all Masks"))
        self.menuVideo.setTitle(_translate("ZepazoWindow", "Video"))
        self.menuParameters.setTitle(_translate("ZepazoWindow", "Parameters"))
        self.actionLoad_Video.setText(_translate("ZepazoWindow", "Open file"))
        self.actionOpen_file.setText(_translate("ZepazoWindow", "Open file"))
        self.actionSave_file.setText(_translate("ZepazoWindow", "Save file"))
        self.labelSaveImpacts.setText(_translate("ZepazoWindow", "Impacts"))
        self.buttonSaveImpacts.setToolTip(_translate("ZepazoWindow", "Folder to save impacts"))
        self.spinBoxFrames.setToolTip(_translate("ZepazoWindows", "Number of sorrounded frames to save additionally"))

def launch_UI():
    app = QApplication(sys.argv)
    win = ZepazoParams()
    win.show()
    sys.exit(app.exec_())


launch_UI()