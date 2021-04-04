#Python 3.8.2
##############################
#
#   Zepazo.py
#
##############################

import  argparse
from Analyzers.video_utilities import VideoAnalyzer
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
parser.add_argument( "-l", "--detectionlimit", type=int, help="Detection limit (1-255) Default 50")
parser.add_argument( "-cl", "--circlelimit", type=int, help="Moon contour detection limit (1-255) Default ~33 calculated while analysis")
parser.add_argument( "-hcl", "--helpcirclelimit", type=bool, help="Interface to adjust circlelimit param")

if ( Path(argv[0]).name != 'sphinx-build' ):
    args = parser.parse_args()
else:
    args = parser.parse_args(ARGS_DOCS)


if(args.detectionlimit != None):
    if(args.detectionlimit < 1 or args.detectionlimit > 255):
        parser.error("Detection limit (-l) must be between 1 and 255")

if(args.video == None):
        parser.error("Video (-v) must be defined")

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

# -> Interface to adjust circlelimit argument
if(args.helpcirclelimit != None and args.helpcirclelimit == True):
    video_analizer.selectAndApplyCircleLimitArgment()

#Proccessing
video_analizer.analyze()