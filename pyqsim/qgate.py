
from .qubit import QubitCollection, Qubit, QuantumState

import numpy as np

from typing import List


def X(q: Qubit) -> None:
    quantum_state: QuantumState = q.quantum_state
    index = quantum_state.qubits.index(q)
    
    mask = 1 << index

    new_indices = np.arange(quantum_state.state.size) ^ mask

    quantum_state.state = quantum_state.state[new_indices]


def CNOT(control: Qubit, target: Qubit) -> None:
    control_state: QuantumState = control.quantum_state
    target_state: QuantumState = target.quantum_state

    control_index = control_state.qubits.index(control)
    target_index = target_state.qubits.index(target)

    new_indices = np.arange(target_state.state.size)
    new_indices = new_indices ^ ((1 << target_index) * ((new_indices >> control_index) & 1))

    target_state.state = target_state.state[new_indices]



def qubit_entangle(qubits: List[Qubit]) -> None:
    quantum_states = list(set([qubit.quantum_state for qubit in qubits]))
    
    if len(quantum_states) == 1:
        return
    
    for i in range(1, len(quantum_states)):
        quantum_states[0].state = np.kron(quantum_states[0].state, quantum_states[i].state)
        quantum_states[0].qubits.extend(quantum_states[i].qubits)
    
    for q in qubits:
        q.quantum_state = quantum_states[0]


def entangle(qcs: List[QubitCollection]) -> None:
    qubits: List[Qubit] = []
    for qc in qcs:
        qubits.extend(qc.qubits)
    
    quantum_states = list(set([qubit.quantum_state for qubit in qubits]))
    
    if len(quantum_states) == 1:
        return
    
    for i in range(1, len(quantum_states)):
        quantum_states[0].state = np.kron(quantum_states[0].state, quantum_states[i].state)
        quantum_states[0].qubits.extend(quantum_states[i].qubits)
    
    for q in qubits:
        q.quantum_state = quantum_states[0]

def BitwiseX(qc: QubitCollection) -> None:
    for q in qc.qubits:
        X(q)


def BitwiseCNOT(control: QubitCollection, target: QubitCollection) -> None:
    if len(control.qubits) != len(target.qubits):
        raise ValueError("Control and target qubit collections must have the same length")
    
    for c, t in zip(control.qubits, target.qubits):
        CNOT(c, t)

