
from typing import List
from .qubit import QubitCollection
from .bitgate import *

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

