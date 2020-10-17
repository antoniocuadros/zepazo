#Python 3.8.2
##############################
#
#   Zepazo.py
#
##############################

import  argparse

parser = argparse.ArgumentParser(description="Zepazo: Get moon impacts frames")
parser.add_argument( "-v", "--video", type=str, help="Video file path to analize")
args = parser.parse_args()