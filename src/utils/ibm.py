
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

def run_and_monitor_circuit(circuit, backend, shots):
    sampler = Sampler(mode=backend)
    transpiled_circuit = transpile(circuit, backend)

    # Record submission time
    submission_time = clean_datetimes(datetime.now())

    # Launch the job
    job = sampler.run([transpiled_circuit], shots=shots)

    # Dictionary to hold the first time each state is seen
    state_timestamps = {
        "SUBMITTED": submission_time,
        "QUEUED": None,
        "INITIALIZING": None,
        "RUNNING": None,
        "DONE": None,
    }

    # Polling loop
    terminal_states = {"DONE", "CANCELLED", "ERROR"}
    polled_states = {"QUEUED", "INITIALIZING", "RUNNING"}
    while True:
        status = job.status()
        now = clean_datetimes(datetime.now())

        if status in polled_states and state_timestamps[status] is None:
            state_timestamps[status] = now

        if status in terminal_states:
            if state_timestamps["DONE"] is None and status == "DONE":
                state_timestamps["DONE"] = now
            break

        time.sleep(1.0)  # adjust polling interval as needed

    result = job.result()

    return {
        "counts": result[0].data.c.get_counts(),
        "timestamps": state_timestamps,
        "job_id": job.job_id(),
    }