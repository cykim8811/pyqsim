
import pyqsim as pq
import numpy as np

from pyqsim.types import qint
from pyqsim.gates import qft, measure, h, iqft


print(qint(3, size=4) * qint(9, size=4))

