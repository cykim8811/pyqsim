
import pyqsim


a = pyqsim.types.qint(7, size=4)
b = pyqsim.types.qint(6, size=4)

c = pyqsim.types.qint(0, size=1)

N = 9

pyqsim.bitgate.mod_addition_controlled(a.transform.reg.qubits, b.transform.reg.qubits, N, c.transform.reg.qubits[0])

print(a, b)

