# To make python 2 and python 3 compatible code
from __future__ import absolute_import
import time
import random
from ImageProcessor import *
from ambiancing.VideoStream import *
from abc import ABC
import yaml


# create class interface
class ILightInitializerImpl(ABC):

    def _detect_lights_position_impl(self):
        print("detect lights position")

        self.__shut_off_all_lights()

        for light in self.lights:
            self.process_images_impl_from_usecase(light)
            (cX, cY, frame_with_contours) = self.image_processor.find_object_position(
                self.frame_light_transition_candidate, self.background_frame)

            # show the image
            # cv2.imshow("Image circle", frame_with_contours)
            # cv2.waitKey(0)

            light.set_position(cX, cY)

    def __shut_off_all_lights(self):
        for light in self.lights:
            print("show the light specs")
            light.show()
            light.shut_off()

    def _print_light_position_impl(self):
        image_all_lights = self.background_frame

        for light in self.lights:
            print("[INFO] light position for light")
            print(light.get_id())
            print(light.get_position()["x"])
            print(light.get_position()["y"])

            cv2.circle(image_all_lights, (light.get_position()["x"], light.get_position()["y"]), 7, (255, 255, 255), -1)

        # show the image
        cv2.imshow("Image circle", image_all_lights)
        cv2.waitKey(0)

    def _get_metadata_impl(self)-> dict:
        metadata = {}
        metadata["H"] = self.H
        metadata["W"] = self.W

        return metadata

    def _get_lights_position_as_list_impl(self) -> dict:

        lights_position = []
        for light in self.lights:
            lights_position.append({"id": light.get_id(), "x": light.get_position()["x"], "y": light.get_position()["y"]})

        return {"lights_position": lights_position}

    def _get_lights_rel_position_as_list_impl(self):
        lights_position = []
        for light in self.lights:
            lights_position.append(
                {"id": light.get_id(),
                 "x": int(light.get_position()["x"]/self.W*100)/100,
                 "y": int(light.get_position()["y"]/self.H*100)/100})


        print("print the positions rel")
        print(self.W)
        print(self.H)
        print(int(light.get_position()["x"]/self.W*100)/100)
        print(int(light.get_position()["y"] / self.H * 100) / 100)

        return {"lights_position": lights_position}

    def _process_images_impl_general(self, frame, cnt):
        # careful, make sure the H and W are well derived from the current frame, looks like they are init from somewhere else
        if self.W is None or self.H is None:
            (self.H, self.W) = frame.shape[:2]

        if cnt is 0:
            print("setup the background frame")
            print(self.H, self.W)
            self.background_frame = frame

        # insert some code for processing the image and initializing
        if cnt is not 0:
            print("count is not null for once")

            frame_opened = self.image_processor.process_image_from_diff(self.prev_frame, frame)
            self._compare_image_diff_to_max_diff_impl(cnt, frame_opened)
            # self._export_frame_to_video_impl(frame_opened)

        self.prev_frame = frame.copy()
        cnt = cnt + 1

        return cnt

    # to be called by interface method
    def _compare_image_diff_to_max_diff_impl(self, cnt, frame_opened):

        # calculate the frame with biggest sum
        if cnt is 1:
            # first diff frame, store as potential to set up recurrence
            self.frame_light_transition_candidate = frame_opened
        else:
            sum_opened_frame = np.sum(frame_opened)
            print("print the sum")
            print(sum_opened_frame)
            if sum_opened_frame > self.max_sum_candidate:
                self.max_sum_candidate = sum_opened_frame
                print("print the max candidate")
                print(self.max_sum_candidate)
                self.frame_light_transition_candidate = frame_opened

    def _export_frame_to_video_impl(self, out_image):
        # check if the video writer is None
        global writer

        writer = None

        if writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter(self.output_video_path, fourcc, 30,
                                     (out_image.shape[1], out_image.shape[0]), True)

        rgb_frame = cv2.cvtColor(out_image, cv2.COLOR_GRAY2RGB)
        writer.write(rgb_frame)