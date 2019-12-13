#!/usr/bin/env python3

import unittest

import tracker

class MockStdscr(object):
    def clear(self):
        pass
    def getch(self):
        return 10
    def addstr(self, x, y, msg, attrs=[]):
        pass
    def refresh(self):
        pass


class MockTmux(object):
    def rename_window_with_message(self, msg):
        pass
    def restore_original_name(self):
        pass

tracker.tmux.TmuxHandler = MockTmux


class MockTimer(object):
    def __init__(self, tracker, duration):
        pass
    def die(self):
        pass

tracker.timer.PomodoroTimer = MockTimer


class TestTrackerMethods(unittest.TestCase):
    def setUp(self):
        stdscr = MockStdscr()
        self.t = tracker.PomodoroTracker(stdscr)

    def test_working_sessions_completed(self):
        self.assertEqual(self.t._working_sessions_completed, 0)
        self.t._complete_session()
        self.assertEqual(self.t._working_sessions_completed, 1)
        self.t._complete_session()
        self.assertEqual(self.t._working_sessions_completed, 1)
        self.t._complete_session()
        self.assertEqual(self.t._working_sessions_completed, 2)


if __name__ == '__main__':
    unittest.main()
