class ToolFunction:
    def __init__(self):
        pass

    @staticmethod
    def list_compare(list1, list2):
        if len(list1) != len(list2):
            return False
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                return False
        return True
