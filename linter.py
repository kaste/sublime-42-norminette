#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Baptiste JAMIN
# Copyright (c) 2016 Baptiste JAMIN
#
# License: MIT
#

"""This module exports the 42Norminette plugin class."""

import shlex
from SublimeLinter.lint import Linter, persist, util
import sublime
import os
import string

class Norminette(Linter):
    """Provides an interface to norminette."""

    executable = 'norminette'

    regex = r'''(?xi)
        ^^(?:(?P<error>Error)|(?P<warning>Warning))   # Error
        # Norminette emits errors that pertain to the code as a whole,
        # in which case there is no line/col information, so that
        # part is optional.
        (?:(.+?(?P<line>\d+)))?
        (?:(.+?(?P<col>\d+)))?
        (?:\)\:\s*)?
        (?:(?P<message>.+))
    '''
    
    line_col_base = (1, 0)
    multiline = True
    error_stream = util.STREAM_BOTH
    defaults = {
        'selector': 'source.c'
    }

    def split_match(self, match):

        match, line, col, error, warning, message, near = super().split_match(match)

        if col > 0:
            col -= 1
            point = self.view.text_point(line, 0)
            content = self.view.substr(self.view.line(point))
            c = 0
            while c < col and c < len(content):
                if content[c] == '\t':
                    col -= 3
                c += 1

        if line is None and message:
            line = 0
            col = 0

        return match, line, col, error, warning, message, near

    def cmd(self):
        result = self.executable
        return result + ' ' + sublime.active_window().active_view().file_name()

