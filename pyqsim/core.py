
import numpy as np

from .qubit import QubitCollection
from . import operations
from . import reggate

from collections import deque
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING: from .operations import QuantumOperation


class QuantumRegister:
    transform: 'QuantumOperation'

    def __init__(self, transform: 'QuantumOperation'):
        self.transform = transform
        self.transform.initiate()

    def __del__(self):
        self.transform.finalize()

    def __invert__(self):
        return QuantumRegister(operations.BitNotOperation(self.transform))
    
    def copy(self):
        return QuantumRegister(operations.CopyOperation(self.transform))

    def __and__(self, other: 'QuantumRegister') -> 'QuantumRegister':
        return QuantumRegister(operations.BitAndOperation(self.transform, other.transform))

    def __or__(self, other: 'QuantumRegister') -> 'QuantumRegister':
        return QuantumRegister(operations.BitOrOperation(self.transform, other.transform))

    def __eq__(self, value: 'QuantumRegister | int') -> 'QuantumRegister':
        if isinstance(value, int):
            return QuantumRegister(operations.EqualImmediateOperation(self.transform, value))
        
        # return QuantumRegister(operations.EqualOperation(self.transform, value.transform))
        raise NotImplementedError("Equality comparison between two quantum registers is not yet implemented")

    def __add__(self, other: 'QuantumRegister') -> 'QuantumRegister':
        return QuantumRegister(operations.AddOperation(self.transform, other.transform))
    
    def __sub__(self, other: 'QuantumRegister') -> 'QuantumRegister':
        return QuantumRegister(operations.SubOperation(self.transform, other.transform))

