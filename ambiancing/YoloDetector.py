# To make python 2 and python 3 compatible code
from __future__ import absolute_import
import numpy as np
import cv2
from IDetector import *


class YoloDetector(IDetector):
    def __init__(self, config):
        print("start yolo detector")
        self.config = config

        # load the COCO class labels our YOLO model was trained on
        self.labelsPath = config.get_yolo_labels_path()
        # derive the paths to the YOLO weights and model configuration
        self.weightsPath = config.get_yolo_weight_path()
        self.configPath = config.get_yolo_cfg_path()

        self.LABELS = open(self.labelsPath).read().strip().split("\n")
        np.random.seed(42)
        self.COLORS = np.random.randint(0, 255, size=(len(self.LABELS), 3),
                                   dtype="uint8")

        self.in_confidence = config.get_yolo_confidence()
        self.threshold = config.get_yolo_threshold()

    def detect_person(self, frame):
        # load our YOLO object detector trained on COCO dataset (80 classes)
        # and determine only the *output* layer names that we need from YOLO
        net = cv2.dnn.readNetFromDarknet(self.configPath, self.weightsPath)
        ln = net.getLayerNames()
        ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

        (W, H) = (None, None)
        # if the frame dimensions are empty, grab them
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        # construct a blob from the input frame and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes
        # and associated probabilities
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)

        # initialize our lists of detected bounding boxes, confidences,
        # and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []
        persons_pos = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)

                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.in_confidence:
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates,
                    # confidences, and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.in_confidence, self.threshold)

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the frame
                # color = [int(c) for c in COLORS[classIDs[i]]]
                color = [int(c) for c in self.COLORS[classIDs[i]]]

                text = "{}: {:.4f}".format(self.LABELS[classIDs[i]],
                                           confidences[i])
                class_object = self.LABELS[classIDs[i]]

                if class_object == "person":
                    # cv2.putText(frame, text, (x, y - 5),
                    # cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.circle(frame, (x + int(w/2), y + int(h/2)), 7, (255, 255, 255), -1)
                    persons_pos.append({"x" : x + int(w/2), "y" : y + int(h/2)})

        return persons_pos

    def __exit__(self, exception_type, exception_value, traceback):
        print("quite yolo detector")