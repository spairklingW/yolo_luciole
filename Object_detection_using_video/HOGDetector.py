# To make python 2 and python 3 compatible code
from __future__ import absolute_import
import cv2
from IDetector import *


class HOGDetector(IDetector):
    def __init__(self, config):
        print("start yolo detector")
        self.config = config
        pass

    def detect_person(self, frame):

        persons_pos = []
        (W, H) = (None, None)
        # if the frame dimensions are empty, grab them
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        ############################################# HOG descriptor
        '''
        NOTE:
        This python script uses the default people detector provided by OpenCV to
        detect people in photos
        USAGE:
        python hog_detector.py
        '''

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        image = frame
        if image.shape[1] < 400:  # if image width < 400
            (height, width) = image.shape[:2]
            ratio = width / float(width)  # find the width to height ratio
            image = cv2.resize(image,
                               (400, height * ratio))  # resize the image according to the width to height ratio

        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        rects, weights = hog.detectMultiScale(img_gray, winStride=(2, 2), padding=(10, 10), scale=1.02)

        for i, (x, y, w, h) in enumerate(rects):
            if weights[i] < 0.13:
                continue
            elif weights[i] < 0.3 and weights[i] > 0.13:
                pass
                # cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            if weights[i] < 0.7 and weights[i] > 0.3:
                pass
                # cv2.rectangle(image, (x, y), (x+w, y+h), (50, 122, 255), 2)
            if weights[i] > 0.95:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                persons_pos.append({"x": x + int(w / 2), "y": y + int(h / 2)})

        cv2.imshow('HOG detection', image)
        cv2.waitKey(0)

        return persons_pos

    def __exit__(self, exception_type, exception_value, traceback):
        print("quite yolo detector")