from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Create the quantum circuit
qc = QuantumCircuit(2, 1)


# We always start with |0>, X Gate initializes q_1 to 1
qc.x(1)

# Add a Hadamard gate to both qubits
qc.h([0, 1])

# Apply the oracle (this example uses a balanced function) -> keep Input qubit unchanged and affect only the
# second qubit
qc.cx(0, 1)


# Apply the final Hadamard gate to the input qubit
qc.h(0)

print(qc)

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


# Measure the input qubit
qc.measure(0, 0)
