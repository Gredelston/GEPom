#!/usr/bin/env python3
import curses
import enum


class SessionType(enum.Enum):
    """The three session types defined in Pomodoro."""
    WORKING_SESSION = 1
    SHORT_BREAK = 2
    LONG_BREAK = 3


# Length of each SessionType, in minutes
SESSION_LENGTHS = {SessionType.WORKING_SESSION: 25,
        SessionType.SHORT_BREAK: 5,
        SessionType.LONG_BREAK: 15}


class PomodoroTracker():
    """Class to keep track of active and historical Pomodoro state."""
    def __init__(self, first_session_type=SessionType.WORKING_SESSION):
        self._sessions_completed = 0
        self._session_type = first_session_type
        self._paused = False

    def _next_session(self):
        """Determine what kind of session should come next."""
        if self._session_type == SessionType.SHORT_BREAK:
            return SessionType.WORKING_SESSION
        elif self._session_type == SessionType.LONG_BREAK:
            return PomdoroSessionType.WORKING_SESSION
        elif session._session_type == SessionType.WORKING_SESSION:
            if self._sessions_completed % 4:
                return SessionType.SHORT_BREAK
            else:
                return SessionType.LONG_BREAK


def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, 'Hello, curses!')

    tracker = PomodoroTracker()

    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    curses.wrapper(main)
