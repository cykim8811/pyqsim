
import pyqsim
from pyqsim.gates import h, z
import math

print("Testing Grover's algorithm")


# Define oracle

def oracle(x):  # x in [0, 255]
    return x == 27


# Run Grover's algorithm
a = h(pyqsim.types.qint(0, size=8))

count = round(math.pi / 4 * math.sqrt(2**8))
for _ in range(count):
    z(oracle(a))
    z(h(a) == 0)

res = pyqsim.gates.measure(a)
print(f"Found {res} in {count} iterations")

