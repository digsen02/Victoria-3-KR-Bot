from datetime import datetime
from abc import *


class Timestamp(metaclass=ABCMeta):
    def timetamp(self):
        print("test")
