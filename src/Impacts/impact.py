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
    def __init__(self, frame, impact_number, video_time):
        self.frame = frame
        self.impact_number = impact_number
        self.video_time = video_time