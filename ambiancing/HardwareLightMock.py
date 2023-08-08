from __future__ import absolute_import

from Utils import *


# create class interface
class HardwareLightMock():

    # TODO: use @classmethod to have different init of class
    def __init__(self, ip=None):
        self.max_brightness = 100
        self.ip = ip

    def shut_on(self):
        print('hardware light mock turn on')

    def shut_off(self):
        print('hardware light mock turn off')

    def set_brightness(self, brightness_ratio):
        print('hardware light mock set brightness')

    @staticmethod
    def discover_lights_ssid(load_from_file=True):
        print('hardware light mock discover sids')
