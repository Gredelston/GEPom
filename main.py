#!/usr/bin/env python3
import curses

import tracker


def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, 'Hello, curses!')

    t = tracker.PomodoroTracker(stdscr)
    t.start_timer(5)
    while t._working_sessions_completed == 0:
        pass

    stdscr.refresh()
    stdscr.getkey()
    t.tmux.restore_original_name()


if __name__ == '__main__':
    curses.wrapper(main)
