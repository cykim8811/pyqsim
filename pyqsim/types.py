
from .core import QuantumRegister
from . import operations


class qint1_t(QuantumRegister):
    def __init__(self):
        super().__init__(operations.CreateOperation(1))

class qint2_t(QuantumRegister):
    def __init__(self, value: int=0):
        super().__init__(operations.CreateOperation(2, value))

class qint4_t(QuantumRegister):
    def __init__(self, value: int=0):
        super().__init__(operations.CreateOperation(4, value))

class qint8_t(QuantumRegister):
    def __init__(self, value: int=0):
        super().__init__(operations.CreateOperation(8, value))


