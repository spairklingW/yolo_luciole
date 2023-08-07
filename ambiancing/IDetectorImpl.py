# To make python 2 and python 3 compatible code
from __future__ import absolute_import
from abc import ABC
#from YoloDetector import *
#from HOGDetector import *


# create class interface
class IDetectorImpl(ABC):

    # check to declare it under __init__
    def _init_class(self, detector_class, config):

        detector = None
        if detector_class == "yolo":
            print("THIS IS THE YOLO DETECTOR")
            #detector = YoloDetector(config)
        elif detector_class == "hog":
            print("THIS IS THE HOG DETECTOR")
            #detector = HOGDetector()

        return detector
