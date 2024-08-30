
from .core import QubitCollection
from . import qgate

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
    

    def initiate(self) -> None:
        self.forward()
    
    def finalize(self) -> None:
        queue: deque[QuantumOperation] = deque([self])
        order = []
        while queue:
            current = queue.popleft()
            if current in order: continue
            order.append(current)
            for child in current.children:
                queue.append(child)
        
        for current in reversed(order):
            if not current.alive:
                current.forward()
        
        self.alive = False

        for current in order:
            if not current.alive:
                current.backward()
    
    @property
    def reg(self) -> QubitCollection:
        if self._reg is None:
            raise ValueError("Quantum register is not initiated")
        return self._reg
    
    

class CreateOperation(QuantumOperation):
    def forward(self):
        print("CreateOperation forward")
        self._reg = QubitCollection(self.n)

    def backward(self):
        print("CreateOperation backward")
        self._reg = None


class BitNotOperation(QuantumOperation):
    def __init__(self, child: QuantumOperation):
        super().__init__(child.n)
        self.children.append(child)
    
    def forward(self):
        print("BitNotOperation forward")
        self._reg = QubitCollection(self.n)
        qgate.BitwiseCNOT(self.children[0].reg, self.reg)
        qgate.BitwiseX(self.reg)

    def backward(self):
        print("BitNotOperation backward")
        qgate.BitwiseX(self.reg)
        qgate.BitwiseCNOT(self.children[0].reg, self.reg)
        # untangle if necessary
        self._reg = None

class InplaceNotOperation(QuantumOperation):
    def __init__(self, child: QuantumOperation):
        super().__init__(child.n)
        self.children.append(child)
    
    def forward(self):
        self._reg = self.children[0].reg
        qgate.BitwiseX(self.reg)

    def backward(self):
        qgate.BitwiseX(self.reg)
        self._reg = None

