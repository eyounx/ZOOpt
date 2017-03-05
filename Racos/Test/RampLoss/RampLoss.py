from Racos.Component.Dimension import Dimension
from Racos.Component.Objective import Objective
from Racos.Component.Parameter import Parameter
from Racos.Method.RacosOptimization import RacosOptimization


class RampLoss:
    def __init__(self):
        self.dim = Dimension() # Dimension
        self.data = []  # training or testing data, include label
        self.c = 1  # hyper-parameter
        self.s = 0  # hyper-parameter
        self.dim_size = 0   # Dimension size
        self.read_data('ionosphere.data.txt')

    # Read data from file "ionosphere.data.txt"
    def read_data(self, filename):
        input = open(filename)
        list_lines = input.readlines()
        mydata = []
        for i in range(len(list_lines)):
            temp_list = list_lines[i].split(',')
            mydata.append([])
            list_len = len(temp_list)
            temp_list[list_len - 1] = temp_list[list_len - 1][: -1]
            for j in range(list_len):
                if j == list_len - 1:
                    if temp_list[j] == 'g':
                        mydata[i].append(1)
                    else:
                        mydata[i].append(-1)
                else:
                    mydata[i].append(float(temp_list[j]))
        self.data = mydata
        return

    # Compute f(x)
    def get_fx(self, weight, j):
        temp_sum = 0
        for i in range(len(weight) - 1):
            temp_sum += weight[i] * self.data[j][i]
        temp_sum += weight[len(weight) - 1]
        return temp_sum

    # Compute hinge loss
    def get_h(self, ylfx, st):
        temp = st - ylfx
        if temp > 0:
            return temp
        else:
            return 0

    # Compute distance
    def get_distance(self, weight):
        temp_sum = 0
        for i in range(len(weight)):
            temp_sum += weight[i] * weight[i]
        return temp_sum

    # Main function to compute ramploss
    def get_value(self, weight):
        H1 = 0
        Hs = 0
        for i in range(len(self.data)):
            fx = self.get_fx(weight, i)
            H1 += self.get_h(self.data[i][len(self.data[0]) - 1] * fx, 1)
            Hs += self.get_h(self.data[i][len(self.data[0]) - 1] * fx, self.s)
        dis = self.get_distance(weight)
        value = dis / 2 + self.c * H1  - self.c * Hs
        return value

    # Validation function
    def validation(self, best):
        right = 1.0
        for i in range(len(self.data)):
            temp_sum = 0
            length = len(self.data[0])
            for j in range(length - 1):
                temp_sum += best[j] * self.data[i][j]
            temp_sum += best[length - 1]
            if temp_sum > 0:
                label = 1
            else:
                label = -1
            # error
            if label == self.data[i][length - 1]:
                right += 1
        rate = right / len(self.data)
        return rate

    def run(self):
        repeat = 1
        result = []
        for i in range(repeat):
            # dim means [weight, bias]
            dim_size = 35
            dim_regs = []
            dim_tys = []
            for j in range(dim_size):
                dim_regs.append([-10, 10])
                dim_tys.append(True)
            dim = Dimension(dim_size, dim_regs, dim_tys)
            objective = Objective(self.get_value, dim)
            budget = 20 * dim_size
            parameter = Parameter(objective, budget)
            racos = RacosOptimization()
            print 'Best solution is:'
            ins = racos.opt(parameter, strategy='WR')
            ins.print_instance()
            print self.validation(ins.get_coordinates())
        return

test = RampLoss()
test.run()