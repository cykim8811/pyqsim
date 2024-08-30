
import pyqsim

a = pyqsim.qint1_t()

b = ~a

print(b.transform.reg.qubits[0].quantum_state.state)

del a
del b

