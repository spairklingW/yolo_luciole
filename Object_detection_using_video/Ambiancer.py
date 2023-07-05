# To make python 2 and python 3 compatible code
from __future__ import absolute_import
from YoloDetector import *
from VideoStream import *
from Utils import *
from Light import *
import math


class Ambiancer(object):

    def __init__(self, labelsPath, weightsPath, configPath, light_pos_file_path):
        self.yolo_detector = YoloDetector(labelsPath, weightsPath, configPath)
        self.lights = self.set_up_ligths(load_yaml(light_pos_file_path)["lights_position"])
        self.frames_proc = []
        self.H = None
        self.W = None

    def initialize(self):
        print("initialize function of Ambiancer")

    def set_up_ligths(self, lights_pos):
        lights = []

        for light_pos in lights_pos:
            lights.append(Light(light_pos["id"], light_pos["x"], light_pos["y"]))
        return lights

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
            self.H, self.W = frame.shape[:2]

            persons_pos = self.yolo_detector.detect_person(frame, confidence, threshold)

            print("persons position")
            print(persons_pos)
            self.update_ambiance(persons_pos)
            self.display_ligths_on_frame(frame)

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

    def display_ligths_on_frame(self, frame):
        for light in self.lights:
            print("this is the light intensity")
            print(light.get_intensity())
            cv2.circle(frame, (light.get_position()["x"], light.get_position()["y"]), int(7*(40*light.get_intensity()/100)), (150, 255, 150), -1)

            cv2.imshow("Image", frame)
            cv2.waitKey(0)

    def convert_rel_light_pos(self):
        for light in self.lights:
            light.set_position(int(light.get_position()["x"]*self.W), int(light.get_position()["y"]*self.H))
            light.show_position()

    def update_ambiance(self, persons_pos):
        self.convert_rel_light_pos()
        lights_intensity, sum_intensities = self.fill_light_intensity(persons_pos)
        self.compute_lights_intensity(lights_intensity, sum_intensities)
        self.power_intensity()

    def distance_person_to_light(self, light, person_pos):

        p_light = [light.get_position()["x"], light.get_position()["y"]]
        p_person = [person_pos["x"], person_pos["y"]]
        print("distance with")
        print(p_light)
        print(p_person)
        print("Warning : This is a mocked answer until distance is really computed !")
        #return 12
        return math.dist(p_light, p_person)   # from python3.9 on

    def fill_light_intensity(self, persons_pos):

        lights_intensity = {}
        sum_intensities = 0

        for light in self.lights:
            light_intensity = []
            for person_pos in persons_pos:
                light_intensity.append(self.distance_person_to_light(light, person_pos))

            sum_intensities = sum_intensities + sum(light_intensity)

            lights_intensity[light.get_id()] = sum(light_intensity)

        print("this is the intensity !!!!")
        print(sum_intensities)
        return lights_intensity, sum_intensities

    def get_light_by_id(self, id):
        for light in self.lights:
            if light.get_id() == id:
                return light

    def compute_lights_intensity(self, lights_intensity, sum_intensities):
        print("lights intensities")
        print(lights_intensity)
        print(type(lights_intensity))
        for key_id in lights_intensity:
            value_light_intensity = lights_intensity[key_id]
            light = self.get_light_by_id(key_id)
            light.udpate_intensity(int(value_light_intensity/sum_intensities*100))

    def power_intensity(self):
        for light in self.lights:
            light.power_intensity()

    def show_images(self, show_images):
        if show_images:
            for f in self.frames_proc:
                # show the output image
                cv2.imshow("Image", f)
                cv2.waitKey(0)

    def __exit__(self, exception_type, exception_value, traceback):
        print("quite yolo detector")