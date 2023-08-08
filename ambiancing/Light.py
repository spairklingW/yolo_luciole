from __future__ import absolute_import
import os
import sys
from pathlib import Path
sys.path.append(str(Path(os.path.dirname(os.path.abspath(__file__))).parent))
from ambiancing.Yeelight import *
from ambiancing.HardwareLightMock import *


# create class interface
class Light():

    def __init__(self, id=None, x=0, y=0, ssid=0, light_brand="yeelight"):
        self.intensity = None
        self.pos = {"x": x, "y": y}
        self.id = id
        self.raspi_pin = ssid
        self.light_on = False
        # ssid can be the ip or pin
        self.light_hardware = self.__init_hardware_light(light_brand, ssid)

    def __init_hardware_light(self, light_brand, ssid):
        if light_brand == "yeelight":
            print("into the init hardware for yeelight")
            return Yeelight(ssid)
        elif light_brand == "light_mock":
            print("into the init hardware with mock")
            return HardwareLightMock()
        else:
            print("Error: no light initialized")

    @staticmethod
    def discover_lights_ssid():
        return Yeelight().discover_lights_ssid()

    def udpate_intensity(self, intensity):
        self.intensity = intensity

    def power_intensity(self):
        self.light_hardware.set_brightness(self.intensity)

    def set_position(self, x, y):
        self.pos["x"] = x
        self.pos["y"] = y

    def show_position(self):
        print("pos light x")
        print(self.pos["x"])
        print("pos light y")
        print(self.pos["y"])

    def show(self):
        print("pos light x")
        print(self.pos["x"])
        print("pos light y")
        print(self.pos["y"])
        print("id")
        print(self.id)
        print("intensity")
        print(self.intensity)
        print("id: raspi pin or ip address")
        print(self.raspi_pin)

    def shut_on(self):
        print("shut on")
        self.light_on = True
        self.light_hardware.shut_on()

    def shut_off(self):
        print("shut off")
        self.light_on = False
        self.light_hardware.shut_off()

    def get_position(self):
        return self.pos

    def get_id(self):
        return self.id

    def get_raspi_pin(self):
        return self.raspi_pin

    def get_intensity(self):
        return self.intensity

    def is_light_on(self):
        return self.light_on

    def __exit__(self, exception_type, exception_value, traceback):
        print("quite yolo detector")
