from qiskit import QuantumCircuit
from matplotlib import pyplot as plt
from qiskit_ibm_runtime.fake_provider import FakeAlmadenV2
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator

# Create a new circuit with two qubits
qc = QuantumCircuit(2)

# Add a Hadamard gate to qubit 0
qc.h(0)

# Perform a controlled-X gate on qubit 1, controlled by qubit 0
qc.cx(0, 1)

# Return a drawing of the circuit using MatPlotLib ("mpl"). This is the
# last line of the cell, so the drawing appears in the cell output.
# Remove the "mpl" argument to get a text drawing.
# qc.draw("mpl")

# Set up six different observables.
# This example measures expectation values by using the qiskit.quantum_info submodule, which is specified by using
# operators (mathematical objects used to represent an action or process that changes a quantum state). The following
# code cell creates six two-qubit Pauli operators: IZ, IX, ZI, XI, ZZ, and XX.
# IZ -> Apply Identity Operator on the first qubit and the Z Operator on the second qubit
observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX", "YY"]
# observables_labels = ["ZZ"]
observables = [SparsePauliOp(label) for label in observables_labels]

# Here, something like the ZZ operator is a shorthand for the tensor product Z⊗Z, which means measuring Z on qubit 1 and
# Z on qubit 0 together, and obtaining information about the correlation between qubit 1 and qubit 0. Expectation values
# like this are also typically written as ⟨Z1Z0⟩. If the state is entangled, then the measurement of ⟨Z1Z0⟩ should be 1.

# The following code instantiates a real device to submit a job to and transforms the circuit and observables to match
# that backend's  Instruction Set Architecture (ISA) .
# QiskitRuntimeService.save_account(channel="ibm_quantum", token="TOKEN")

# If you did not previously save your credentials, use the following line instead:
# service = QiskitRuntimeService(channel="ibm_quantum", token="<MY_IBM_QUANTUM_TOKEN>")
# service = QiskitRuntimeService()
# backend = service.least_busy(simulator=False, operational=True)

# LOCAL testing
backend = FakeAlmadenV2()

# Convert to an ISA circuit and layout-mapped observables.
pm = generate_preset_pass_manager(backend=backend, optimization_level=0)
isa_circuit = pm.run(qc)

# isa_circuit.draw("mpl", idle_wires=False)

# Run Estimation
# You can estimate the value of the observable by using the Estimator class. Estimator is one of two primitives;
# the other is Sampler, which can be used to get data from a quantum computer.
# Construct the Estimator instance.
estimator = Estimator(mode=backend)
estimator.options.resilience_level = 1
estimator.options.default_shots = 100

mapped_observables = [
    observable.apply_layout(isa_circuit.layout) for observable in observables
]

# One pub, with one circuit to run against five different observables.
job = estimator.run([(isa_circuit, mapped_observables)])

# sampler = Sampler(mode=backend)
# sampler.options.default_shots = 1
# job_2 = sampler.run([(isa_circuit, mapped_observables)])

# Use the job ID to retrieve your job data later
print(f">>> Job ID: {job.job_id()}")

# This is the result of the entire submission.  You submitted one Pub,
# so this contains one inner result (and some metadata of its own).
job_result = job.result()
# job_result_2 = job_2.result()

# This is the result from our single pub, which had six observables,
# so contains information on all six.
pub_result = job.result()[0]
# pub_result = job_2.result()[0]


# Graphical Analysis
# Plot the result

values = pub_result.data.evs
errors = pub_result.data.stds

# plotting graph
plt.close("all")
plt.plot(observables_labels, values, "-o")
plt.errorbar(
    observables_labels,
    values,
    yerr=errors,
    fmt="o-",
    capsize=5,
    capthick=1,
    ecolor="red",
    color="blue",
)
plt.xlabel("Observables")
plt.ylabel("Values")
plt.savefig("my_plot.png")
