import math


class ActivationFunction:
    @staticmethod
    def sigmoid(x):
        for i in range(len(x)):
            if -700 <= x[i] <= 700:
                x[i] = (2 / (1 + math.exp(-x[i]))) - 1  # sigmoid function
            else:
                if x[i] < -700:
                    x[i] = -1
                else:
                    x[i] = 1
        return x
