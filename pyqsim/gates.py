
from . import operations
from . import reggate
from .core import QuantumRegister

def h(qr: QuantumRegister) -> QuantumRegister:
    return QuantumRegister(operations.HadamardOperation(qr.transform))

def z(qr: QuantumRegister) -> None:
    operations.reggate.bitwiseZ(qr.transform.reg)

def qft(qr: QuantumRegister) -> QuantumRegister:
    return QuantumRegister(operations.QFTOperation(qr.transform))

def measure(qr: QuantumRegister) -> int:
    return reggate.measure(qr.transform.reg)

