from datetime import datetime
from abc import *


class Timestamp(metaclass=ABCMeta):
    def timestamp(self):
        print("test")
