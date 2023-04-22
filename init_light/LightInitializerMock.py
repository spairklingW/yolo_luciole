# To make python 2 and python 3 compatible code
from __future__ import absolute_import
from Light import *
from CameraStreamMock import *
from ImageProcessor import *
import time
import random


# create class interface
class LightInitializerMock(object):

    def __init__(self):
        self.lights = []
        self.frame_mock = self.get_frame()
        self.prev_frame = None
        self.diff = None
        self.frame_light_transition_candidate = None
        self.background_frame = None
        self.output_video_path = None
        self.H = None
        self.W = None
        self.image_processor = ImageProcessor()
        self.max_sum_candidate = 0

    def get_frame(self):
        camera_stream = CameraStreamMock()
        return camera_stream.get_frame()

    def detect_lights(self):
        print("detect the lights")

        # detect which raspi pins are in used || set up a random number of lights
        # in the detector
        light_number = 4
        for i in range(0, light_number):
            self.lights.append(Light(i))

    def detect_lights_position(self):
        print("detect lights position")

        for light in self.lights:
            self.process_images(light)
            (cX, cY, frame_with_contours) = self.image_processor.find_object_position(self.frame_light_transition_candidate, self.background_frame)

            # show the image
            # cv2.imshow("Image circle", frame_with_contours)
            # cv2.waitKey(0)

            light.set_position(cX, cY)

    def print_light_position(self):

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

    def process_images(self, light):

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
                #random.uniform(0, 1)*
                print(self.H)
                cv2.circle(frame, (int(random.uniform(0.2, 1.8)*self.H / 2), int(random.uniform(0.2, 1.8)*self.W / 2)), 7, (255, 255, 255), -1)
                # variant for real hardware
                # light.setIntensityUp
                print("in the cercle")
                # show the image
                cv2.imshow("Image circle", frame)
                cv2.waitKey(0)

            # if the frame dimensions are empty, grab them
            if self.W is None or self.H is None:
                (self.H, self.W) = frame.shape[:2]

            if cnt is 0:
                self.background_frame = frame

            # insert some code for processing the image and initializing
            if cnt is not 0:

                frame_opened = self.image_processor.process_image_from_diff(self.prev_frame, frame)
                self.compare_image_diff_to_max_diff(cnt, frame_opened)
                #self.export_frame_to_video(out_image)

            self.prev_frame = frame
            cnt = cnt + 1
            elapsed_time = elapsed_time + time.time() - time_start

    def compare_image_diff_to_max_diff(self, cnt, frame_opened):

        # calculate the frame with biggest sum
        if cnt is 1:
            # first diff frame, store as potential to set up recurrence
            self.frame_light_transition_candidate = frame_opened
        else:
            sum_opened_frame = np.sum(frame_opened)
            if sum_opened_frame > self.max_sum_candidate:
                self.max_sum_candidate = sum_opened_frame
                self.frame_light_transition_candidate = frame_opened

    def export_frame_to_video(self, out_image):
        # check if the video writer is None
        global writer

        if writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter(self.output_video_path, fourcc, 30,
                                     (out_image.shape[1], out_image.shape[0]), True)

        rgb_frame = cv2.cvtColor(out_image, cv2.COLOR_GRAY2RGB)
        writer.write(rgb_frame)

    def __exit__(self, exception_type, exception_value, traceback):
        print("quite yolo detector")