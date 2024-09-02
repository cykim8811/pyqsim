
import pyqsim as pq
import numpy as np

from pyqsim.types import qint
from pyqsim.gates import qft, measure

a = qint(15, size=4)
b = qint(7, size=4)

c = a - b

print(measure(c))

