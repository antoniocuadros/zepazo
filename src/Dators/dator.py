#Python 3.8.2
##############################
#
#   dator.py
#
##############################

class Dator:
    """
    This 'abstract' class will help to have multiple classes accessing data in a exactly same way.
    """
    def __init__(self):
        if(isinstance(self, Dator)):
            raise Exception("Non-instantiable class")

    
    def saveFrame(self, name, frame):
        raise Exception("The method must be implemented by another class")


    def saveSurroundingFrames(self, num_frames, current_frame, name):
        raise Exception("The method must be implemented by another class")

    def saveLog(self, impacts):
        raise Exception("The method must be implemented by another class")

    def videoExists(self, path_to_video):
        raise Exception("The method must be implemented by another class")

    def logFileExists(self, path_to_log):
        raise Exception("The method must be implemented by another class")