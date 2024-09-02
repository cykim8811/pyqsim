
import pyqsim as pq
import numpy as np

from pyqsim.types import qint
from pyqsim.gates import qft, measure

a = qint(5, size=4)
b = qint(12 , size=4)

pq.reggate.addition(a.transform.reg, b.transform.reg)

print(measure(a), measure(b))

