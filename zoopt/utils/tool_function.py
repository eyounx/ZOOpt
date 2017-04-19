
import pickle

"""
class ToolFunction defines some tool function used in project.

Author:
    Yuren Liu, Yang Yu
"""


class ToolFunction:
    def __init__(self):
        pass

    # Compare two lists. If lists are same, return True.
    @staticmethod
    def list_compare(list1, list2):
        if len(list1) != len(list2):
            return False
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return False
        return True

    @staticmethod
    def deepcopy(obj):
        return pickle.loads(pickle.dumps(obj));

    @staticmethod
    def log(text):
        print('[zoopt] '+text)
