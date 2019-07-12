import sys
import unittest

from py3.src.read_log import get_log_content, parse_laps, group_laps_by_pilot, print_pilot_laps, Pilot, Lap, PilotLaps

from datetime import timedelta, datetime
from tempfile import NamedTemporaryFile
from unittest.mock import Mock, patch


class TestSuit(unittest.TestCase):
    def test_get_log_content_from_argv(self):
        with NamedTemporaryFile() as tf:
            tf.write(b"line 0\nline 1\t\n\tline 2\nline 3")
            tf.flush()
            testargs = ["script", tf.name]
            with patch.object(sys, 'argv', testargs):
                content = get_log_content()
                self.assertEqual(content[0], "line 0")
                self.assertEqual(content[1], "line 1")
                self.assertEqual(content[2], "line 2")
                self.assertEqual(content[3], "line 3")

    def test_get_log_content_from_stdin(self):
        readlines = Mock(
            return_value=["line 0", "line 1\t", "\tline 2", "line 3"])
        isatty = Mock(return_value=False)
        stdin = Mock(isatty=isatty, readlines=readlines)
        with patch.object(sys, 'stdin', stdin):
            content = get_log_content()
            self.assertEqual(content[0], "line 0")
            self.assertEqual(content[1], "line 1")
            self.assertEqual(content[2], "line 2")
            self.assertEqual(content[3], "line 3")

    @unittest.expectedFailure
    def test_get_log_content_without_input(self):
        isatty = Mock(return_value=True)
        stdin = Mock(isatty=isatty)
        with patch.object(sys, 'stdin', stdin):
            get_log_content()

    def test_parse_laps(self):
        lines = [
            "23:49:08.277 038 – F.MASSA 1 1:02.852 44,275",
            "23:49:10.858 033 – R.BARRICHELLO 2 1:04.352 43,243"
        ]
        laps = parse_laps(lines)
        self.assertEqual(len(laps), 2)
        self.assertIsInstance(laps[0], Lap)
        self.assertEqual(laps[0], Lap(
            Pilot('038', 'F.MASSA'), 1, datetime(1900, 1, 1, 23, 49, 8, 277000), timedelta(
                minutes=1, seconds=2, milliseconds=852), 44.275
        ))
        self.assertIsInstance(laps[1], Lap)
        self.assertEqual(laps[1], Lap(Pilot('033', 'R.BARRICHELLO'), 2, datetime(
            1900, 1, 1, 23, 49, 10, 858000), timedelta(minutes=1, seconds=4, milliseconds=352), 43.243))

    def test_parse_laps_skip_one(self):
        lines = [
            "23:49:08.277 038 – F.MASSA 1 1:02.852 44,275",
            "23:49:10.858 033 – R.BARRICHELLO 2 1:04.352 43,243"
        ]
        laps = parse_laps(lines, 1)
        self.assertEqual(len(laps), 1)
        self.assertIsInstance(laps[0], Lap)
        self.assertEqual(laps[0], Lap(Pilot('033', 'R.BARRICHELLO'), 2, datetime(
            1900, 1, 1, 23, 49, 10, 858000), timedelta(minutes=1, seconds=4, milliseconds=352), 43.243))

    @unittest.expectedFailure
    def test_parse_laps_wrong_pattern(self):
        lines = [
            "23:49:08 038 – F.MASSA 1 1:02.852 44,275",
        ]
        parse_laps(lines)

    def test_group_laps_by_pilot(self):
        all_laps = [
            Lap(Pilot('038', 'F.MASSA'), 1, datetime(
                1900, 1, 1), timedelta(), 0.0),
            Lap(Pilot('033', 'R.BARRICHELLO'), 1,
                datetime(1900, 1, 1), timedelta(), 0.0),
            Lap(Pilot('038', 'F.MASSA'), 2, datetime(
                1900, 1, 1), timedelta(), 0.0),
            Lap(Pilot('002', 'K.RAIKKONEN'), 1,
                datetime(1900, 1, 1), timedelta(), 0.0),
        ]
        result = group_laps_by_pilot(all_laps)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], PilotLaps)
        self.assertEqual(result[0].pilot, Pilot('002', 'K.RAIKKONEN'))
        self.assertIsInstance(result[1], PilotLaps)
        self.assertEqual(result[1].pilot, Pilot('033', 'R.BARRICHELLO'))
        self.assertIsInstance(result[2], PilotLaps)
        self.assertEqual(result[2].pilot, Pilot('038', 'F.MASSA'))

    def test_print_pilot_laps(self):
        write = Mock(return_value=lambda d: d.strip())
        stdout = Mock(write=write)
        with patch.object(sys, 'stdout', stdout):
            all_pilot_laps = [
                PilotLaps(Pilot('002', 'K.RAIKKONEN'), *[
                    Lap(None, 1, datetime(1900, 1, 1), timedelta(milliseconds=678), 0.0),
                    Lap(None, 1, datetime(1900, 1, 1), timedelta(milliseconds=890), 0.0),
                ]),
                PilotLaps(Pilot('023', 'M.WEBBER'), *[
                    Lap(None, 1, datetime(1900, 1, 1), timedelta(milliseconds=987), 0.0),
                ]),
                PilotLaps(Pilot('038', 'F.MASSA'), *[
                    Lap(None, 1, datetime(1900, 1, 1), timedelta(milliseconds=789), 0.0),
                    Lap(None, 1, datetime(1900, 1, 1), timedelta(milliseconds=567), 0.0),
                ]),
            ]
            print_pilot_laps(all_pilot_laps)
        self.assertEqual(write.call_count, 8)
        call_args_list = [z.strip() for z in [[y for y in x][0][0]
                                              for x in write.call_args_list] if z != "\n"][1:]
        self.assertEqual(len(call_args_list), 3)
        self.assertRegex(
            call_args_list[0], '^1\\s+038\\s+F\\.MASSA\\s+2\\s+0:01\\.356$')
        self.assertRegex(
            call_args_list[1], '^2\\s+002\\s+K\\.RAIKKONEN\\s+2\\s+0:01\\.568$')
        self.assertRegex(
            call_args_list[2], '^3\\s+023\\s+M\\.WEBBER\\s+1\\s+0:00\\.987$')


if __name__ == "__main__":
    unittest.main(verbosity=2)
