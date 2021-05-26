import  argparse
from Dators.fsdator import FSDator
import os
from datetime import datetime


######################
#
# Defining arguments
#
######################
parser = argparse.ArgumentParser(description="ZepazoVerify: From two log files checks if there is an impact taking place in time in the same period")
parser.add_argument( "-lgf1", "--logFile1", type=str, help="Log file from the first video")
parser.add_argument( "-lgf2", "--logFile2", type=str, help="Log file from the second video")
parser.add_argument( "-rlfg", "--resultingLogFile", type=str, help="Log file where to save analysis")

#Getting arguments
args = parser.parse_args()


######################
#
# Checking arguments
#
######################
#Checks the first log file
if(args.logFile1 == None):
    parser.error(("First log file (-lgf1) must be defined."))
else:
    folder = os.path.dirname(args.logFile1)
    dator = FSDator(folder)

if(args.logFile1 == None or dator.logFileExists(args.logFile1) == False):
    parser.error(("First log file (-lgf1) must be defined and exists."))


#Checks the second log file
if(args.logFile2 == None):
    parser.error(("Second log file (-lgf2) must be defined."))
else:
    folder = os.path.dirname(args.logFile2)
    dator = FSDator(folder)

if(args.logFile2 == None or dator.logFileExists(args.logFile2) == False):
    parser.error(("Second log file (-lgf1) must be defined and exists."))


#Checks the resulting log file path
if(args.resultingLogFile == None):
    parser.error(("Resulting log file (-rlfg) must be defined."))
else:
    folder = os.path.dirname(args.resultingLogFile)
    dator = FSDator(folder)

if(args.resultingLogFile == None or dator.correctPathToSaveJSON(args.resultingLogFile) == False):
    parser.error(("Resulting log file (-rlfg) must be defined and have .json extension."))


######################
#
# Verifying impacts
#
######################
#Load first Json
impacts_1 = dator.loadLogFile(args.logFile1)

#Load second Json
impacts_2 = dator.loadLogFile(args.logFile2)

data = []
for impact_log_1 in impacts_1:
    time = impact_log_1['impact_time']
    date = datetime.strptime(time, '%H:%M:%S')
    
    
    for impact_log_2 in impacts_2:
        time2 = impact_log_2['impact_time']

        date2 = datetime.strptime(time2, '%H:%M:%S')

        if(date > date2):
            sub = abs((date - date2).seconds)

        else:
            sub = abs((date2 - date).seconds)


        if(sub < 10):
            data.append({'log_1_impact': impact_log_1['impact_number'],'log_2_impact': impact_log_2['impact_number'], 'sub':sub})
            
    
    dator.saveCoincidenceLog(args.logFile1, args.logFile2, args.resultingLogFile, data)        