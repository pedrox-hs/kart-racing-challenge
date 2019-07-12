from datetime import timedelta
from functools import reduce


class Pilot:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other): 
        return self.code == other.code


class Lap:
    def __init__(self, pilot, lap, time, duration, avg_speed):
        self.pilot = pilot
        self.lap = lap
        self.time = time
        self.duration = duration
        self.avg_speed = avg_speed

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__


class PilotLaps:
    def __init__(self, pilot, *laps):
        self.pilot = pilot
        self.qty_laps = len(laps)
        self.laps = laps
        self.total_time = reduce(
            lambda acc, c: c.duration + acc, laps, timedelta())

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
