
from .qubit import QubitCollection, Qubit

import numpy as np

from typing import List


def entangle(qcs: List[QubitCollection]) -> None:
    qubits: List[Qubit] = []
    for qc in qcs:
        qubits.extend(qc.qubits)
    
    quantum_states = list(set([qubit.quantum_state for qubit in qubits]))
    
    if len(quantum_states) == 1:
        return
    
    for i in range(1, len(quantum_states)):
        quantum_states[0].state = np.kron(quantum_states[0].state, quantum_states[i].state)
        


def BitX(qc: QubitCollection) -> None:
    pass


def BitCNOT(control: QubitCollection, target: QubitCollection) -> None:
    pass

