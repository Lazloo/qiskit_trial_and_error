from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


def bernstein_vazirani_circuit(
    secret_str: str, use_ancilla: bool = True, use_paired_qubits: bool = False
):
    """
    Create a Bernstein-Vazirani quantum circuit based on the given secret string and configuration.

    This function generates a quantum circuit for the Bernstein-Vazirani algorithm, which aims to
    determine a secret string using a single query to a quantum oracle. The function supports
    different circuit configurations based on the input parameters.

    Args:
        secret_str (str): The secret binary string to be encoded in the quantum oracle.
        use_ancilla (bool, optional): Whether to use an ancilla qubit in the circuit.
                                      Defaults to True.
        use_paired_qubits (bool, optional): Whether to use paired qubits for each bit of the
                                            secret string. Defaults to False.

    Returns:
        QuantumCircuit: A Qiskit QuantumCircuit object representing the Bernstein-Vazirani circuit.

    Circuit Configurations:
    1. use_ancilla=True, use_paired_qubits=False (Default):
       - Uses n+1 qubits (n input qubits + 1 ancilla qubit)
       - Applies CX gates between input qubits and the ancilla qubit
    2. use_ancilla=False, use_paired_qubits=True:
       - Uses 2n qubits (n input qubits + n paired qubits)
       - Applies CX gates between each input qubit and its corresponding paired qubit
    3. use_ancilla=False, use_paired_qubits=False:
       - Uses n qubits (input qubits only)
       - Applies X gates to the input qubits (Note: This might need adjustment based on specific requirements)

    Note:
    - The secret string 's' is interpreted with s0 as the rightmost bit and sn-1 as the leftmost bit.
    - The circuit includes initialization, oracle implementation, measurement basis change, and measurement.
    - Barriers are added for visual separation and to control the Qiskit transpiler optimizations.

    Example:
        >>> circuit = bernstein_vazirani_circuit("101")
        >>> circuit_no_ancilla = bernstein_vazirani_circuit("101", use_ancilla=False, use_paired_qubits=True)
    """

    n = len(secret_str)

    # Determine the number of qubits based on the chosen configuration
    num_qubits = n + 1 if use_ancilla else 2 * n if use_paired_qubits else n

    circuit = QuantumCircuit(num_qubits, n)

    # Initialize qubits
    if use_ancilla:
        circuit.x(n)
        circuit.h(range(n + 1))
    else:
        circuit.h(range(n))

    circuit.barrier()

    # Oracle implementation
    for i, bit in enumerate(reversed(secret_str)):
        if bit == "1":
            if use_ancilla:
                circuit.cx(i, n)
            elif use_paired_qubits:
                circuit.cx(i, n + i)
            else:
                # For the case without ancilla or paired qubits, we might need a different approach
                # This is a placeholder and might need adjustment based on specific requirements
                circuit.x(i)

    circuit.barrier()

    # Measurement basis change
    circuit.h(range(n))

    # Measurement
    circuit.measure(range(n), range(n))

    return circuit


secret_string = "10110101"  # Example secret string
bv_circuit = bernstein_vazirani_circuit(secret_string)
print(bv_circuit)

# Execute the circuit on a simulator
# Create the AerSimulator
simulator = AerSimulator()

# Execute the circuit
job = simulator.run(bv_circuit, shots=1024)
result = job.result()

# state = Statevector(bv_circuit)
# print("Final state:")
# print(state)
# probabilities = state.probabilities()
# print("\nMeasurement probabilities:")
# for i, prob in enumerate(probabilities):
#     print(f"|{i:02b}>: {prob:.4f}")

# Get and print the results
counts = result.get_counts()
print("Measurement outcomes:", counts)

# Visualize the results
plot_histogram(counts, filename="hist.png")
