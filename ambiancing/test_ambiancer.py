from __future__ import absolute_import
from YoloDetector import *
from VideoStream import *
from Utils import *
from Light import *
from Ambiancer import *
from Config import *
import math

#python app.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco --light_pos_file ../init_light/light_pos.yaml

def test_ambiancer_video():
    light_pos_file_path = "light_pos_test.yaml"
    metadata_file_path = "../init_light/metadata.yaml"
    config = Config(load_yaml("config.yaml"))
    detector = "yolo"
    ambiancer = Ambiancer(config, light_pos_file_path, metadata_file_path, detector)

    person_pos = [{"x": 280, "y": 415}, {"x": 250, "y": 350}, {"x": 390, "y": 390}, {"x": 100, "y": 100}]

    intensities_lights_all_persons = ambiancer.fill_light_intensity(person_pos)
    ambiancer.compute_lights_intensity_per_person(intensities_lights_all_persons)
    lights = ambiancer.get_lights()
    frame = cv2.imread("images/dining_table.jpg")

    for light in lights:
        print("print dimensions image")
        light.show()
        cv2.circle(frame, (int(light.get_position()["x"]), int(light.get_position()["y"])),
                   int(light.get_intensity()*50), (255, 255, 255), -1)

    for pers_pos in person_pos:
        print("person pos")
        print(int(pers_pos["x"]))
        print(int(pers_pos["y"]))
        cv2.circle(frame, (int(pers_pos["x"]), int(pers_pos["y"])),
                   10, (0, 0, 255), -1)

    cv2.imshow("Image final", frame)
    cv2.waitKey(0)


    print("print the intensities: end of test")
    print(intensities_lights_all_persons)

    print("print the sum of the intensities: should be around 1")
    print(sum(intensities_lights_all_persons.values()))

    assert 1 == 2