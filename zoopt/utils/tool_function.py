"""
This module contains the class ToolFunction.

Author:
    Yu-Ren Liu, Yang Yu
"""

import pickle


class ToolFunction:
    """
    This class defines some tool functions used in the project.
    """
    def __init__(self):
        pass

    @staticmethod
    def log(text):
        """
        Output logs in ZOOpt.

        :param text: the text content
        :return: no return value
        """
        print('[zoopt] '+text)
