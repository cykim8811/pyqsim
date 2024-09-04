
import pyqsim


a = pyqsim.types.qint(8, size=4)
b = pyqsim.types.qint(8, size=4)

N = 9

pyqsim.bitgate.mod_addition(a.transform.reg.qubits, b.transform.reg.qubits, N)

print(a, b)
