#Python 3.8.2
##############################
#
#   Zepazo.py
#
##############################

import  argparse
from Analyzers.video_utilities import *
from sys import argv
from pathlib import Path


#################
#
#   Arguments
#
#################
#Needed to Sphinx
ARGS_DOCS = ['-v', '../videos/test.mp4']

parser = argparse.ArgumentParser(description="Zepazo: Get moon impacts frames")
parser.add_argument( "-v", "--video", type=str, help="Video file path to analize")
parser.add_argument( "-s", "--show", type=bool, help="Show video during analysis")
parser.add_argument( "-m", "--mask", type=int, help="Place num_masks rectangular masks")


if ( Path(argv[0]).name != 'sphinx-build' ):
    args = parser.parse_args()
else:
    args = parser.parse_args(ARGS_DOCS)
#################
#
#  Program
#
#################
video_analizer = VideoAnalyzer(args)

#Pre Processing
# -> Apply a mask
if(args.mask != None):
    video_analizer.selectAndApplyMask()

#Proccessing
video_analizer.analyze()