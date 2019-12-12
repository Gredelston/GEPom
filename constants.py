#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import enum

TMUX_WINDOW_BASENAME = "🍅"

class SessionType(enum.Enum):
    """The three session types defined in Pomodoro."""
    WORKING_SESSION = 1
    SHORT_BREAK = 2
    LONG_BREAK = 3


# Length of each SessionType, in seconds
SESSION_LENGTHS = {SessionType.WORKING_SESSION: 25*60,
        SessionType.SHORT_BREAK: 5*60,
        SessionType.LONG_BREAK: 15*60}
