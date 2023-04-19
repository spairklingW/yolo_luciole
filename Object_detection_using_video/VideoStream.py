# To make python 2 and python 3 compatible code
from __future__ import absolute_import

from threading import Thread
import time
import sys
import cv2
# pylint: disable=E1101
# pylint: disable=E0401
# Disabling linting that is not supported by Pylint for C extensions such as OpenCV. See issue https://github.com/PyCQA/pylint/issues/1955

# only for python > or equal 3
from queue import Queue

# This class reads all the video frames in a separate thread and always has the keeps only the latest frame in its queue to be grabbed by another thread


class VideoStream(object):
    def __init__(self, path, queueSize=3):
        self.stream = cv2.VideoCapture(path)
        print(f"{self.stream.get(cv2.CAP_PROP_FPS)} frames per second")
        self.fps = self.stream.get(cv2.CAP_PROP_FPS)
        self.stopped = False
        self.Q = Queue(maxsize=queueSize)

    def start(self):
        # start a thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        try:
            while True:
                i = 0
                while i < 60000:
                    i = i + 1

                if self.stopped:
                    return

                if not self.Q.full():
                    (grabbed, frame) = self.stream.read()

                    # if the `grabbed` boolean is `False`, then we have
                    # reached the end of the video file
                    if not grabbed:
                        self.stop()
                        return

                    self.Q.put(frame)

                    # Clean the queue to keep only the latest frame
                    while self.Q.qsize() > 1:
                        self.Q.get()

                #wait a defined time for processing images at fps pace
                #time.sleep(self.fps)

        except Exception as e:
            print("got error: "+str(e))

    def read(self):
        return self.Q.get()

    def more(self):
        return self.Q.qsize() > 0

    def is_stopped(self):
        return self.stopped

    def stop(self):
        self.stopped = True

    def __exit__(self, exception_type, exception_value, traceback):
        self.stream.release()