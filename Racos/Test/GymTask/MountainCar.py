from NNModel import NN_Model
from GymTask import Gym_Task
from Components import Dimension
from Racos import RacosOptimizaiton
# import FileOperator as fo

# test function
def runTest():
    hidden_layer_num = [5]

    task_name = 'MountainCar-v0'

    max_step = 10000

    gym_task = Gym_Task(task_name)
    gym_task.newNN_Model(hidden_layer_num)
    gym_task.setMaxStep(max_step)

    SampleSize = 20  # the instance number of sampling in an iteration
    MaxIteration = 100  # the number of iterations
    Budget = 21  # budget in online style 2000
    PositiveNum = 2  # the set size of PosPop
    RandProbability = 0.95  # the probability of sample in model
    UncertainBits = 1  # the dimension size that is sampled randomly

    # set dimension
    dim = None
    dim = Dimension()
    dim.setDimensionSize(gym_task.getPareSize())
    regs = []
    regs.append(-10.0)
    regs.append(10.0)
    for i in range(dim.getSize()):
        dim.setRegion(i, regs, True)

    monitor_record = True

    print 'Online_mode RACOS ====================================================================='
    # run
    racos = None
    racos = RacosOptimizaiton(dim)

    # call online version RACOS
    racos.OnlineTurnOn()
    print 'Online-mode RACOS begin...'
    racos.ContinueOpt(gym_task.SumReward, SampleSize, Budget, PositiveNum, RandProbability, UncertainBits)
    print 'Online-mode RACOS end!'

    w = racos.getOptimal().getFeatures()
    w_v = racos.getOptimal().getFitness()

    test_repeat = 5
    gym_task.setMaxStep(1000)
    for e_i in range(test_repeat):
        print 'test num:', e_i, '----------------------------------------------------------'
        stop_step = gym_task.ShowResult(w, e_i, monitor_record)
        print 'stop step:', stop_step




