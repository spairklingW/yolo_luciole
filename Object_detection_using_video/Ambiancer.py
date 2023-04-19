# To make python 2 and python 3 compatible code
from __future__ import absolute_import

from threading import Thread
import numpy as np
import argparse
import imutils
import time
import cv2
import os
from VideoStream import *
import time
import sys
import cv2
from YoloDetector import *
from VideoStream import *
# pylint: disable=E1101
# pylint: disable=E0401
# Disabling linting that is not supported by Pylint for C extensions such as OpenCV. See issue https://github.com/PyCQA/pylint/issues/1955

# only for python > or equal 3
from queue import Queue

# This class reads all the video frames in a separate thread and always has the keeps only the latest frame in its queue to be grabbed by another thread


#idea to debug : add the app content to the controller.py and performs
#some asserts functions to check each data, blob, layer, etc
#avoid copies of frames, etc

class Ambiancer(object):

    def __init__(self, labelsPath, weightsPath, configPath):
        self.yolo_detector = YoloDetector(labelsPath, weightsPath, configPath)
        self.frames_proc = []

    def initialize(self):
        print("initialize function of Ambiancer")

    def start_stream_proc(self, input_stream_path, confidence, threshold, output_file_path):
        writer = None

        video_stream = VideoStream(input_stream_path)
        video_stream.start()

        while True:

            print("increment")

            if video_stream.is_stopped():
                print("video stream is stopped")
                break

            frame = video_stream.read()

            #frame = cv2.imread('C:\\Users\\brene\\source\\repos\\github\\yolo_luciole\\images\\gospel.jpg')
            #cv2.imshow("Image", frame)
            #print(frame.shape[:2])
            #cv2.waitKey(0)

            self.yolo_detector.detect_person(frame, confidence, threshold)

            # check if the video writer is None
            if writer is None:
                # initialize our video writer
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                writer = cv2.VideoWriter(output_file_path, fourcc, 30,
                                         (frame.shape[1], frame.shape[0]), True)

            self.frames_proc.append(frame)

            # write the output frame to disk
            writer.write(frame)

        # release the file pointers
        print("[INFO] cleaning up...")
        writer.release()

    def show_images(self, show_images):
        if show_images:
            for f in self.frames_proc:
                # show the output image
                cv2.imshow("Image", f)
                cv2.waitKey(0)

    def get_net(self):
        return self.yolo_detector.get_net()

    def get_weightpath(self):
        return self.yolo_detector.get_weightpath()

    def get_configpath(self):
        return self.yolo_detector.get_configpath()

    def get_confidence(self):
        return self.yolo_detector.get_confidence()

    def get_scores(self):
        return self.yolo_detector.get_scores()

    def get_layerout(self):
        return self.yolo_detector.get_layerOut()

    def __exit__(self, exception_type, exception_value, traceback):
        print("quite yolo detector")