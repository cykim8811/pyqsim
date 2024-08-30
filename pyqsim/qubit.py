
from typing import List

import numpy as np


class QuantumState:
    qubits: List['Qubit']
    def __init__(self):
        self.qubits = []
        self.state = np.ones(1, dtype=np.complex64)


class Qubit:
    pass


class QubitCollection:
    def __init__(self, n: int):
        self.qubits = [Qubit() for _ in range(n)]

