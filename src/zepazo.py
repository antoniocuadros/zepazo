#Python 3.8.2
##############################
#
#   Zepazo.py
#
##############################

import  argparse
from video_utilities import *
from sys import argv
from pathlib import Path


#################
#
#   Arguments
#
#################
print(argv)
#Needed to Sphinx
ARGS_DOCS = ['-v', '../videos/test.mp4']

parser = argparse.ArgumentParser(description="Zepazo: Get moon impacts frames")
parser.add_argument( "-v", "--video", type=str, help="Video file path to analize")
parser.add_argument( "-s", "--show", type=bool, help="Show video during analysis")


if ( Path(argv[0]).name != 'sphinx-build' ):
    args = parser.parse_args()
    print (args)
else:
    args = parser.parse_args(ARGS_DOCS)
#################
#
#  Program
#
#################
video_analizer = VideoAnalizer(args)
video_analizer.analyze()