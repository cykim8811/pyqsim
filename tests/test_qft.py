
import pyqsim as pq
import numpy as np

for i in range(4):
    a = pq.types.qint2_t(i)
    pq.bitgate.entangle([a.transform.reg.qubits[1], a.transform.reg.qubits[0]])

    pq.gates.qft(a)

    display = np.round(a.transform.reg.qubits[0].quantum_state.state, 3) * 2
    print(display)


