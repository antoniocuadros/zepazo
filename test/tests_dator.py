#Python 3.8.2
##############################
#
#   tests_dator.py
#
##############################
import pytest
import cv2
import os
import runpy
import  argparse
from src.Dators.dator import Dator

################################################
#
# Checks if we cant create a Dator instance
#
################################################
def test_if_dator_created_then_error(capfd):  
    with pytest.raises(Exception) as e:
        
        dator = Dator()

    assert str(e.value) == "Non-instantiable class"
