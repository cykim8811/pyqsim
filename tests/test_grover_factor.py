
import pyqsim as pq
import numpy as np

from pyqsim.types import qint
from pyqsim.gates import h, z

a = h(qint(0, size=4))
b = h(qint(0, size=4))

# pq.bitgate.entangle(a.transform.reg.qubits + b.transform.reg.qubits)

for _ in range(3):
    z(a+b==15)
    z((h(a) == 0) & (h(b) == 0))


# for i in range(2 ** 4):
#     print(f"{i:04b} -> {a.transform.reg.qubits[0].quantum_state.state[i]:.2f}")

print(a, b)
