from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Create the quantum circuit
qc = QuantumCircuit(2)

# Add a Hadamard gate to qubit 0
qc.h(0)

# Perform a controlled-X gate on qubit 1, controlled by qubit 0
qc.cx(0, 1)

# Calculate the statevector
state = Statevector(qc)

# Print the statevector
print("Final state:")
print(state)

# Calculate measurement probabilities
probabilities = state.probabilities()
print("\nMeasurement probabilities:")
for i, prob in enumerate(probabilities):
    print(f"|{i:02b}>: {prob:.4f}")
