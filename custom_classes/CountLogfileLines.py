"""
 This following class is returning a object with the number of lines of each files inputed.
"""
class LogFileLinesLister(object):
    def __init__(self, *args):
        index = 0
        with open(*args) as f:
            for line in f:
                index += 1
            self.no_of_lines = index
    @property
    def filename(self, *args):
        return str(*args)



