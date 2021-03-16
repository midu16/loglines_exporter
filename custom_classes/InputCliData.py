"""
 This following class is returning a object with the path for the logs and port of the server.
"""
from custom_classes import CountLogfileLines

class InputData(object):
    def __init__(self, *args):
        file = CountLogfileLines.LogFileLinesLister(*args)
        nolines = file.no_of_lines
        self.lines = nolines


