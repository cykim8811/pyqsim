
import pyqsim
from pyqsim.gates import h, z
import numpy as np



def oracle1(x):
    return x & x


a = pyqsim.types.qint4_t(5)

print(a.measure())