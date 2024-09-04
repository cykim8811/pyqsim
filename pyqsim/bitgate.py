
from .qubit import Qubit, QuantumState

import numpy as np

from typing import List


def X(q: Qubit) -> None:
    quantum_state: QuantumState = q.quantum_state
    index = quantum_state.qubits.index(q)
    
    mask = 1 << index

    new_indices = np.arange(quantum_state.state.size) ^ mask

    quantum_state.state = quantum_state.state[new_indices]

def Z(q: Qubit) -> None:
    quantum_state: QuantumState = q.quantum_state
    index = quantum_state.qubits.index(q)
    
    mask = 1 << index

    quantum_state.state[(np.arange(quantum_state.state.size) & mask) != 0] *= -1

def P(q: Qubit, phi: float) -> None:
    quantum_state: QuantumState = q.quantum_state
    index = quantum_state.qubits.index(q)

    mask = 1 << index

    quantum_state.state[(np.arange(quantum_state.state.size) & mask) != 0] *= np.exp(1j * phi)

def CNOT(control: Qubit, target: Qubit) -> None:
    entangle([control, target])
    quantum_state = control.quantum_state

    control_index = quantum_state.qubits.index(control)
    target_index = quantum_state.qubits.index(target)

    new_indices = np.arange(quantum_state.state.size)
    new_indices = new_indices ^ ((1 << target_index) * ((new_indices >> control_index) & 1))

    quantum_state.state = quantum_state.state[new_indices]

def MCX(controls: List[Qubit], target: Qubit) -> None:
    entangle(controls + [target])
    quantum_state = controls[0].quantum_state

    control_indices = [quantum_state.qubits.index(q) for q in controls]
    target_index = quantum_state.qubits.index(target)

    mask = 0
    for index in control_indices:
        mask |= 1 << index

    new_indices = np.arange(quantum_state.state.size)
    new_indices = new_indices ^ ((1 << target_index) * ((new_indices & mask) == mask))

    quantum_state.state = quantum_state.state[new_indices]

def MCZ(controls: List[Qubit], target: Qubit | None = None) -> None:
    if target is not None:
        controls.append(target)
    entangle(controls)
    quantum_state = controls[0].quantum_state

    control_indices = [quantum_state.qubits.index(q) for q in controls]

    mask = 0
    for index in control_indices:
        mask |= 1 << index

    target_indices = np.arange(quantum_state.state.size) & mask == mask

    quantum_state.state[target_indices] *= -1

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
    # quantum_states = list(set([qubit.quantum_state for qubit in qubits]))
    quantum_states = []
    for qubit in qubits:
        if qubit.quantum_state not in quantum_states:
            quantum_states.append(qubit.quantum_state)
    
    if len(quantum_states) == 1:
        return
    
    for i in range(1, len(quantum_states)):
        quantum_states[0].state = np.kron(quantum_states[i].state, quantum_states[0].state)
        quantum_states[0].qubits.extend(quantum_states[i].qubits)
    
    for q in quantum_states[0].qubits:
        q.quantum_state = quantum_states[0]

def H(q: Qubit) -> None:
    quantum_state = q.quantum_state
    index = quantum_state.qubits.index(q)

    mask = 1 << index

    zero_indices = np.where((np.arange(quantum_state.state.size) & mask) == 0)
    one_indices = np.where((np.arange(quantum_state.state.size) & mask) != 0)

    quantum_state.state[zero_indices], quantum_state.state[one_indices] = (quantum_state.state[zero_indices] + quantum_state.state[one_indices]) / np.sqrt(2), (quantum_state.state[zero_indices] - quantum_state.state[one_indices]) / np.sqrt(2)

def CPHASE(control: Qubit, target: Qubit, phi: float) -> None:
    entangle([control, target])
    quantum_state = control.quantum_state

    control_index = quantum_state.qubits.index(control)
    target_index = quantum_state.qubits.index(target)

    mask = (1 << control_index) | (1 << target_index)

    quantum_state.state[(np.arange(quantum_state.state.size) & mask) == mask] *= np.exp(1j * phi)

def MCPHASE(controls: List[Qubit], target: Qubit, phi: float) -> None:
    entangle(controls + [target])
    quantum_state = controls[0].quantum_state

    control_indices = [quantum_state.qubits.index(q) for q in controls]
    target_index = quantum_state.qubits.index(target)

    mask = 0
    for index in control_indices:
        mask |= 1 << index
    mask |= 1 << target_index

    quantum_state.state[(np.arange(quantum_state.state.size) & mask) == mask] *= np.exp(1j * phi)

def bit_addition(target: List[Qubit], operand: List[Qubit]) -> None:
    if len(target) < len(operand):
        raise ValueError("Target qubits must have at least as many qubits as the operand qubits")
    
    n = len(target)
    
    QFT(target)

    for i in range(n):
        for k in range(i, n):
            CPHASE(target[k], operand[i], 2 * np.pi / (2 ** (k - i + 1)))

    IQFT(target)

def bit_subtraction(target: List[Qubit], operand: List[Qubit]) -> None:
    if len(target) < len(operand):
        raise ValueError("Target qubits must have at least as many qubits as the operand qubits")
    
    n = len(target)
    
    QFT(target)

    for i in range(n):
        for k in range(i, n):
            CPHASE(target[k], operand[i], -2 * np.pi / (2 ** (k - i + 1)))

    IQFT(target)

def bit_QFT(qubits: List[Qubit]) -> None:
    n = len(qubits)
    
    qubits.reverse()
    
    for i in range(n):
        # Apply Hadamard gate to the current qubit
        H(qubits[i])
        
        # Apply controlled rotation gates
        for j in range(i + 1, n):
            k = j - i
            CPHASE(qubits[j], qubits[i], np.pi / (2 ** k))
    
    qubits.reverse()

def bit_IQFT(qubits: List[Qubit]) -> None:
    n = len(qubits)
    
    qubits.reverse()
    
    for i in range(n - 1, -1, -1):
        # Apply inverse controlled rotation gates
        for j in range(n - 1, i, -1):
            k = j - i
            CPHASE(qubits[j], qubits[i], -np.pi / (2 ** k))
        
        # Apply Hadamard gate to the current qubit
        H(qubits[i])
    
    qubits.reverse()

def bit_multiplication(a: List[Qubit], b: List[Qubit], result: List[Qubit]) -> None:
    if len(result) < len(a) + len(b):
        raise ValueError("Result qubit collection must have at least twice the length of the input qubit collections")
    
    n_a = len(a)
    n_b = len(b)
    n_result = len(result)
    
    QFT(result)
    
    for i in range(n_a):
        for j in range(n_b):
            for k in range(n_result):
                MCPHASE([a[i], b[j]], result[k], math.pi / 2 **(k-i-j))

    IQFT(result)

def bit_inv_multiplication(a: List[Qubit], b: List[Qubit], result: List[Qubit]) -> None:
    if len(result) < len(a) + len(b):
        raise ValueError("Result qubit collection must have at least twice the length of the input qubit collections")
    
    n_a = len(a)
    n_b = len(b)
    n_result = len(result)
    
    QFT(result)

    for i in reversed(range(n_a)):
        for j in reversed(range(n_b)):
            for k in reversed(range(n_result)):
                MCPHASE([a[i], b[j]], result[k], -math.pi / 2 **(k-i-j))

    IQFT(result)

