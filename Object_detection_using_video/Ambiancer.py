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
        intensities_lights_all_persons = self.fill_light_intensity(persons_pos)
        #self.compute_lights_intensity_per_person(lights_intensity_per_person, sum_intensities_per_person)
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

        lights_intensity_per_person = {}
        lights_intensity_norm = {}
        distances_light_person = []
        Itotal_person = []
        Itotal_person_sum = 0

        intensities_lights_all_persons = {}
        n_person = len(persons_pos)

        for person_pos in persons_pos:
            #create the list of all intensities from person to all lights
            for light in self.lights:
                distances_light_person.append(self.distance_person_to_light(light, person_pos))

            # Ia = S/A
            for light in self.lights:
                lights_intensity_per_person[light.get_id()] = int(sum(distances_light_person)/self.distance_person_to_light(light, person_pos))
                Itotal_person.append(lights_intensity_per_person[light.get_id()])

            Itotal_person_sum = sum(Itotal_person)  # maybe if dict returns the 2 values of the 2 columns, just grab the second one
            #normalize this intensity sum I = 1
            for light in self.lights:
                #vector id_light: list of intensities normalized for all persons fed one by one
                lights_intensity_norm[light.get_id()].append(int(lights_intensity_per_person[light.get_id()]/Itotal_person_sum))

            for light in self.lights:
                # N personnes, intensity of a light is the average of all intensities
                intensities_lights_all_persons[light.get_id()] = int(sum(lights_intensity_norm[light.get_id()])/n_person)

        return intensities_lights_all_persons

    def get_light_by_id(self, id):
        for light in self.lights:
            if light.get_id() == id:
                return light

    def compute_lights_intensity_per_person(self, intensities_lights_all_persons):
        print("lights intensities")
        print(intensities_lights_all_persons)
        print(type(intensities_lights_all_persons))
        for key_id in intensities_lights_all_persons:
            value_light_intensity = intensities_lights_all_persons[key_id]
            light = self.get_light_by_id(key_id)
            light.udpate_intensity(value_light_intensity)  #see calculation, Ia = S/A, then normalize

        #normalize
        #for key_id in lights_intensity_per_person:



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