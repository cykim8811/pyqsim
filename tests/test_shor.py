
import pyqsim


a = pyqsim.types.qint(5, size=3)
b = 7
r = pyqsim.types.qint(0, size=6)

c = pyqsim.types.qint(0, size=1)

N = 9

pyqsim.bitgate.mod_multiplication_immediate_controlled(a.transform.reg.qubits, b, r.transform.reg.qubits, N, c.transform.reg.qubits[0])

print(a, b, r)

