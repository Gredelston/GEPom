#!/usr/bin/env python3
import curses

import tracker


def main(stdscr):
    t = tracker.PomodoroTracker(stdscr)
    while not t._QUIT:
        pass

if __name__ == '__main__':
    curses.wrapper(main)
