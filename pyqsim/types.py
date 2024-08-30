
from .core import QuantumRegister
from . import operations

class qint4_t(QuantumRegister):
    def __init__(self):
        super().__init__(operations.CreateOperation(4))

class qint1_t(QuantumRegister):
    def __init__(self):
        super().__init__(operations.CreateOperation(1))