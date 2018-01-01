"""
This module contains the class Loader, which can load another module from its path.

Author:
    Yu-Ren Liu
"""

import traceback


class Loader(object):
    """
    This class can load a module from path.
    """

    def __init__(self):
        pass

    def load(self, path):
        """
        Load a module from path.

        :param path: path of the module
        :return: loaded module(succeed) or None(fail)
        """
        try:
            tmp = {}
            exec open(path).read() in tmp
            return tmp
        except:
            print("Load module [path %s] error: %s"
                  % (path, traceback.format_exc()))
            return None