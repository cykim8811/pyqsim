
import pyqsim

a = pyqsim.Qubit()
b = pyqsim.Qubit()

pyqsim.qubit_entangle([a, b])

print(a.quantum_state.state)