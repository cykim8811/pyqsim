
from typing import List

import numpy as np


class QuantumState:
    qubits: List['Qubit']
    def __init__(self, qubit: 'Qubit'):
        self.qubits = [qubit]
        self.state = np.array([1, 0], dtype=np.complex64)


class Qubit:
    quantum_state: QuantumState
    def __init__(self):
        self.quantum_state = QuantumState(self)


class QubitCollection:
    qubits: List[Qubit]
    def __init__(self, n: int):
        self.qubits = [Qubit() for _ in range(n)]

