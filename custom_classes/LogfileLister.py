import os
"""
    The following class is returning a object of files in a specific directory and the number of files.
"""
class DirectoryLister(object):
    def __init__(self, *args):
        self.directory = os.listdir(*args)

    @property
    def count(self):
        return len(self.directory)