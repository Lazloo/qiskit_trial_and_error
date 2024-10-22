from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
import numpy as np


# Native
def qft_circuit(n):
    circuit = QuantumCircuit(n)

    for j in range(n):
        circuit.h(j)
        for k in range(j + 1, n):
            circuit.cu(
                theta=2 * np.pi / 2 ** (k - j + 1),
                phi=0,
                lam=0,
                gamma=0,
                control_qubit=k,
                target_qubit=j,
            )

    # Swap qubits
    for i in range(n // 2):
        circuit.swap(i, n - i - 1)

    return circuit


print(qft_circuit(3))

# Alternative

qft = QFT(
    num_qubits=3,
    approximation_degree=0,
    do_swaps=True,
    inverse=False,
    insert_barriers=True,
    name="qft",
)
print(qft)

# Inverse
inv_qft = QFT(
    num_qubits=3,
    approximation_degree=0,
    do_swaps=True,
    inverse=True,
    insert_barriers=True,
    name="inv_qft",
)
print(inv_qft)
