#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import subprocess
import sys

TMUX_WINDOW_BASENAME = "🍅"


class TmuxHandler:
    def __init__(self):
        self._original_name = self.window_name
        subprocess.call(['tmux', 'rename-window', TMUX_WINDOW_BASENAME])
        print(self._find_this_pane_id())
        self.restore_basename()

    def _find_this_pane_id(self):
        """https://jacob-walker.com/blog/taming-tmux-find-one-process-among-many-windows.html"""
        pid = os.getpid()
        argv = ['tmux', 'run-shell',
                'echo $(ps eww %s | sed "1d; s/^.*TMUX_PANE=//;s/ .*//")' % pid]
        return subprocess.check_output(argv).strip()

    @property
    def window_name(self):
        argv = ['tmux', 'display-message', '-p', "#W"]
        return subprocess.check_output(argv).strip()

    def rename_window(self, new_name):
        subprocess.call(['tmux', 'rename-window', new_name])

    def restore_basename(self):
        self.rename_window(TMUX_WINDOW_BASENAME)

    def rename_window_with_message(self, message):
        new_name = '%s {%s}' % (TMUX_WINDOW_BASENAME, message)
        self.rename_window(new_name)

    def restore_original_name(self):
        self.rename_window(self._original_name)
