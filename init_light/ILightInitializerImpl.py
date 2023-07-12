# To make python 2 and python 3 compatible code
from __future__ import absolute_import
import time
import random
from ImageProcessor import *
from abc import ABC
import yaml


# create class interface
class ILightInitializerImpl(ABC):

    def _detect_lights_position_impl(self):
        print("detect lights position")

        for light in self.lights:
            self._process_images_impl(light)
            (cX, cY, frame_with_contours) = self.image_processor.find_object_position(
                self.frame_light_transition_candidate, self.background_frame)

            # show the image
            # cv2.imshow("Image circle", frame_with_contours)
            # cv2.waitKey(0)

            light.set_position(cX, cY)

    def _print_light_position_impl(self):
        image_all_lights = self.background_frame

        for light in self.lights:
            print("[INFO] light position for light")
            print(light.get_id())
            print(light.get_position()["x"])
            print(light.get_position()["x"])

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

    def _process_images_impl(self, light):

        cnt = 0
        self.max_sum_candidate = 0
        setup_time = 1  # second
        elapsed_time = 0

        while elapsed_time < setup_time:

            time_start = time.time()
            path = r'C:\Users\brene\source\repos\github\yolo_luciole\Object_dection_using_image\images\living_room.jpg'
            frame = cv2.imread(path)

            elapsed_time = elapsed_time + time.time() - time_start
            time_start = time.time()
            print("this is the elapsed time")
            print(elapsed_time)

            if 0.2 < elapsed_time < 0.7:

                self.set_light_on(light)
                #random.uniform(0, 1)*
                print(self.H)
                cv2.circle(frame, (int(random.uniform(0.2, 1.8)*self.H / 2), int(random.uniform(0.2, 1.8)*self.W / 2)), 7, (255, 255, 255), -1)
                # variant for real hardware
                # light.setIntensityUp
                print("in the cercle")
                # show the image
                cv2.imshow("Image circle", frame)
                cv2.waitKey(0)

            self.set_light_off(light)

            # if the frame dimensions are empty, grab them
            if self.W is None or self.H is None:
                (self.H, self.W) = frame.shape[:2]

            if cnt is 0:
                self.background_frame = frame

            # insert some code for processing the image and initializing
            if cnt is not 0:

                frame_opened = self.image_processor.process_image_from_diff(self.prev_frame, frame)
                self._compare_image_diff_to_max_diff_impl(cnt, frame_opened)
                #self._export_frame_to_video(out_image)

            self.prev_frame = frame
            cnt = cnt + 1
            elapsed_time = elapsed_time + time.time() - time_start

    # to be called by interface method
    def _compare_image_diff_to_max_diff_impl(self, cnt, frame_opened):

        # calculate the frame with biggest sum
        if cnt is 1:
            # first diff frame, store as potential to set up recurrence
            self.frame_light_transition_candidate = frame_opened
        else:
            sum_opened_frame = np.sum(frame_opened)
            if sum_opened_frame > self.max_sum_candidate:
                self.max_sum_candidate = sum_opened_frame
                self.frame_light_transition_candidate = frame_opened

    def _export_frame_to_video_impl(self, out_image):
        # check if the video writer is None
        global writer

        if writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter(self.output_video_path, fourcc, 30,
                                     (out_image.shape[1], out_image.shape[0]), True)

        rgb_frame = cv2.cvtColor(out_image, cv2.COLOR_GRAY2RGB)
        writer.write(rgb_frame)