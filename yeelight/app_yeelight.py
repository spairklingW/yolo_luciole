import argparse
import os
from yeelight import *

print("going to print the bulbs infos")
bulbs = discover_bulbs()
print(bulbs)

bulb = Bulb("192.168.0.182")
bulb.turn_on()
bulb.set_brightness(50)