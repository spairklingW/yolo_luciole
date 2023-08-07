# To make python 2 and python 3 compatible code
from __future__ import absolute_import
from Utils import *


class Config(object):

    def __init__(self, config_yaml):
        self.config = config_yaml

    def get_yolo_folder_path(self):
        return self.config["detector"]["yolo"]["folder_path"]

    def get_yolo_labels_path(self):
        return self.get_yolo_folder_path() + "/" + self.config["detector"]["yolo"]["labels_path"]

    def get_yolo_weight_path(self):
        return self.get_yolo_folder_path() + "/" + self.config["detector"]["yolo"]["weight_path"]

    def get_yolo_cfg_path(self):
        return self.get_yolo_folder_path() + "/" + self.config["detector"]["yolo"]["cfg_path"]

    def get_yolo_confidence(self):
        return self.config["detector"]["yolo"]["confidence"]

    def get_yolo_threshold(self):
        return self.config["detector"]["yolo"]["threshold"]
