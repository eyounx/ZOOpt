"""
Objective functions can be implemented in this file

Author:
    Yu-Ren Liu

Time:
    2017.1.20
"""

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

 Copyright (C) 2015 Nanjing University, Nanjing, China
"""

from theano import function
import theano.tensor as T
import numpy


# Sphere
x = T.dvector('x')
value_sphere = ((x - 0.2)**2).sum()
Sphere = function([x], value_sphere)


# Arkley
a = 20
b = 0.2
c = 2 * numpy.pi
bias = [-0.151132887462, 0.388548543877, -0.933234772744, -0.581705468848, 0.920983693072, -0.117206127637,
        -0.716147047949, 0.231077702939, -0.751868710065, -0.968869507224]
length = T.shape(x)[0]
value_seq = -b * numpy.sqrt(((x - bias) ** 2).sum() / length)
RE = function([x], value_seq)
value_cos = (c * (x - bias)).cos().sum() / length
value_arkley = -a * numpy.exp(value_seq) - numpy.exp(value_cos) + a + numpy.e
Arkley = function([x], value_arkley)
