from qiskit import QuantumCircuit

def phi_plus_meassured():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc

# Define a trivial entanglement introspection circuit (CHSH-type test)
def chsh_circuit():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.h(1)
    qc.measure([0, 1], [0, 1])
    return qc

# This is a simple proxy for entanglement correlation, not a full CHSH test.
def compute_entanglement_correlation(counts):
    prob_00 = counts.get('00', 0) / sum(counts.values())
    prob_11 = counts.get('11', 0) / sum(counts.values())
    return prob_00 + prob_11  # Proxy for correlation
