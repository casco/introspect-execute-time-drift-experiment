from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# Transpile our backend-independent circuit to the backend we'll use
def transpile(qc, backend):
  pass_manager = generate_preset_pass_manager(optimization_level=3,
                                            backend=backend)
  return pass_manager.run(qc)