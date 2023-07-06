from __future__ import absolute_import
from YoloDetector import *
from VideoStream import *
from Utils import *
from Light import *
from Ambiancer import *
import math

#python app.py --input videos/airport.mp4 --output output/airport_output.avi --yolo yolo-coco --light_pos_file ../init_light/light_pos.yaml

def test_ambiancer():
    labelsPath = "yolo-coco/coco.names"
    weightsPath = "yolo-coco/yolov3.weights"
    configPath = "yolo-coco/yolov3.cfg"
    light_pos_file_path = "light_pos_test.yaml"
    metadata_file_path = "../init_light/metadata.yaml"
    ambiancer = Ambiancer(labelsPath, weightsPath, configPath, light_pos_file_path, metadata_file_path)

    person_pos = [{"x": 280, "y": 415}]
    intensities_lights_all_persons = ambiancer.fill_light_intensity(person_pos)
    ambiancer.compute_lights_intensity_per_person(intensities_lights_all_persons)
    lights = ambiancer.get_lights()
    frame = cv2.imread("../Object_dection_using_image/images/dining_table.jpg")

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

    assert 1==0

    print("print the intensities: end of test")
    print(intensities_lights_all_persons)