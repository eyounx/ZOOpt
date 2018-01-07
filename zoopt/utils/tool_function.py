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
    def list_compare(list1, list2):
        """
        Compare two lists.

        :return: True if the two lists are the same else False.
        """
        if len(list1) != len(list2):
            return False
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return False
        return True

    @staticmethod
    def deepcopy(obj):
        """
        Deep copy an object.

        :param obj: an object
        :return: a new object
        """
        return pickle.loads(pickle.dumps(obj))

    @staticmethod
    def log(text):
        """
        Output logs in ZOOpt.

        :param text: the text content
        :return: no return value
        """
        print('[zoopt] '+text)
