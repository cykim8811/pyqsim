
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
    entangle([control, target])
    quantum_state = control.quantum_state

    control_index = quantum_state.qubits.index(control)
    target_index = quantum_state.qubits.index(target)

    new_indices = np.arange(quantum_state.state.size)
    new_indices = new_indices ^ ((1 << target_index) * ((new_indices >> control_index) & 1))

    quantum_state.state = quantum_state.state[new_indices]

def bit_measure(q: Qubit) -> int:
    quantum_state = q.quantum_state
    index = quantum_state.qubits.index(q)

    probabilities = np.abs(quantum_state.state) ** 2
    mask = 1 << index

    zero_indices = np.where((np.arange(quantum_state.state.size) & mask) == 0)
    one_indices = np.where((np.arange(quantum_state.state.size) & mask) != 0)

    zero_probability = np.sum(probabilities[zero_indices])
    one_probability = np.sum(probabilities[one_indices])

    result = 0 if np.random.rand() < zero_probability else 1

    if result == 0:
        quantum_state.state[one_indices] = 0
        quantum_state.state /= np.sqrt(zero_probability)
    else:
        quantum_state.state[zero_indices] = 0
        quantum_state.state /= np.sqrt(one_probability)
    
    # untangle - remove qubit from quantum state
    quantum_state.qubits.remove(q)
    q.quantum_state = QuantumState(q)
    if result == 0:
        q.quantum_state.state = np.array([1, 0], dtype=np.complex64)
        quantum_state.state = quantum_state.state[zero_indices]
    else:
        q.quantum_state.state = np.array([0, 1], dtype=np.complex64)
        quantum_state.state = quantum_state.state[one_indices]

    return result

def entangle(qubits: List[Qubit]) -> None:
    quantum_states = list(set([qubit.quantum_state for qubit in qubits]))
    
    if len(quantum_states) == 1:
        return
    
    for i in range(1, len(quantum_states)):
        quantum_states[0].state = np.kron(quantum_states[i].state, quantum_states[0].state)
        quantum_states[0].qubits.extend(quantum_states[i].qubits)
    
    for q in quantum_states[0].qubits:
        q.quantum_state = quantum_states[0]


def BitwiseX(qc: QubitCollection) -> None:
    for q in qc.qubits:
        X(q)


def BitwiseCNOT(control: QubitCollection, target: QubitCollection) -> None:
    if len(control.qubits) != len(target.qubits):
        raise ValueError("Control and target qubit collections must have the same length")
    
    for c, t in zip(control.qubits, target.qubits):
        CNOT(c, t)


def measure(qc: QubitCollection) -> int:
    if len(qc.qubits) == 0:
        raise ValueError("Cannot measure an empty qubit collection")
    
    results = [bit_measure(q) for q in qc.qubits]
    return int("".join(map(str, results)), 2)

