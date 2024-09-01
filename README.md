# pyqsim: High-Level Quantum Computing Simulation in Python

pyqsim is a Python library designed to simplify quantum computing simulation through high-level abstractions. It aims to make quantum programming more accessible and intuitive, bridging the gap between classical and quantum computing paradigms.

## Features

- **High-Level Abstraction**: Move beyond low-level circuit and qubit manipulations to a more intuitive programming model.
- **Automatic Inverse Operations**: Objects automatically perform inverse operations upon deletion, maintaining quantum state consistency.
- **Familiar Programming Model**: Use quantum data types similarly to classical types like int, making the transition to quantum computing smoother for classical programmers.
- **Eager Execution**: Computations are performed immediately as Python functions are called, allowing for real-time interaction and debugging.
- **Quantum-Classical Hybrid Programming**: Seamlessly mix quantum operations with classical programming constructs.

## Installation

```bash
pip install pyqsim
```

## Quick Start

Here's a simple example implementing Deutsch's algorithm:

```python
import pyqsim
from pyqsim.gates import h, z

def oracle(x): return x  # Constant function

a = pyqsim.types.qint1_t()
z(oracle(h(a)))
result = pyqsim.gates.measure(a)
print("Constant" if result == 0 else "Balanced")
```

## Advanced Usage

Check out the `examples/` directory for more complex quantum algorithms implementations, including Grover's search algorithm.

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any queries or support, please open an issue on our GitHub repository or contact me at [cykim@snu.ac.kr](mailto:cykim@snu.ac.kr).
