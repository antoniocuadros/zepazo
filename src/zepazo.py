#Python 3.8.2
##############################
#
#   Zepazo.py
#
##############################

import  argparse
from video_utilities import *


#################
#
#   Arguments
#
#################
parser = argparse.ArgumentParser(description="Zepazo: Get moon impacts frames")
parser.add_argument( "-v", "--video", type=str, help="Video file path to analize")
args = parser.parse_args()

#################
#
#  Program
#
#################
video_analizer = VideoAnalizer(args)
video_analizer.analyze()