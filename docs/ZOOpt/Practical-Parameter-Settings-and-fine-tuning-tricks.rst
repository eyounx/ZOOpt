Practical Parameter Settings and Fine-tuning Tricks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. contents:: Table of Contents

Practical Parameter Settings
-----------------------------

Enable parallel optimization
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

.. code:: python

    parameter = Parameter(..., parallel=True, server_num=3, ...)

Using parallel optimization in ZOOpt is quite simple, just adding two keys in the definition of the parameter. In this example, ZOOpt will start three daemon processors for evaluating the solution. Make sure that the server_num is less than the number of available cores of your compouter, otherwise the overhead of competing for computing resources will be high.  

Set seed
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

.. code:: python

    parameter = Parameter(..., seed=999, ...)

Fixing the seed makes the optimization result reproducible. Note that if the parallel optimization is enabled, fixing the seed cannot
reprodece the result because it cannot assure the same sequence of evaluated solutions. 

Specify some initial samples 
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
.. code:: python

    dim_size = 10
    sol1 = Solution(x = [0] * dim_size)
    sol2 = Solution(x = [1] * dim_size)
    parameter = Parameter(..., init_samples=[sol1, sol2], ...)

In some cases, users have known several good solutions of a problem. ZOOpt can use them as initial samples, helping accelerating the optimization. Another more common situation is that users want to resume the optmization when the budget runs out. To achieve this,  users can use the last result that ZOOpt outputs as a initial sample in the next optimization progress.  The number of initial samples should not exceed the population size (train_size). 

Print intermediate results
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

.. code:: python

    parameter = Parameter(..., intermediate_result=True, intermediate_freq=100, ...)

``intermediate_result`` and ``intermediate_freq`` are set for showing
intermediate results during the optimization progress. The procedure
will show the best solution every ``intermediate_freq`` calls to the
objective function if ``intermediate_result=True``.
``intermediate_freq`` is set to 100 by default.

In this example, the optimization procedure will print the best solution
every 100 budgets.

Set population size manually
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

.. code:: python

    parameter = Parameter(budget=20000)
    parameter.set_train_size(22)
    parameter.set_positive_size(2)

In ZOOpt, population size is represented by ``train_size``.
``train_size`` represents the size of the binary classification data
set, which is a component of the optimization algorithm ``RACOS``, ``SRACOS`` and ``SSRACOS``.
``positive_size`` represents the size of the positive data among all
data. ``negetive_size`` is set to ``train_size`` - ``positive_size``
automatically. There is no need to set it manually.

In most cases, default setting can work well and there's no need to set
them manually.

Set the time limit
>>>>>>>>>>>>>>>>>>>>>>

.. code:: python

    parameter = Parameter(..., time_budget=3600, ...)

In this example, time budget is 3600s and it means if the
running time exceeds 3600s, the optimization procedure will stop early
and return the best solution so far regardless of the budget.

Customize a stopping criterion
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

.. code:: python

    class StoppingCriterion:
        def __init__(self):
            self.__best_result = 0 
            self.__count = 0
            self.__total_count = 0
            self.__count_limit = 100

        def check(self, optcontent):
            """
            :param optcontent: an instance of the class RacosCommon. Several functions can be invoked to get the contexts of the optimization, which are listed as follows,
            optcontent.get_best_solution(): get the current optimal solution
            optcontent.get_data(): get all the solutions contained in the current solution pool
            optcontent.get_positive_data(): get positive solutions contained in the current solution pool
            optcontent.get_negative_data(): get negative solutions contained in the current solution pool

            :return: bool object.

            """
            self.__total_count += 1
            content_best_value = optcontent.get_best_solution().get_value()
            if content_best_value == self.__best_result:
                self.__count += 1
            else:
                self.__best_result = content_best_value
                self.__count = 0
            if self.__count >= self.__count_limit:
                print("stopping criterion holds, total_count: %d" % self.__total_count)
                return True
            else:
                return False

    parameter = Parameter(budget=20000, stopping_criterion=StoppingCriterion())

StoppingCriterion customizes a stopping criterion for the optimization, which is used as a initialization parameter of the class Parameter and should implement a member function ``check(self, optcontent)``. The ``check`` function is invoked at each iteration of the optimization. The optimization will stop if this function returns True, otherwise, it is not affected. In this example, the optimization will be stopped if the best result remains unchanged for 100 iterations.

Fine-tuning Tricks
-----------------------------
As shown in the previous introduction, the number of adjustable parameters in ZOOpt may look scary. However, remember that there is no need to set each parameter manually. ZOOpt's default parameters can work well in most case. In this part, we will introduce some advisable fine-tuning tricks to configure the best zeroth-order optimization solver for your task. 

Adjust the uncertain_bits
>>>>>>>>>>>>>>>>>>>>>>>>>>
``uncertain_bits`` determines how many bits can be different from the present best solution when a new solution is sampled from the learned search space. In default, when the dimension size is less than 50, uncertain_bits equals 1. When the dimension size is between 50 and 1000, 
uncertain_bits equals 3, otherwise, uncertain_bits equals 5. We suggest to use smaller uncertain_bits at first especially when the budget is abundant. For example, the uncertain_bits can be set to be 1 even if the dimension size is larger than 50.

.. code:: python

   par = Parameter(..., uncertain_bit=1, ...)

Adjust the exploration rate
>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Exploration rate (sample from the whole search space) is an important factor for the optimization. In default, it is set to be only 1%. This setting can help ZOOpt achieve good results in locally highly non-convex but globally trendy functions. For many real-world optimization tasks, there is no obvious trend in global either. We suggest to increase exploration rate in such conditions, e.g., incresing the exploration rate to 10% or 20%. 

.. code:: python

   par = Parameter(..., exploration_rate = 0.2, ...)
