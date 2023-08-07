# To make python 2 and python 3 compatible code
from __future__ import absolute_import
from abc import ABC, abstractmethod
from IDetectorImpl import *


# create class interface
class IDetector(IDetectorImpl, ABC):

    @abstractmethod
    def detect_person(self, frame):
        pass