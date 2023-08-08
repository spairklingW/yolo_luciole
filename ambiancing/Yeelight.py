from __future__ import absolute_import
from yeelight import *

from Utils import *


# create class interface
class Yeelight():

    # TODO: use @classmethod to have different init of class
    def __init__(self, ip=None):
        self.max_brightness = 100
        self.ip = ip
        self.bulb = Bulb(ip)

    def shut_on(self):
        self.bulb.turn_on()

    def shut_off(self):
        self.bulb.turn_off()

    def set_brightness(self, brightness_ratio):
        print("SET BRIGHTNESSSSSS ###########################")
        print(int(brightness_ratio*self.max_brightness))
        self.bulb.set_brightness(int(brightness_ratio*self.max_brightness))

    @staticmethod
    def discover_lights_ssid(load_from_file=True):
        if load_from_file:
            return load_yaml("lights_ip.yaml")["lights_ip"]
        else:
            bulbs = discover_bulbs()
            return bulbs