# run experiment
def runExp():
    hidden_layer_num = []
    # hidden_layer_num.append([5, 3, 2])              # CartPole-v0
    hidden_layer_num.append([5])                    # MountainCar-v0
    # hidden_layer_num.append([5, 3])                 # Acrobot-v1

    task_name = []
    # task_name.append('CartPole-v0')
    task_name.append('MountainCar-v0')
    # task_name.append('Acrobot-v1')

    max_step = []
    # max_step.append(20000)                          # CartPole-v0  20000
    max_step.append(10000)                          # MountainCar-v0  10000
    # max_step.append(2000)                           # Acrobot-v1  2000

    run_repeat = 15
    test_repeat = 10

    SampleSize = 20            # the instance number of sampling in an iteration
    MaxIteration = 100         # the number of iterations
    Budget = 2000            # budget in online style 2000
    PositiveNum = 2            # the set size of PosPop
    RandProbability = 0.95     # the probability of sample in model
    UncertainBits = 1          # the dimension size that is sampled randomly

    monitor_record = False

    for t_i in range(len(task_name)):

        gym_task = Gym_Task(task_name[t_i])
        gym_task.newNN_Model(hidden_layer_num[t_i])
        gym_task.setMaxStep(max_step[t_i])

        # set dimension
        dim = None
        dim = Dimension()
        dim.setDimensionSize(gym_task.getPareSize())
        regs = []
        regs.append(-10.0)
        regs.append(10.0)
        for i in range(dim.getSize()):
            dim.setRegion(i, regs, True)

        # OLRACOS
        if True:
            print 'task name:', task_name[t_i]
            print 'max stop step:', max_step[t_i]
            print 'dimension size:', dim.getSize()
            print 'hidden layer:', hidden_layer_num[t_i]
            print 'budget:', Budget
            record = []
            record.append('task name:' + task_name[t_i])
            record.append('max stop step:' + str(max_step[t_i]))
            record.append('dimension size:' + str(dim.getSize()))
            record.append('hidden layer:' + List2String(hidden_layer_num[t_i]))
            record.append('budget:' + str(Budget))
            record.append('method: Online-mode RACOS')
            # online racos---------------------------------------------------------------------------------------------
            for r_i in range(run_repeat):
                print 'Online_mode RACOS ', r_i, '====================================================================='
                record.append('run num:' + str(r_i) + '================================================================')
                # run
                racos = None
                racos = RacosOptimizaiton(dim)

                # call online version RACOS
                racos.OnlineTurnOn()
                print 'Online-mode RACOS begin...'
                racos.ContinueOpt(gym_task.SumReward, SampleSize, Budget, PositiveNum, RandProbability, UncertainBits)
                print 'Online-mode RACOS end!'

                w = racos.getOptimal().getFeatures()
                w_v = racos.getOptimal().getFitness()

                record.append('x:' + List2String(w))
                record.append('fitness:' + str(w_v))

                for e_i in range(test_repeat):
                    print 'test num:', e_i, '----------------------------------------------------------'
                    record.append('test num:' + str(e_i) + '------------------------------------------------------')
                    stop_step = gym_task.ShowResult(w, e_i, monitor_record)
                    print 'stop step:', stop_step
                    record.append('stop step:' + str(stop_step))
            file_name = task_name[t_i] + '_olracos' + '_results.txt'
            fo.FileWriter(file_name, record)
            # online racos end-----------------------------------------------------------------------------------------

        # RACOS
        if True:
            print 'task name:', task_name[t_i]
            print 'max stop step:', max_step[t_i]
            print 'dimension size:', dim.getSize()
            print 'hidden layer:', hidden_layer_num[t_i]
            print 'budget:', Budget
            record = []
            record.append('task name:' + task_name[t_i])
            record.append('max stop step:' + str(max_step[t_i]))
            record.append('dimension size:' + str(dim.getSize()))
            record.append('hidden layer:' + List2String(hidden_layer_num[t_i]))
            record.append('budget:' + str(Budget))
            record.append('method: Batch-mode RACOS')
            # online racos---------------------------------------------------------------------------------------------
            for r_i in range(run_repeat):
                print 'Batch_mode RACOS ', r_i, '====================================================================='
                record.append('run num:' + str(r_i) + '================================================================')
                # run
                racos = None
                racos = RacosOptimizaiton(dim)

                # call online version RACOS
                # racos.OnlineTurnOn()
                print 'Batch-mode RACOS begin...'
                racos.ContinueOpt(gym_task.SumReward, SampleSize, MaxIteration, PositiveNum, RandProbability, UncertainBits)
                print 'Batch-mode RACOS end!'

                w = racos.getOptimal().getFeatures()
                w_v = racos.getOptimal().getFitness()

                record.append('x:' + List2String(w))
                record.append('fitness:' + str(w_v))

                for e_i in range(test_repeat):
                    print 'test num:', e_i, '----------------------------------------------------------'
                    record.append('test num:' + str(e_i) + '------------------------------------------------------')
                    stop_step = gym_task.ShowResult(w, e_i, monitor_record)
                    print 'stop step:', stop_step
                    record.append('stop step:' + str(stop_step))
            file_name = task_name[t_i] + '_racos' + '_results.txt'
            fo.FileWriter(file_name, record)
            # online racos end-----------------------------------------------------------------------------------------

        # CMAES
        if True:
            print 'task name:', task_name[t_i]
            print 'max stop step:', max_step[t_i]
            print 'dimension size:', dim.getSize()
            print 'hidden layer:', hidden_layer_num[t_i]
            print 'budget:', Budget
            record = []
            record.append('task name:' + task_name[t_i])
            record.append('max stop step:' + str(max_step[t_i]))
            record.append('dimension size:' + str(dim.getSize()))
            record.append('hidden layer:' + List2String(hidden_layer_num[t_i]))
            record.append('budget:' + str(Budget))
            record.append('method: CMA-ES')
            # CMAES----------------------------------------------------------------------------------------------------
            for r_i in range(run_repeat):
                print 'CMAES ', r_i, '====================================================================='
                record.append('run num:' + str(r_i) + '================================================================')
                # run
                w, w_v = runCMAES(dim, Budget, gym_task.SumReward)

                record.append('x:' + List2String(w))
                record.append('fitness:' + str(w_v))

                for e_i in range(test_repeat):
                    print 'test num:', e_i, '-------------------------------------------------------------'
                    record.append('test num:' + str(e_i) + '------------------------------------------------------')
                    stop_step = gym_task.ShowResult(w, e_i, monitor_record)
                    print 'stop step:', stop_step
                    record.append('stop step:' + str(stop_step))
            file_name = task_name[t_i] + '_cmaes' + '_results.txt'
            fo.FileWriter(file_name, record)
            # CMAES end------------------------------------------------------------------------------------------------

        # PSO
        if True:
            print 'task name:', task_name[t_i]
            print 'max stop step:', max_step[t_i]
            print 'dimension size:', dim.getSize()
            print 'hidden layer:', hidden_layer_num[t_i]
            print 'budget:', Budget
            record = []
            record.append('task name:' + task_name[t_i])
            record.append('max stop step:' + str(max_step[t_i]))
            record.append('dimension size:' + str(dim.getSize()))
            record.append('hidden layer:' + List2String(hidden_layer_num[t_i]))
            record.append('budget:' + str(Budget))
            record.append('method: PSO')
            # PSO------------------------------------------------------------------------------------------------------
            p = 2.0
            g = 2.0
            popsize = SampleSize
            record.append('p:' + str(p))
            record.append('g:' + str(g))
            for r_i in range(run_repeat):
                print 'PSO ', r_i, '====================================================================='
                record.append('run num:' + str(r_i) + '================================================================')
                # run
                w, w_v = runPSO(dim, popsize, MaxIteration, p, g, gym_task.SumReward)

                record.append('x:' + List2String(w))
                record.append('fitness:' + str(w_v))
                for e_i in range(test_repeat):
                    print 'test num:', e_i, '------------------------------------------------------------'
                    record.append('test num:' + str(e_i) + '------------------------------------------------------')
                    stop_step = gym_task.ShowResult(w, e_i, monitor_record)
                    print 'stop step:', stop_step
                    record.append('stop step:' + str(stop_step))
            file_name = task_name[t_i] + '_pso' + '_results.txt'
            fo.FileWriter(file_name, record)

            # PSO end--------------------------------------------------------------------------------------------------

        # DE
        if True:
            print 'task name:', task_name[t_i]
            print 'max stop step:', max_step[t_i]
            print 'dimension size:', dim.getSize()
            print 'hidden layer:', hidden_layer_num[t_i]
            print 'budget:', Budget
            record = []
            record.append('task name:' + task_name[t_i])
            record.append('max stop step:' + str(max_step[t_i]))
            record.append('dimension size:' + str(dim.getSize()))
            record.append('hidden layer:' + List2String(hidden_layer_num[t_i]))
            record.append('budget:' + str(Budget))
            record.append('method: DE')
            # DE-------------------------------------------------------------------------------------------------------
            popsize = SampleSize
            for r_i in range(run_repeat):
                print 'DE ', r_i, '====================================================================='
                record.append('run num:' + str(r_i) + '================================================================')
                # run
                w, w_v = runDE(dim, popsize, MaxIteration, gym_task.SumReward)

                record.append('x:' + List2String(w))
                record.append('fitness:' + str(w_v))
                for e_i in range(test_repeat):
                    print 'test num:', e_i, '------------------------------------------------------------'
                    record.append('test num:' + str(e_i) + '------------------------------------------------------')
                    stop_step = gym_task.ShowResult(w, e_i, monitor_record)
                    print 'stop step:', stop_step
                    record.append('stop step:' + str(stop_step))
            file_name = task_name[t_i] + '_de' + '_results.txt'
            fo.FileWriter(file_name, record)

            # DE end--------------------------------------------------------------------------------------------------

runExp()

# runTest()

    # gym_task.setMaxStep(20000)
    # try_size = 10
    # for i in range(try_size):
    #     print 'try:', i
    #     gym_task.ShowResult(w, i)


# racos.ContinueOpt(Sphere, SampleSize, MaxIteration, PositiveNum, RandProbability, UncertainBits)

# nn_model = NN_Model(input_layer_num, hidden_layer_num, output_layer_num)
#
# a = 0.45
# w = []
# for i in range(nn_model.getParaNum()):
#     w.append(a)
#     a -= 0.01
#
# nn_model.ResetWeight(w)
#
# task_name = 'MountainCar-v0'
# max_step = 200
#
# gym_task = Gym_Task(task_name)
# gym_task.newNN_Model(hidden_layer_num)
# gym_task.setMaxStep(max_step)
# sum_reward = gym_task.SumReward(w)
# stop_step = gym_task.getStopStep()
#
# print 'reward:', sum_reward, 'stop step:', stop_step

# print 'model setting'