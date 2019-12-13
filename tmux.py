#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import libtmux
import os
import subprocess

TMUX_WINDOW_BASENAME = "🍅"


class TmuxHandler:
    def __init__(self):
        self._pane_id = self._find_this_pane()
        self._window_id = self._find_this_window()
        self._original_name = self.window_name
        self.rename_window(TMUX_WINDOW_BASENAME)

    def _find_this_window(self):
        """Find the ID of the Tmux window running this gepom process."""
        #TODO: Make this method not rely on libtmux.
        assert hasattr(self, '_pane_id'), 'Must find pane ID before window ID'
        server = libtmux.Server()
        window_id = ''
        for session in server.list_sessions():
            for window in session.list_windows():
                if window.get_by_id(self._pane_id):
                    window_id = window.id
                    break
        assert window_id, 'Failed to find window ID'
        return window_id

    def _find_this_pane(self):
        """
        Find the ID of the Tmux pane running this gepom process.

        Stolen from https://jacob-walker.com/blog/...
        taming-tmux-find-one-process-among-many-windows.html

        """
        pid = os.getpid()
        argv = ['tmux', 'run-shell',
                'echo $(ps eww %s | sed "1d; s/^.*TMUX_PANE=//;s/ .*//")' % pid]
        pane_id = subprocess.check_output(argv).strip().decode()
        assert pane_id, 'Failed to find pane ID'
        return pane_id

    @property
    def window_name(self):
        assert hasattr(self, '_pane_id'), \
                'Must find pane ID before getting window name'
        argv = ['tmux', 'display-message', '-t', self._pane_id, '-p', "#W"]
        return subprocess.check_output(argv).strip()

    def rename_window(self, new_name):
        assert hasattr(self, '_window_id'), \
                'Must find window ID before renaming window'
        assert self._window_id is not None, 'window ID cannot be None'
        subprocess.call(['tmux', 'rename-window', '-t', self._window_id,
            new_name])

    def rename_window_with_message(self, message):
        new_name = '%s {%s}' % (TMUX_WINDOW_BASENAME, message)
        self.rename_window(new_name)

    def restore_original_name(self):
        self.rename_window(self._original_name)
