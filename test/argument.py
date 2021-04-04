#Python 3.8.2
##############################
#
#   argument.py
#
##############################

class Argument:
    def __init__(self, videopath, show, limit):
        self.video = videopath
        self.show = show
        self.detectionlimit = limit
        self.circlelimit = None