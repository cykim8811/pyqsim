
import numpy as np

from .qubit import QubitCollection
from . import operations

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
    
