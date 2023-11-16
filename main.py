# Quantum key distribution using BB84 protocol

from qiskit import QuantumCircuit, Aer, execute
from qiskit.providers.aer.noise import NoiseModel
from qiskit.quantum_info import state_fidelity
from qiskit.tools.monitor import job_monitor
from qiskit.providers.aer.noise.errors import depolarizing_error
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
import numpy as np


# create Bob's quantum circuit with measurement
def create_circuit_bob():
    circuit = QuantumCircuit (1, 1)
    circuit.measure (0, 0)
    circuit.draw (output='mpl')  # this is to qiskit to draw the circuit
    return circuit


# create Alice and Bob's quantum circuits
def create_circuit(hadamard=False, measure=False):
    circuit = QuantumCircuit (1, 1)
    if hadamard:
        circuit.h (0)
    if measure:
        circuit.measure (0, 0)
    circuit.draw (output='mpl')
    return circuit


# create the quantum channel between Alice and Bob
def quantum_channel(alice, bob):
    backend = Aer.get_backend ('statevector_simulator')
    job = execute (alice, backend)
    result = job.result ()
    state = result.get_statevector ()
    bob.initialize (state, 0)
    bob.draw (output='mpl')


# create the noise model
def noise_model():
    error = depolarizing_error (0.05, 1)
    noise_model = NoiseModel ()
    noise_model.add_all_qubit_quantum_error (error, ['u1', 'u2', 'u3'])
    return noise_model


alice = create_circuit (hadamard=True, measure=True)
bob = create_circuit_bob ()  # Use the create_circuit_bob function here
eve = create_circuit (hadamard=True, measure=True)


# create the quantum circuit for Alice and Bob
def alice_bob():
    return create_circuit (hadamard=True, measure=True)


# create the quantum circuit for Bob and Eve
def bob_eve():
    return create_circuit ()


# create the quantum circuit for Alice and Eve
def alice_eve():
    return create_circuit (hadamard=True, measure=True)


# create the quantum circuit for Alice, Bob and Eve
def alice_bob_eve():
    return create_circuit (hadamard=True, measure=True)


# make the quantum key distribution
def execute_circuit(circuit, backend, shots=1, noise_model=None):
    job = execute (circuit, backend, shots=shots, noise_model=noise_model)
    job_monitor (job)
    result = job.result ()
    counts = result.get_counts ()
    print (counts)
    if '0' in counts:
        circuit.x (0)
    return circuit


backend = Aer.get_backend ('qasm_simulator')

alice = execute_circuit (alice, backend, noise_model=noise_model ())
bob = execute_circuit (bob, backend, noise_model=noise_model ())
eve = execute_circuit (eve, backend, noise_model=noise_model ())


# run the quantum key distribution
def run():
    alice = alice_bob ()
    bob = bob_eve ()
    quantum_channel (alice, bob)
    alice_eve ()
    backend = Aer.get_backend ('statevector_simulator')
    job = execute (alice, backend)
    result = job.result ()
    alice_state = result.get_statevector ()
    job = execute (bob, backend)
    result = job.result ()
    bob_state = result.get_statevector ()
    fidelity = state_fidelity (alice_state, bob_state)
    print (fidelity)
    return fidelity


if __name__ == '__main__':
    fidelity = run ()
    print (fidelity)
