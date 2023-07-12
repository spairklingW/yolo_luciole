# To make python 2 and python 3 compatible code
from __future__ import absolute_import
import numpy as np
import cv2
import glob as glob
import os


class HOGDetector(object):
    def __init__(self, labelsPath, weightsPath, configPath):
        print("start yolo detector")
        self.LABELS = open(labelsPath).read().strip().split("\n")
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),
                                   dtype="uint8")
        self.weightsPath = weightsPath
        self.configPath = configPath

    def detect_person(self, frame, in_confidence, threshold):
        # load our YOLO object detector trained on COCO dataset (80 classes)
        # and determine only the *output* layer names that we need from YOLO
        net = cv2.dnn.readNetFromDarknet(self.configPath, self.weightsPath)
        ln = net.getLayerNames()
        ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

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

        image_paths = glob.glob('../input/*.jpg')
        for image_path in image_paths:
            image_name = image_path.split(os.path.sep)[-1]
            image = cv2.imread(image_path)
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

            cv2.imshow('HOG detection', image)
            cv2.imwrite(f"../outputs/{image_name}", image)
            cv2.waitKey(0)

        persons_pos = []
        return persons_pos

    def __exit__(self, exception_type, exception_value, traceback):
        print("quite yolo detector")