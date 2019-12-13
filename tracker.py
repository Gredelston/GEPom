#!/usr/bin/env python3
import curses
import enum
import sys

import timer
import tmux

class SessionType(enum.Enum):
    """The three session types defined in Pomodoro."""
    WORKING_SESSION = 1
    SHORT_BREAK = 2
    LONG_BREAK = 3


SESSION_LENGTHS = {SessionType.WORKING_SESSION: 25*60,
        SessionType.SHORT_BREAK: 5*60,
        SessionType.LONG_BREAK: 15*60}

SESSION_TITLES = {SessionType.WORKING_SESSION: 'Working Session',
        SessionType.SHORT_BREAK: 'Short Break',
        SessionType.LONG_BREAK: 'Long Break'}


class PomodoroTracker():
    """Class to keep track of active and historical Pomodoro state."""
    def __init__(self, stdscr, override_first_session_duration=False):
        self._QUIT = False
        self._stdscr = stdscr
        self.tmux = tmux.TmuxHandler()
        self._timer = None
        self._paused = False
        self._total_sessions_completed = 0
        self._begin_next_session(override_first_session_duration)

    def _begin_next_session(self, override_duration=False):
        self._stdscr.clear()
        self.write(0, SESSION_TITLES[self._session_type()])
        session_type = self._session_type()
        if override_duration:
            duration = override_duration
        else:
            duration = SESSION_LENGTHS[session_type]
        self._start_timer(duration)

    def _session_type(self):
        """Determine the current session type (or upcoming, if between sessions)"""
        if self._total_sessions_completed % 2 == 0:
            return SessionType.WORKING_SESSION
        elif self._total_sessions_completed % 8 == 7:
            return SessionType.LONG_BREAK
        else:
            return SessionType.SHORT_BREAK
    
    def _start_timer(self, duration):
        assert self._timer is None, 'Cannot have multiple timers running'
        self._timer = timer.PomodoroTimer(self, duration)

    def _complete_session(self):
        self.write(3, 'Session is now complete.')
        self.tmux.rename_window_with_message('DONE')
        self._total_sessions_completed += 1
        self._timer.die()
        self._timer = None

        # Offer to advance to the next session or to quit
        self.write(4, 'Press q/x to exit, or ENTER to advance')
        while True:
            k = self._stdscr.getch()
            if k in (ord('q'), ord('x')):
                self.close()
                self._QUIT = True
                return
            elif k in (curses.KEY_ENTER, 10):
                self._begin_next_session()
                return

    @property
    def _working_sessions_completed(self):
        return (self._total_sessions_completed + 1) // 2
        

    def write(self, y, msg):
        self._stdscr.addstr(y, 0, str(msg))
        self._stdscr.refresh()

    def close(self):
        """Perform shutdown processes."""
        self.tmux.restore_original_name()
