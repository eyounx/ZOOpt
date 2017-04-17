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
"""

"""
The class ActivationFunction defines some activation functions.

Author:
    Yuren Liu
"""
import math


class ActivationFunction:

    @staticmethod
    # sigmoid function
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
