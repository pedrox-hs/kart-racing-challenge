#!/usr/bin/env python3

import re
import sys

from datetime import datetime, timedelta
from itertools import groupby
from os import path

from py3.src.lib.models import Pilot, Lap, PilotLaps
from py3.src.lib.exceptions import IncorrectUsageException, InvalidFormatException


def main():
    try:
        log_data = get_log_content()
        laps = parse_laps(log_data, 1)
        pilot_laps = group_laps_by_pilot(laps)
        print_pilot_laps(pilot_laps)
    except IncorrectUsageException as e:
        print(e)


def get_log_content():
    lines = []
    if len(sys.argv) > 1 and path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as f:
            lines = f.readlines()
    elif not sys.stdin.isatty():
        lines = sys.stdin.readlines()
    else:
        script_path = sys.argv[0]
        raise IncorrectUsageException(
            "Usage:\n\n  Using arguments:\n    python3 %s [log_path]\n\n  Using STDIN:\n    cat [log_path] | python3 %s" % (script_path, script_path))
    content = [x.strip() for x in lines]
    return content


def parse_laps(raw_data, skip=0):
    laps = []
    pattern = '^(\\d{2}:\\d{2}:\\d{2}\\.\\d{3})\\s+(\\d+?)\\s+–\\s+(.+?)\\s+(\\d+?)\\s+(\\d+:\\d{2}\\.\\d{,3})\\s+(\\d+,\\d+)$'
    pattern = re.compile(pattern)
    for d in raw_data[skip:]:
        if not pattern.match(d):
            raise InvalidFormatException("%s not match %s" % (d, pattern.pattern))
        time, pilot_id, pilot_name, number, duration, speed = pattern.findall(d)[0]
        pilot = Pilot(pilot_id, pilot_name)
        lap = Lap(pilot, int(number), parse_time(time),
                  parse_duration(duration), parse_speed(speed))
        laps.append(lap)
    return laps


def parse_time(raw_time):
    time = raw_time.ljust(15, '0')
    time = datetime.strptime(time, '%H:%M:%S.%f')
    return time


def parse_duration(raw_duration):
    pattern = re.compile('^(\\d+):(\\d{2})\\.(\\d+)$')
    if not pattern.match(raw_duration):
        raise InvalidFormatException("%s not match %s" % (raw_duration, pattern.pattern))
    minutes, seconds, milliseconds = pattern.findall(raw_duration)[0]
    return timedelta(minutes=int(minutes), seconds=int(seconds), milliseconds=int(milliseconds))


def parse_speed(speed):
    return float(speed.replace(',', '.'))


def group_laps_by_pilot(all_laps):
    laps = sort_laps(all_laps)
    grouped = groupby(laps, key=lambda l: l.pilot)
    return [PilotLaps(k, *list(v)) for k, v in grouped]


def print_pilot_laps(all_pilot_laps):
    formatter = "{:<15} {:<13} {:<20} {:<23} {:<20}"
    header = ('Posição Chegada', 'Código Piloto', 'Nome Piloto',
              'Qtde Voltas Completadas', 'Tempo Total de Prova')
    print(formatter.format(*header))
    pilot_laps = sort_pilot_laps(all_pilot_laps)
    for p, pilot_lap in enumerate(pilot_laps):
        line = (p + 1, pilot_lap.pilot.code, pilot_lap.pilot.name,
                pilot_lap.qty_laps, format_duration(pilot_lap.total_time))
        print(formatter.format(*line))


def sort_laps(laps):
    return sorted(laps, key=lambda l: (l.pilot.code, l.lap))


def sort_pilot_laps(pilot_laps):
    return sorted(pilot_laps, key=lambda l: (-l.qty_laps, l.total_time))


def format_duration(duration):
    return "{:2}:{:02}.{:03}".format(
        duration.seconds // 60,
        duration.seconds % 60,
        duration.microseconds // 1000
    )


if __name__ == '__main__':
    main()
