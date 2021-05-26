import  argparse
from Dators.fsdator import FSDator


######################
#
# Defining arguments
#
######################
parser = argparse.ArgumentParser(description="ZepazoVerify: From two log files checks if there is an impact taking place in time in the same period")
parser.add_argument( "-lgf1", "--logFile1", type=str, help="Log file from the first video")
parser.add_argument( "-lgf2", "--logFile2", type=str, help="Log file from the second video")

#Getting arguments
args = parser.parse_args()


######################
#
# Checking arguments
#
######################