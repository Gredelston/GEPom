#!/usr/bin/env python3
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


class PomodoroTracker():
    """Class to keep track of active and historical Pomodoro state."""
    def __init__(self, stdscr, first_session_type=SessionType.WORKING_SESSION):
        self._stdscr = stdscr
        self._working_sessions_completed = 0
        self._session_type = first_session_type
        self._paused = False
        self._timer = None
        self.tmux = tmux.TmuxHandler()

    def _next_session(self):
        """Determine what kind of session should come next."""
        if self._session_type == SessionType.SHORT_BREAK:
            return SessionType.WORKING_SESSION
        elif self._session_type == SessionType.LONG_BREAK:
            return PomdoroSessionType.WORKING_SESSION
        elif session._session_type == SessionType.WORKING_SESSION:
            if self._working_sessions_completed % 4:
                return SessionType.SHORT_BREAK
            else:
                return SessionType.LONG_BREAK
    
    def start_timer(self, duration):
        assert self._timer is None, 'Cannot have multiple timers running'
        self._timer = timer.PomodoroTimer(self, duration)

    def complete_session(self):
        self.write(3, 'Session is now complete.')
        self.tmux.rename_window_with_message('DONE')
        if self._session_type == SessionType.WORKING_SESSION:
            self._working_sessions_completed += 1
        self._timer.die()
        self._timer = None
        sys.exit(0)

    def write(self, y, msg):
        self._stdscr.addstr(y, 0, str(msg))
        self._stdscr.refresh()
