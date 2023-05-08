from __future__ import absolute_import


# create class interface
class Light():

    def __init__(self, id, pin = 0):
        self.intensity = None
        self.pos = {"x": 0, "y": 0}
        self.id = id
        self.raspi_pin = pin
        self.light_on = False

    def udpate_intensity(self, intensity):
        self.intensity = intensity

    def set_position(self, x, y):
        self.pos["x"] = x
        self.pos["y"] = y

    def shut_on(self):
        print("shut on")
        self.light_on = True

    def shut_off(self):
        print("shut off")
        self.light_on = False

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