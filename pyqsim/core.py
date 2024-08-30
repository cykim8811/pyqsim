

from typing import List
from cirq.devices import line_qubit

from collections import deque


class QuantumOperation:
    n: int
    reg: List[line_qubit.LineQubit]
    alive: bool
    children: List['QuantumOperation']

    def __init__(self, n: int):
        self.n = n
        self.reg = line_qubit.LineQubit.range(n)
        self.alive = True

    def __forward(self):
        raise NotImplementedError

    def __backward(self):
        raise NotImplementedError
    

    def initiate(self):
        self.__forward()
    
    def finalize(self):
        queue: deque[QuantumOperation] = deque([self])
        order = []
        while queue:
            current = queue.popleft()
            order.append(current)
            for child in current.children:
                queue.append(child)
        
        for current in reversed(order):
            if not current.alive:
                current.__forward()
        
        self.__backward()

        for current in order:
            if not current.alive:
                current.__backward()



class QuantumRegister:
    transform: QuantumOperation

    def __init__(self, transform: QuantumOperation):
        self.transform = transform
        self.transform.initiate()


    def __del__(self):
        self.transform.finalize()
