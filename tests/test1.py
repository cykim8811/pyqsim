
import pyqsim

b = ~pyqsim.qint1_t()

c = pyqsim.QuantumRegister(pyqsim.operations.CopyOperation(b.transform))


print(c.transform.reg.qubits[0].quantum_state.state)
