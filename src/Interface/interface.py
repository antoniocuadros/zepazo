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



def launch_UI():
    app = QApplication(sys.argv)
    win = ZepazoParams()
    win.show()
    sys.exit(app.exec_())


launch_UI()