import argparse
from LightInitializerMockFromVideo import *
from LightInitializerMockFromImage import *
from LightInitializer import *
from ambiancing.Utils import *
from ambiancing.Config import *


def start(light_initializer, metadata_file_path, light_pos_file_path):
    light_initializer.detect_lights()
    light_initializer.detect_lights_position()
    lights_position = light_initializer.get_lights_rel_position_as_list()
    metadata = light_initializer.get_metadata()

    print("lights positions")
    print(lights_position)
    dump_yaml(lights_position, light_pos_file_path)
    dump_yaml(metadata, metadata_file_path)

    debug = True
    if debug:
        light_initializer.print_light_position()


def parse_args():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-k", "--mode", type=str, default="video",
                    help="choose between video, image, or camera")
    ap.add_argument("-a", "--hardware_brand", type=str, required=False, default="light_mock",
                    help="choose between video, image, or camera")
    ap.add_argument("-i", "--input", required=False,
                    help="path to input video")
    ap.add_argument("-o", "--output", required=False,
                        help="path to output video")
    ap.add_argument("-l", "--light_pos_file", required=True,
                    help="path to output video")
    ap.add_argument("-m", "--metadata", required=True,
                    help="metadata interface file path")
    ap.add_argument("-c", "--config_path", required=True,
                    help="config yaml path")
    ap.add_argument("-f",  "--verbose", type=str, choices=['true', 'false'], default='false')
    args = vars(ap.parse_args())

    return args


def main():
    start_time = time.time()
    args = parse_args()
    config = Config(load_yaml(args["config_path"]))
    light_pos_file_path = args["light_pos_file"]
    metadata_file_path = args["metadata"]
    input_file_path = args["input"]
    hardware_brand = args["hardware_brand"]
    output_file_path = args["output"]
    mode = args["mode"]
    verbose = args["verbose"].lower() == "true"
    light_initializer = None

    if mode == "video":
        light_initializer = LightInitializerMockFromVideo(input_file_path, output_file_path, config, verbose)
    elif mode == "image":
        light_initializer = LightInitializerMockFromImage(input_file_path, output_file_path, config, verbose)
    elif mode == "camera":
        #TODO abstract the brand of the light as param, yeelight vs cameramock
        light_initializer = LightInitializer(config, hardware_brand, verbose)

    start(light_initializer, metadata_file_path, light_pos_file_path)

    print("--- %s seconds ---" % (time.time() - start_time))

main()