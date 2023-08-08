# To make python 2 and python 3 compatible code
from __future__ import absolute_import
from threading import Thread
import cv2
from queue import Queue


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

    def get_size(self):
        length = int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))
        print("this is the number of frame of the file")
        print(length)

    def is_stopped(self):
        return self.stopped

    def stop(self):
        self.stopped = True

    def __exit__(self, exception_type, exception_value, traceback):
        self.stream.release()