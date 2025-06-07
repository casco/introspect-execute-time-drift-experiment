from qiskit import QuantumCircuit
from collections import defaultdict
import numpy as np

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

def packed_chsh_circuit():
    qc = QuantumCircuit(8, 8)

    # Bell state preparation (H + CX)
    for i in range(0, 8, 2):
        qc.h(i)
        qc.cx(i, i+1)

    # Settings:
    # Pair 0–1: A0 = Z (identity), B0 = RY(-π/4) → 22.5°
    qc.ry(-np.pi/4, 1)

    # Pair 2–3: A0 = Z, B1 = RY(π/4) → -22.5°
    qc.ry(np.pi/4, 3)

    # Pair 4–5: A1 = RY(-π/2) → 45°, B0 = RY(-π/4)
    qc.ry(-np.pi/2, 4)
    qc.ry(-np.pi/4, 5)

    # Pair 6–7: A1 = RY(-π/2), B1 = RY(π/4)
    qc.ry(-np.pi/2, 6)
    qc.ry(np.pi/4, 7)

    # Measure all
    qc.measure(range(8), range(8))

    return qc


def compute_parallel_CHSH_scores(counts):
   
    # Given a counts dictionary from an 8-qubit packed CHSH measurement,
    # extract the four 2-qubit subcounts (one per qubit pair),
    # compute the CHSH correlator (S) for each pair, and return a dict.

    pair_counts = [defaultdict(int) for _ in range(4)]
    
    for bitstring, count in counts.items():
        # Reverse bitstring if needed (Qiskit endianness)
        bits = bitstring[::-1]  # Assuming little-endian order (qubit 0 is LSB)
        
        for i in range(4):
            a = bits[2*i]
            b = bits[2*i + 1]
            pair_key = a + b
            pair_counts[i][pair_key] += count

    def compute_E(c):
        total = sum(c.values())
        if total == 0:
            return 0
        e = 0
        for bstr, n in c.items():
            parity = 1 if bstr in ('00', '11') else -1
            e += parity * n / total
        return e

    # Each pair represents a different measurement setting:
    # Pair 0: A0-B0 (Z-Z)
    # Pair 1: A0-B1 (Z–(Z+X)/√2)
    # Pair 2: A1-B0 (X-Z)
    # Pair 3: A1-B1 (X–(Z+X)/√2)
    E = [compute_E(c) for c in pair_counts]

    S = E[0] + E[1] + E[2] - E[3]

    return {
        'E00': E[0],
        'E01': E[1],
        'E10': E[2],
        'E11': E[3],
        'CHSH_score': S
    }