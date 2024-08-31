
from .core import QubitCollection
from . import reggate
from . import bitgate

from collections import deque
from typing import List

class QuantumOperation:
    n: int
    _reg: QubitCollection | None
    alive: bool
    children: List['QuantumOperation']

    def __init__(self, n: int):
        self.n = n
        self.alive = True
        self.children = []

    def forward(self) -> None:
        raise NotImplementedError

    def backward(self) -> None:
        raise NotImplementedError
    
    def apply_forward(self) -> None:
        self.forward()

    def apply_backward(self) -> None:
        self.backward()
    

    def initiate(self) -> None:
        self.apply_forward()
    
    def finalize(self) -> None: # TODO: Optimize this
        queue: deque[QuantumOperation] = deque([self])
        order = []
        while queue:
            current = queue.popleft()
            if current in order:
                order.remove(current)
            order.append(current)
            for child in current.children:
                queue.append(child)
        for current in reversed(order):
            if not current.alive:
                current.apply_forward()
        
        self.alive = False

        for current in order:
            if not current.alive:
                current.apply_backward()
    
    @property
    def reg(self) -> QubitCollection:
        if self._reg is None:
            raise ValueError("Quantum register is not initiated")
        return self._reg
    
    

class CreateOperation(QuantumOperation):
    def __init__(self, n: int, value: int = 0):
        super().__init__(n)
        self.value = value

    def forward(self):
        self._reg = QubitCollection(self.n)
        reggate.maskedBitwiseX(self.reg, self.value)

    def backward(self):
        reggate.maskedBitwiseX(self.reg, self.value)
        reggate.measure(self.reg)
        self._reg = None


class CopyOperation(QuantumOperation):
    def __init__(self, child: QuantumOperation):
        super().__init__(child.n)
        self.children.append(child)
    
    def forward(self):
        self._reg = QubitCollection(self.n)
        reggate.bitwiseCNOT(self.children[0].reg, self.reg)

    def backward(self):
        reggate.bitwiseCNOT(self.children[0].reg, self.reg)
        reggate.measure(self.reg)
        self._reg = None


class BitNotOperation(QuantumOperation):
    def __init__(self, child: QuantumOperation):
        super().__init__(child.n)
        self.children.append(child)
    
    def forward(self):
        self._reg = QubitCollection(self.n)
        reggate.bitwiseCNOT(self.children[0].reg, self.reg)
        reggate.bitwiseX(self.reg)

    def backward(self):
        reggate.bitwiseX(self.reg)
        reggate.bitwiseCNOT(self.children[0].reg, self.reg)
        reggate.measure(self.reg)
        self._reg = None


class HadamardOperation(QuantumOperation):
    def __init__(self, child: QuantumOperation):
        super().__init__(child.n)
        self.children.append(child)
    
    def forward(self):
        self._reg = QubitCollection(self.n)
        self.children[0]._reg, self._reg = self._reg, self.children[0]._reg
        reggate.bitwiseH(self.reg)

    def backward(self):
        reggate.bitwiseH(self.reg)
        self.children[0]._reg, self._reg = self._reg, self.children[0]._reg
        reggate.measure(self.reg)
        self._reg = None


class BitAndOperation(QuantumOperation):
    def __init__(self, child1: QuantumOperation, child2: QuantumOperation):
        super().__init__(child1.n)
        self.children.append(child1)
        self.children.append(child2)
    
    def forward(self):
        self._reg = QubitCollection(self.n)
        reggate.bitwiseMCX([self.children[0].reg, self.children[1].reg], self.reg)

    def backward(self):
        reggate.bitwiseMCX([self.children[0].reg, self.children[1].reg], self.reg)
        reggate.measure(self.reg)
        self._reg = None


class BitOrOperation(QuantumOperation):
    def __init__(self, child1: QuantumOperation, child2: QuantumOperation):
        super().__init__(child1.n)
        self.children.append(child1)
        self.children.append(child2)
    
    def forward(self):
        self._reg = QubitCollection(self.n)
        reggate.bitwiseX(self.children[0].reg)
        reggate.bitwiseX(self.children[1].reg)
        reggate.bitwiseMCX([self.children[0].reg, self.children[1].reg], self.reg)
        reggate.bitwiseX(self.children[0].reg)
        reggate.bitwiseX(self.children[1].reg)

    def backward(self):
        reggate.bitwiseX(self.children[0].reg)
        reggate.bitwiseX(self.children[1].reg)
        reggate.bitwiseMCX([self.children[0].reg, self.children[1].reg], self.reg)
        reggate.bitwiseX(self.children[0].reg)
        reggate.bitwiseX(self.children[1].reg)
        reggate.measure(self.reg)
        self._reg = None


class EqualImmediateOperation(QuantumOperation):
    def __init__(self, child: QuantumOperation, value: int):
        super().__init__(1)
        self.children.append(child)
        self.value = value
    
    def forward(self):
        self._reg = QubitCollection(self.n)
        reggate.maskedBitwiseX(self.children[0].reg, self.value)
        bitgate.MCX(self.children[0].reg.qubits, self.reg.qubits[0])

