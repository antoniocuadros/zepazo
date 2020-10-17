#Python 3.8.2
##############################
#
#   Zepazo.py
#
##############################

import  argparse
from video_utilities import *

parser = argparse.ArgumentParser(description="Zepazo: Get moon impacts frames")
parser.add_argument( "-v", "--video", type=str, help="Video file path to analize")
args = parser.parse_args()

print(args.video)

video_analizer = VideoAnalizer(args.video)