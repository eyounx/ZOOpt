"""
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

  Copyright (C) 2017 Nanjing University, Nanjing, China
  LAMDA, http://lamda.nju.edu.cn
"""
from random import Random

"""
This file records Global variables used in the algorithm
Author:
    Yuren Liu
"""

class Global:
    rand = None

    def __init__(self):
        # rand is the random object used by all files
        self.rand = Random()
        self.set_seed(100)
        self.precision = 1e-17
        # rand.seed(100)

    # Set random seed
    def set_seed(self, seed):
        self.rand.seed(seed)
        return

    # Set precision, precision is used to judge whether two floats are equal
    def set_precision(self, my_precision):
        self.precision = my_precision
        return

gl = Global()
# constants
pos_inf = float('Inf')
neg_inf = float('-Inf')
nan = float('Nan')
