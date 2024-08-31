
import pyqsim
from pyqsim.gates import h, z
import numpy as np
import math


def oracle(x):
    return x == 5


for i in range(16):
    a = pyqsim.types.qint4_t(i)
    res = oracle(a)
    if res.measure() == 1:
        print(f"Oracle found solution: {i}")
        break



a = h(pyqsim.types.qint8_t(0))

for i in range(round(math.pi/4 * math.sqrt(2**8))):
    z(oracle(a))
    z(h(a)==0)
print(f"Oracle found solution: {a.measure()}")

