#Python 3.8.2
##############################
#
#   impact.py
#
##############################

class Impact:
    """
    This data class will represent an impact and will contain information about an specific impact.
    """
    def __init__(self, frame, impact_number, frame_number):
        self.frame = frame
        self.impact_number = impact_number
        self.frame_number = frame_number
        self.time = ""
    
    def setTime(self, time):
        self.time = time