# To make python 2 and python 3 compatible code
from __future__ import absolute_import
from YoloDetector import *
from VideoStream import *
from Utils import *
from Light import *
import math


class Ambiancer(object):

    def __init__(self, labelsPath, weightsPath, configPath, light_pos_file_path, metadata_file_path):
        self.H = load_yaml(metadata_file_path)["H"]
        self.W = load_yaml(metadata_file_path)["W"]
        self.yolo_detector = YoloDetector(labelsPath, weightsPath, configPath)
        self.lights = self.set_up_ligths(load_yaml(light_pos_file_path)["lights_position"])
        self.frames_proc = []

    def initialize(self):
        print("initialize function of Ambiancer")

    def set_up_ligths(self, lights_pos):
        lights = []
        print("LIGHT POS ")
        print(lights_pos)
        print(self.W)
        print(self.H)

        for light_pos in lights_pos:
            lights.append(Light(light_pos["id"], light_pos["x"]*self.W, light_pos["y"]*self.H))
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

            self.show_results(frame, persons_pos)
            self.frames_proc.append(frame)

            # write the output frame to disk
            writer.write(frame)

        # release the file pointers
        print("[INFO] cleaning up...")
        writer.release()

    def show_results(self, frame, person_pos):
        for light in self.lights:
            print("print dimensions image")
            light.show()
            print(int(light.get_position()["x"]))
            print(int(light.get_position()["y"]))
            cv2.circle(frame, (int(light.get_position()["x"]), int(light.get_position()["y"])),
                       int(light.get_intensity() * 50), (255, 255, 255), -1)

        for pers_pos in person_pos:
            print("person pos")
            print(int(pers_pos["x"]))
            print(int(pers_pos["y"]))
            cv2.circle(frame, (int(pers_pos["x"]), int(pers_pos["y"])),
                       10, (0, 0, 255), -1)

    def display_ligths_on_frame(self, frame):
        for light in self.lights:
            print("this is the light intensity")
            print(light.get_intensity())
            cv2.circle(frame, (light.get_position()["x"], light.get_position()["y"]), int(7*(40*light.get_intensity()/100)), (150, 255, 150), -1)

            cv2.imshow("Image", frame)
            cv2.waitKey(0)

    def convert_rel_light_pos(self):
        for light in self.lights:
            light.set_position(int(light.get_position()["x"]), int(light.get_position()["y"]))
            light.show_position()

    def update_ambiance(self, persons_pos):
        self.convert_rel_light_pos()
        intensities_lights_all_persons = self.fill_light_intensity(persons_pos)
        self.compute_lights_intensity_per_person(intensities_lights_all_persons)
        self.power_intensity()

    def distance_person_to_light(self, light, person_pos):

        p_light = [light.get_position()["x"], light.get_position()["y"]]
        p_person = [person_pos["x"], person_pos["y"]]
        print("distance with")
        print(p_light)
        print(p_person)
        print("Warning : This is a mocked answer until distance is really computed !")
        #return 12
        print("COMPUTE DISTANCE")
        return math.dist(p_light, p_person)   # from python3.9 on

    def fill_light_intensity(self, persons_pos):

        print("PERSON POS VALUE")
        print(persons_pos)
        lights_intensity_per_person = {}
        lights_intensity_norm = {}
        distances_light_person = []
        Itotal_person = []
        Itotal_person_sum = 0

        # initialize the lights_intensity_norms
        lights_intensity_norm_all_persons = {}
        lights_intensity_norm = {}
        for light in self.lights:
            lights_intensity_norm_all_persons[light.get_id()] = []
            lights_intensity_norm[light.get_id()] = []

        intensities_lights_all_persons = {}
        n_person = len(persons_pos)

        for person_pos in persons_pos:
            # create the list of all intensities from person to all lights
            for light in self.lights:
                distances_light_person.append(self.distance_person_to_light(light, person_pos))

            # Ia = S/A
            print("compute Intensity_l")
            for light in self.lights:
                lights_intensity_per_person[light.get_id()] = int(sum(distances_light_person)/self.distance_person_to_light(light, person_pos))
                Itotal_person.append(lights_intensity_per_person[light.get_id()])

            Itotal_person_sum = sum(Itotal_person)  # maybe if dict returns the 2 values of the 2 columns, just grab the second one
            print("intensities not normed")
            print(Itotal_person)
            print("Itotal_person_sum")
            print(Itotal_person_sum)
            # normalize this intensity sum I = 1
            for light in self.lights:
                print(light.show_position())
                print("PROCESSING  light with id:")
                print(light.get_id())
                print("intensity for a person")
                print(lights_intensity_per_person[light.get_id()])
                # vector id_light: list of intensities normalized for all persons fed one by one
                lights_intensity_norm[light.get_id()].append(lights_intensity_per_person[light.get_id()]/Itotal_person_sum)

        print("INTENSITIES NORMED")
        print(lights_intensity_norm)

        # NOT PART OF THE LOOP
        print("intensity in pourcent for all person for one light")
        for light in self.lights:
            # N persons, intensity of a light is the average of all intensities
            intensities_lights_all_persons[light.get_id()] = sum(lights_intensity_norm[light.get_id()])/n_person

        print("INTENSITIES ALL PERSONS")
        print(intensities_lights_all_persons)
        return intensities_lights_all_persons

    def get_light_by_id(self, id):
        for light in self.lights:
            if light.get_id() == id:
                return light

    def get_lights(self):
        return self.lights

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