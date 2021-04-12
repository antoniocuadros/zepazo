from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys

class ZepazoParams(QMainWindow):
    def __init__(self):
        super(ZepazoParams, self).__init__()
        self.setObjectName("ZepazoWindow")
        self.resize(1052, 765)
        self.setWindowTitle("Zepazo Params")

    def setupUI(self):
        self.setUpCentralWidget()
        self.setSuperiorFrame()
        self.setCentralContent()
        self.setInferiorFrame()

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
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 104, 32))
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
        icon.addPixmap(QtGui.QPixmap("icons/visualize_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
        icon2.addPixmap(QtGui.QPixmap("play_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_play.setIcon(icon2)
        self.button_play.setIconSize(QtCore.QSize(25, 25))
        self.button_play.setObjectName("button_play")
        self.layoutSuperior.addWidget(self.button_play, 0, 2, 1, 1)
        
        #Adds superior frame to general layout
        self.layoutVerticalTresPaneles.addWidget(self.frame_superior)

    def setCentralContent(self):
        self.centralPanel = QtWidgets.QGraphicsView(self.centralwidget)
        self.centralPanel.setObjectName("centralPanel")
        self.layoutVerticalTresPaneles.addWidget(self.centralPanel)

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
        self.layoutWidget1.setGeometry(QtCore.QRect(21, 10, 449, 59))
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
        self.spinboxEllipse.setEnabled(False)
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
        self.checkBoxEllipse.setChecked(True)
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

        #Masks
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

        
def launch_UI():
    app = QApplication(sys.argv)
    win = ZepazoParams()
    win.show()
    sys.exit(app.exec_())


launch_UI()