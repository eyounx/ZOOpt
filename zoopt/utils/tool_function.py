"""
This module contains the class ToolFunction.

Author:
    Yu-Ren Liu, Yang Yu
"""

import pickle


class ToolFunction:
    """
    Class ToolFunction defines some tool function used in project.
    """
    def __init__(self):
        pass

    @staticmethod
    def list_compare(list1, list2):
        """
        Compare two lists. If lists are same, return True.

        :return: True or False
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

        :param obj: object
        :return: a new object
        """
        return pickle.loads(pickle.dumps(obj));

    @staticmethod
    def log(text):
        """
        Log output in ZOOpt.

        :param text: text to output
        :return: no return
        """
        print('[zoopt] '+text)
