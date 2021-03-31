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
parser.add_argument( "-mm", "--mousemask", type=int, help="Place num_masks rectangular masks  by clicking in first frame ")
parser.add_argument( "-cm", "--coordinatesmask",nargs='+', type=int, help="Place num_masks rectangular masks  by giving a list of points")


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
if(args.mousemask != None):
    video_analizer.selectAndApplyMask(args.mousemask)
else:
    if(args.coordinatesmask != None):
        if(len(args.coordinatesmask) % 2 != 0):
            parser.error("Coordinate list must be even")
        else:
            video_analizer.selectAndApplyMask(len(args.coordinatesmask), args.coordinatesmask)

#Proccessing
video_analizer.analyze()