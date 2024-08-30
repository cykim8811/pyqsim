
import pyqsim
import numpy as np

a = ~pyqsim.qint1_t()

b = a.copy()

b = ~b

print(a.measure(), b.measure())
