# To make python 2 and python 3 compatible code
from __future__ import absolute_import
import cv2
import numpy as np


class ImageProcessor(object):

    def __init__(self, config):
        self.config = config
        print("Image Processor class")

    def find_object_position(self, frame_light_transition, background_frame):

        # compute bounding box on the frame_light_transition
        # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
        contours, hierarchy = cv2.findContours(image=frame_light_transition, mode=cv2.RETR_TREE,
                                               method=cv2.CHAIN_APPROX_NONE)

        # show the image
        #cv2.imshow("Image light transition", frame_light_transition)
        #cv2.waitKey(0)

        # draw contours on the original image
        cv2.drawContours(image=frame_light_transition, contours=contours, contourIdx=-1, color=(100, 100, 100), thickness=2,
                         lineType=cv2.LINE_AA)

        # Find the index of the largest contour (should be modified to most dense/ filled up)
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        largest_contour = contours[max_index]

        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(frame_light_transition, (x, y), (x + w, y + h), (100, 100, 100), 2)

        # cv2.imshow('threshold', image_copy)
        # cv2.waitKey(0)

        # see the results
        # cv2.imshow('None approximation', image_copy)
        # cv2.waitKey(0)

        # compute the center of the contour
        M = cv2.moments(largest_contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # draw the contour and center of the shape on the image
        cv2.drawContours(background_frame, [largest_contour], -1, (0, 255, 0), 2)
        cv2.circle(background_frame, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(background_frame, "center", (cX - 20, cY - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return cX, cY, background_frame

    def process_image_from_diff(self, prev_frame, current_frame):

        prev_frame_grey = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

        frame_grey = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        diff = cv2.absdiff(frame_grey, prev_frame_grey)

        print("this is the sum3")
        print(cv2.sumElems(diff))

        #if time:
            #cv2.imshow("print diff", diff)
            #cv2.waitKey(0)

        # find the best threshold :
        # 1- check how many bounding box are generated, increase the threshold until only stays, for the transition images (2)
        # 2- store max sum of pixel intensity of of bounding boxes per image, applied threshold of 0.90max. Do the same for all images
        # and keep in the end the one containing the max of the max -> should be the transition image, apply bounding box to it.
        # lower the threeshold if an error is found or no light is found !!!
        th, frame_thresh = cv2.threshold(diff, self.config.get_threshold(), 255, cv2.THRESH_BINARY)

        # opening to erase white noise on background (maybe not necessary after option above)
        kernel = np.ones((5, 5), np.uint8)
        frame_opened = cv2.morphologyEx(frame_thresh, cv2.MORPH_OPEN, kernel)

        return frame_opened