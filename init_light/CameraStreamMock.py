# To make python 2 and python 3 compatible code
from __future__ import absolute_import
from threading import Thread
import cv2
from queue import Queue


class CameraStreamMock(object):

    def __init__(self):
        self.path = r'C:\Users\brene\source\repos\github\yolo_luciole\Object_dection_using_image\images\living_room.jpg'
        self.frame = cv2.imread(self.path)

    def get_frame(self):
        return self.frame