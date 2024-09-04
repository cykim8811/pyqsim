
import pyqsim


a = pyqsim.gates.h(pyqsim.types.qint(0, size=4))
b = pyqsim.types.qint(0, size=4)

def ftn(x: int) -> int:
    return (3 ** x) % 7

pyqsim.bitgate.arbitrary_operation(a.transform.reg.qubits, b.transform.reg.qubits, ftn)

print(a, b)


