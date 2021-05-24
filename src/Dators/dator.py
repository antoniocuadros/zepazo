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