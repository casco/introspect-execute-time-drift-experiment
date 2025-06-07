
from datetime import datetime
import time
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.providers.jobstatus import JobStatus
from dotenv import load_dotenv
from qiskit import transpile
import os
from src.utils.python_utils import clean_datetimes

# Get the quantum computer from IBM that we think will become available sooner.
def get_backend():
  load_dotenv()
  ibm_token = os.getenv("IBM_QUANTUM_TOKEN")
  service = QiskitRuntimeService(channel="ibm_quantum", token=ibm_token)
  return service.least_busy(operational=True, simulator=False)

# Get a shapshot of a backend's properties so we can later analyze what we got.
def get_backend_snapshot(backend):
    return clean_datetimes(backend.properties().to_dict())

# Run the circuit and wrap results (counts) with job stats
def run_and_wrap(circuit, backend, shots):
    sampler = Sampler(mode=backend)
    transpiled_circuit = transpile(circuit, backend)
    job = sampler.run([transpiled_circuit], shots=shots)
    result = job.result()
    return {
        "counts": result[0].data.c.get_counts(),
        "timestamps": job.metrics()['timestamps'],
        'usage': job.metrics()['usage'],
        "job_id": job.job_id(),
    }
