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


def launch_UI():
    app = QApplication(sys.argv)
    win = ZepazoParams()
    win.show()
    sys.exit(app.exec_())


launch_UI()