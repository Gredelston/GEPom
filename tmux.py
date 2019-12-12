#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import subprocess

TMUX_WINDOW_BASENAME = "🍅"


class TmuxHandler:
    def __init__(self):
        self._original_name = self.window_name
        self.restore_basename()

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
