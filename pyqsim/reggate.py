
from typing import List
from .qubit import QubitCollection
from .bitgate import *
import math

def bitwiseX(qc: QubitCollection) -> None:
    for q in qc.qubits:
        X(q)

def maskedBitwiseX(qc: QubitCollection, mask: int) -> None:
    for q in qc.qubits:
        if mask & 1:
            X(q)
        mask >>= 1

def bitwiseCNOT(control: QubitCollection, target: QubitCollection) -> None:
    if len(control.qubits) != len(target.qubits):
        raise ValueError("Control and target qubit collections must have the same length")
    
    for c, t in zip(control.qubits, target.qubits):
        CNOT(c, t)

def measure(qc: QubitCollection) -> int:
    if len(qc.qubits) == 0:
        raise ValueError("Cannot measure an empty qubit collection")
    
    results = sum([bit_measure(q) * (1 << i) for i, q in enumerate(qc.qubits)])

    return results

def bitwiseH(qc: QubitCollection) -> None:
    for q in qc.qubits:
        H(q)

def bitwiseMCX(controls: List[QubitCollection], target: QubitCollection) -> None:
    if len(controls) == 0:
        raise ValueError("Cannot perform a multi-controlled X gate with no control qubits")
    
    for c in controls:
        if len(c.qubits) != len(target.qubits):
            raise ValueError("Control and target qubit collections must have the same length")
    
    for i in range(len(target.qubits)):
        MCX([c.qubits[i] for c in controls], target.qubits[i])

def bitwiseZ(qc: QubitCollection) -> None:
    for q in qc.qubits:
        Z(q)

def QFT(qc: QubitCollection) -> None:
    n = len(qc.qubits)
    
    qc.qubits.reverse()
    
    for i in range(n):
        # Apply Hadamard gate to the current qubit
        H(qc.qubits[i])
        
        # Apply controlled rotation gates
        for j in range(i + 1, n):
            k = j - i
            CPHASE(qc.qubits[j], qc.qubits[i], math.pi / (2 ** k))
    
    qc.qubits.reverse()
    
def IQFT(qc: QubitCollection) -> None:
    n = len(qc.qubits)
    
    qc.qubits.reverse()
    
    for i in range(n - 1, -1, -1):
        # Apply inverse controlled rotation gates
        for j in range(n - 1, i, -1):
            k = j - i
            CPHASE(qc.qubits[j], qc.qubits[i], -math.pi / (2 ** k))
        
        # Apply Hadamard gate to the current qubit
        H(qc.qubits[i])
    
    qc.qubits.reverse()

def addition(target: QubitCollection, operand: QubitCollection) -> None:
    if len(target.qubits) != len(operand.qubits):
        raise ValueError("Target and operand qubit collections must have the same length")
    
    n = len(target.qubits)
    
    QFT(target)

    for i in range(n):
        for k in range(i, n):
            CPHASE(target.qubits[k], operand.qubits[i], math.pi / (2 ** (k - i)))

    IQFT(target)

def subtraction(target: QubitCollection, operand: QubitCollection) -> None:
    if len(target.qubits) != len(operand.qubits):
        raise ValueError("Target and operand qubit collections must have the same length")
    
    n = len(target.qubits)
    
    QFT(target)

    for i in range(n):
        for k in range(i, n):
            CPHASE(target.qubits[k], operand.qubits[i], -math.pi / (2 ** (k - i)))

    IQFT(target)


