# To make python 2 and python 3 compatible code
from __future__ import absolute_import
from abc import ABC, abstractmethod
from ILightInitializerImpl import *


# create class interface
class ILightInitializer(ILightInitializerImpl, ABC):

    @abstractmethod
    def detect_lights(self):
        pass

    @abstractmethod
    def set_light_on(self):
        pass

    @abstractmethod
    def set_light_off(self):
        pass

    def detect_lights_position(self):
        self._detect_lights_position_impl()

    def print_light_position(self):
        self._print_light_position_impl()

    def get_lights_position_as_list(self):
        return self._get_lights_position_as_list_impl()