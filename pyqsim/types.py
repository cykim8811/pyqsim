
from .core import QuantumRegister
from . import operations

class qint(QuantumRegister):
    def __init__(self, value: int=0, size: int=1):
        super().__init__(operations.CreateOperation(size, value))
