#!/usr/bin/env python3
import curses
import enum
import sys
import threading
import time


class SessionType(enum.Enum):
    """The three session types defined in Pomodoro."""
    WORKING_SESSION = 1
    SHORT_BREAK = 2
    LONG_BREAK = 3


# Length of each SessionType, in seconds
SESSION_LENGTHS = {SessionType.WORKING_SESSION: 25*60,
        SessionType.SHORT_BREAK: 5*60,
        SessionType.LONG_BREAK: 15*60}


class PomodoroTimer:
    def __init__(self, tracker, interval):
        self._tracker = tracker
        self._timer = None
        self._time_remaining_at_last_pause = interval
        self._updater = None
        self.resume()

    @property
    def _is_running(self):
        return self._timer is not None

    @property
    def _elapsed(self):
        assert self._is_running, 'No time elapses when no timer is running'
        return time.time() - self._started_at

    @property
    def time_remaining(self):
        if self._is_running:
            return self._time_remaining_at_last_pause - self._elapsed
        else:
            return self._time_remaining_at_last_pause

    def resume(self):
        assert not self._is_running, 'Cannot resume when a timer is running'
        self._started_at = time.time()
        interval = self.time_remaining
        self._timer = threading.Timer(interval, self._tracker.complete_session)
        self._timer.start()
        self._create_updater()

    def pause(self):
        assert self._is_running, 'Cannot pause when no timer is running'
        self._timer.cancel()
        self._time_remaining_at_last_pause -= self._elapsed
        self._timer = None
        self._started_at = None

    def _create_updater(self):
        """Schedule a short timer to update the displays."""
        if self._updater is None:
            self._updater = threading.Timer(0.05, self._update)
            self._updater.start()

    def _update(self):
        """Update displays to show how much time is left."""
        self._updater = None
        self._tracker.write(2, self.time_remaining)
        if self._is_running:
            self._create_updater()

    def die(self):
        self._updater.cancel()
        self._timer.cancel()


class PomodoroTracker():
    """Class to keep track of active and historical Pomodoro state."""
    def __init__(self, stdscr, first_session_type=SessionType.WORKING_SESSION):
        self._stdscr = stdscr
        self._sessions_completed = 0
        self._session_type = first_session_type
        self._paused = False
        self._timer = None

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
    
    def start_timer(self, duration):
        assert self._timer is None, 'Cannot have multiple timers running'
        self._timer = PomodoroTimer(self, duration)

    def complete_session(self):
        self.write(3, 'Session is now complete.')
        self._sessions_completed += 1
        self._timer.die()
        self._timer = None
        sys.exit(0)

    def write(self, y, msg):
        self._stdscr.addstr(y, 0, str(msg))
        self._stdscr.refresh()


def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, 'Hello, curses!')

    tracker = PomodoroTracker(stdscr)
    tracker.start_timer(5)
    tracker.write(4, time.time())
    while tracker._sessions_completed == 0:
        pass
    tracker.write(5, time.time())

    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    curses.wrapper(main)
