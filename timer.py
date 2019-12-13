#!/usr/bin/env python3
import threading
import time

class PomodoroTimer:
    def __init__(self, tracker, interval):
        self._tracker = tracker
        self._timer = None
        self._time_remaining_at_last_pause = interval
        self._last_timestamp_pushed = None
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
    
    @property
    def timestamp(self):
        seconds_remaining = int(self.time_remaining)
        minutes = str(int(seconds_remaining) // 60)
        seconds = str(int(seconds_remaining) % 60).zfill(2)
        return '%s:%s' % (minutes, seconds)

    def resume(self):
        assert not self._is_running, 'Cannot resume when a timer is running'
        self._started_at = time.time()
        interval = self.time_remaining
        self._timer = threading.Timer(interval, self._tracker._complete_session)
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
        timestamp = self.timestamp
        if timestamp != self._last_timestamp_pushed:
            self._tracker.write(2, timestamp)
            self._tracker.tmux.rename_window_with_message(timestamp)
            self._last_timestamp_pushed = timestamp
        if self._is_running:
            self._create_updater()

    def die(self):
        self._updater.cancel()
        self._timer.cancel()
