
import pyqsim
from pyqsim.gates import h, z

print("Testing Deutsch's algorithm")


# Define oracles

def oracle0(x): return x
def oracle1(x): return ~x
def oracle2(x): return x & ~x
def oracle3(x): return x | ~x

oracles = [oracle0, oracle1, oracle2, oracle3]


# Run Deutsch's algorithm
for i, oracle in enumerate(oracles):
    print(f"Oracle{i}: ", end="")
    a = pyqsim.types.qint(0, size=1)
    z(oracle(h(a)))
    res = pyqsim.gates.measure(a)
    if res == 0:
        print("Constant")
    else:
        print("Balanced")

