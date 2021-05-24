#Python 3.8.2
##############################
#
#   dator.py
#
##############################

class Dator:
    """
    This 'abstract' class will help to have .
    """
    def __init__(self):
        if(isinstance(self, Dator)):
            raise Exception("Non-instantiable class")

    
    def saveFrame(self):
        raise Exception("The method must be implemented by another class")