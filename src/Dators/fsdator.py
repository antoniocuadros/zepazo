#Python 3.8.2
##############################
#
#   fsdator.py
#
##############################

from .dator import Dator
import os
from cv2 import cv2
import json
from pathlib import Path
import mimetypes
import ntpath

class FSDator(Dator):
    """
    This class will implement Dator methods to save data in files and folders.
    """
    def __init__(self, path):
        #Checks if folder in path exists
        if(path !=None and os.path.exists(path) == False and os.path.isfile(path)): #Folder doesn't exists, we create it
            os.mkdir(path)
        
        self.path = path



    
    def saveFrame(self, name, frame):
        """
        Save an image in a selected directory.
        :param: frame: the image to save.
        :type: frame: numpy.ndarray.

        :param: name: name of the image to save.
        :type: frame1: str.
        """
        path_to_image = ""
        if(self.path[-1] != "/"):
                path_to_image =  self.path + "/" + name
        else:
            path_to_image =  self.path + name
            
        cv2.imwrite(path_to_image + ".png", frame)

    def saveSurroundingFrames(self, num_frames, current_frame, name,videopath):
        if(self.path[-1] != "/"):
                path_to_image =  self.path + "/" + name
        else:
            path_to_image =  self.path + name

        init_frame = current_frame - num_frames
        end_frame = current_frame + num_frames

        video_capturer = cv2.VideoCapture(videopath)

        count = init_frame
        video_capturer.set(cv2.CAP_PROP_POS_FRAMES, init_frame)
        name_count = 0
        while count<=end_frame:
            path_to_image2 = path_to_image
            path_to_image2 = path_to_image2 + "." + str(name_count)
            ret,frame = video_capturer.read()
            count+=1

            if(name_count != num_frames):
                cv2.imwrite(path_to_image2 + ".png", frame)

            name_count+=1
    
    def saveLog(self, impacts):
        if(self.path[-1] != "/"):
            path_to_image =  self.path + "/"
        else:
            path_to_image = self.path

        log = {}

        imp = []
        
        for impact in impacts:
            data_element = {}
            data_element['impact_number'] = impact.impact_number
            data_element['impact_frame_number'] = impact.frame_number
            data_element['impact_time'] = impact.time
            
            imp.append(data_element)
        
    
        with open(path_to_image + 'log.json', 'w') as json_file:
            json.dump(imp, json_file, indent=4, separators=(',', ': '), sort_keys=True)


    def videoExists(self, path_to_video):
        file = Path(path_to_video)
        if(file.is_file() == False):
            return False
        else:
            try:
                if(mimetypes.guess_type(path_to_video)[0].startswith('video') == False):
                    return False
            except:
                return False
            else:
                return True

    def logFileExists(self, path_to_log):
        file = Path(path_to_log)
        if(file.is_file() == False):
            return False
        else:
            try:
                with open(path_to_log, 'r') as json_file:
                    args = json.load(json_file)
            except:
                return False
          
            return True

    def loadLogFile(self, path_to_log):
        with open(path_to_log, 'r') as json_file:
            args = json.load(json_file)
        return args

    def saveCoincidenceLog(self, path_to_log1, path_to_log2, path_to_save, data):
        
        log = []
        for coincidence in data:
            json_args = {
                    'log_1_impact':coincidence['log_1_impact'],
                    'log_2_impact':coincidence['log_2_impact'],
                    'difference':coincidence['sub'],
                    'path_to_log1':path_to_log1,
                    'path_to_log2':path_to_log2
                }
            log.append(json_args)

        with open(path_to_save, 'w') as json_file:
            json.dump(log, json_file, indent=4, separators=(',', ': '), sort_keys=True)

    def correctPathToSaveJSON(self, path_to_json):
        path_without_name = os.path.dirname(path_to_json)
        
        check = True
        if(os.path.isdir(path_without_name) == False):
            check = False

        if(ntpath.basename(path_to_json).endswith(".json") == False):
            check = False
        return check