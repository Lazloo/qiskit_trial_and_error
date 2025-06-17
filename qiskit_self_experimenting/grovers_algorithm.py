from qiskit import QuantumCircuit
import numpy as np


# Oracle für Grover's Algorithm
def create_oracle(marked_states, num_qubits):
    """Erstellt ein Oracle, das markierte Zustände identifiziert"""
    oracle = QuantumCircuit(num_qubits)

    # Markiere spezifische Zustände durch Phaseninversion
    for state in marked_states:
        # Erstelle Multi-Control-Z Gate für den markierten Zustand
        # num_bits = 4: bin(5) -> '0b101' -> '101' ->  '0101'
        #                      -> [(0, '1'), (1, '0'), (2, '1'), (3, '0')]
        for i, bit in enumerate(reversed(bin(state)[2:].zfill(num_qubits))):
            # Flippe nur  die wahrscheinlichkeiten von |0> und |1> an den positionen an denen der
            # gesuchte Zustand "0" is
            if bit == "0":
                oracle.x(i)

        # Multi-Control-Z Gate
        if num_qubits == 1:
            oracle.z(0)
        else:
            oracle.mcz(list(range(num_qubits - 1)), num_qubits - 1)

        # Rückgängig machen der X-Gates
        for i, bit in enumerate(reversed(bin(state)[2:].zfill(num_qubits))):
            if bit == "0":
                oracle.x(i)

    return oracle


# Grover-Operator implementieren
def grover_diffuser(num_qubits):
    """
    Implementiert den Grover-Diffuser: Wende Z gate auf invertierten Zustand an

    """
    diffuser = QuantumCircuit(num_qubits)

    # Hadamard auf alle Qubits
    diffuser.h(range(num_qubits))

    # |0...0⟩ Zustand markieren
    # why x: the Z-gate flips the sign of the |1> part but we need to flip the sign of |0>
    diffuser.x(range(num_qubits))
    diffuser.mcz(list(range(num_qubits - 1)), num_qubits - 1)
    diffuser.x(range(num_qubits))

    # Hadamard auf alle Qubits
    diffuser.h(range(num_qubits))

    return diffuser


# Vollständige Grover-Implementierung
def grover_search(marked_states, num_qubits):
    """Implementiert Grover's Search Algorithm"""
    # Optimale Anzahl von Iterationen
    num_iterations = int(np.pi / 4 * np.sqrt(2**num_qubits / len(marked_states)))

    # Quantenschaltkreis erstellen
    qc = QuantumCircuit(num_qubits, num_qubits)

    # Initialisierung: Superposition aller Zustände
    qc.h(range(num_qubits))

    # Oracle und Diffuser
    oracle = create_oracle(marked_states, num_qubits)
    # Der Diffuser begwegt die Nadel die theoretisch durch das oracle wieder zurück gedreht wird
    # Aber die Oracle-Bewegung abhängig von dem gesuchten Zustand ist, iterriert diese Bewegung
    # weiter zum gesuchten Zustand
    diffuser = grover_diffuser(num_qubits)

    # Grover-Iterationen
    for _ in range(num_iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(diffuser, inplace=True)

    # Messung
    qc.measure_all()

    return qc


# Beispiel: Suche nach Zustand |11⟩ in 2-Qubit-System
marked_states_of_interest = [3]  # |11⟩ = 3 in dezimal
num_qubits_total = 2
circuit = grover_search(marked_states_of_interest, num_qubits_total)
print("Grover Circuit erstellt für Suche nach Zustand |11⟩")
