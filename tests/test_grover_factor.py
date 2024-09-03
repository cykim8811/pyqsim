
import pyqsim as pq
import numpy as np
import math

from pyqsim.types import qint
from pyqsim.gates import h, z


a = h(qint(0, size=4))
b = h(qint(0, size=4))

iter_count = round(math.pi / 4 * math.sqrt(2 ** 8 / 2))
for _ in range(iter_count):
    z(a * b == 91)
    z((h(a) == 0) & (h(b) == 0))

print(a, b)
