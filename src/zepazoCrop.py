from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import  argparse
from Dators.fsdator import FSDator
import os


######################
#
# Defining arguments
#
######################
parser = argparse.ArgumentParser(description="ZepazoCrop: Cuts a portion of the video")
parser.add_argument( "-vo", "--videoOriginal", type=str, help="Video file path to crop")
parser.add_argument( "-vc", "--videoCropped", type=str, help="Video path to save cropped video")
parser.add_argument( "-ss", "--secondStart", type=int, help="Second when starts new cropped video")
parser.add_argument( "-se", "--secondEnd", type=int, help="Second when ends new cropped video")

#Getting arguments
args = parser.parse_args()


######################
#
# Checking arguments
#
######################

#Checks Original video
if(args.videoOriginal == None):
    parser.error(("Original video to crop (-vo) must be defined."))

else:
    folder = os.path.dirname(args.videoOriginal)
    dator = FSDator(folder)

if( args.videoOriginal == None or dator.videoExists(args.videoOriginal) == False):
    parser.error("Original video to crop (-vo) must exists.")

#Checks path to cropped video
if(args.videoCropped == None):
    parser.error(("Cropped video path/name (-vo) must be defined."))
else:
    if(dator.videoExists(args.videoCropped) == True):
        parser.error("Cropped video (-vc) error, there is another file with the same name.")

#Checks seconds start and senconds end
if(args.secondStart == None or args.secondEnd == None):
        parser.error("Second start (-ss) and Second end (-se) must be specified")
else:
    if(args.secondStart > args.secondEnd):
        parser.error("Second start (-ss) must be minor than Second end (-se)")







