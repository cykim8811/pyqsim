
import pyqsim
from pyqsim.gates import h, z
import numpy as np



def oracle1(x):
    return ~x


a = pyqsim.types.qint1_t()
b = h(a)
c = ~b
print(b.transform.reg.qubits[0].quantum_state.state)
pyqsim.bitgate.Z(c.transform.reg.qubits[0])
print(b.transform.reg.qubits[0].quantum_state.state)
