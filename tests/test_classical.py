
import pyqsim

from pyqsim.types import qint

# Addition
a = qint(3, size=4)
b = qint(5, size=4)

print(f"a + b = {a + b}")


# Multiplication
a = qint(3, size=4)
b = qint(5, size=4)

print(f"a * b = {a * b}")


# Function
def test1(p, q):
    return p * q

a = qint(3, size=4)
b = qint(5, size=4)

print(f"test1(a, b) = {test1(a, b)}")


# Function with local variable
def test2(p):
    t = p + 3
    return p * t

a = qint(3, size=4)

print(f"test2(a) = {test2(a)}") # Automatically uncomputes t
