"""
使用 Qiskit 框架为指定数量的量子比特构建量子 Fourier 变换（QFT）。

该电路可作为构建模块，用于设计量子计算中的 Shor 算法、量子相位估计等。

该电路使用 Qiskit 内置的纯 Python ``BasicSimulator`` 模拟（无需编译后的
``qiskit-aer`` 后端），因此可在任何能够安装 Qiskit 的环境中运行。

参考资料：
https://en.wikipedia.org/wiki/Quantum_Fourier_transform
https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.QFT
"""

import math

import numpy as np
import qiskit
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit.providers.basic_provider import BasicSimulator


def quantum_fourier_transform(number_of_qubits: int = 3) -> qiskit.result.counts.Counts:
    """
    构建并模拟作用于全零态 ``|0...0>`` 的量子 Fourier 变换。QFT 将
    ``|0...0>`` 映射为均匀叠加态，因此每个计算基测量结果的概率相同
    （忽略采样噪声）。

    # number_of_qubits = 3 时的量子电路：
                                               ┌───┐
    qr_0: ──────■──────────────────────■───────┤ H ├─X─
                │                ┌───┐ │P(π/2) └───┘ │
    qr_1: ──────┼────────■───────┤ H ├─■─────────────┼─
          ┌───┐ │P(π/4)  │P(π/2) └───┘               │
    qr_2: ┤ H ├─■────────■───────────────────────────X─
          └───┘
    cr: 3/═════════════════════════════════════════════

    参数：
        number_of_qubits : 量子比特数量

    返回：
        qiskit.result.counts.Counts: 10,000 次采样得到的测量计数。

    模拟设置了随机种子，因此观测结果集合可复现：

    >>> counts = quantum_fourier_transform(2)
    >>> sorted(counts)
    ['00', '01', '10', '11']
    >>> sum(counts.values())
    10000
    >>> quantum_fourier_transform(-1)
    Traceback (most recent call last):
        ...
    ValueError: number of qubits must be > 0.
    >>> quantum_fourier_transform('a')
    Traceback (most recent call last):
        ...
    TypeError: number of qubits must be a integer.
    >>> quantum_fourier_transform(100)
    Traceback (most recent call last):
        ...
    ValueError: number of qubits too large to simulate(>10).
    >>> quantum_fourier_transform(0.5)
    Traceback (most recent call last):
        ...
    ValueError: number of qubits must be an exact integer.

    >>> result = quantum_fourier_transform(2)
    >>> 2350<=result['10']<=2600
    True
    >>> 2350<=result['00']<=2600
    True
    >>> 2350<=result['11']<=2600
    True
    >>> 2350<=result['01']<=2600
    True
    >>> res = quantum_fourier_transform(3)
    >>> 1150<=res['000']<=1350 and 1150<=res['001']<=1350
    True
    >>> 1150<=res['010']<=1350 and 1150<=res['100']<=1350
    True
    >>> 1150<=res['101']<=1350 and 1150<=res['110']<=1350
    True
    >>> 1150<=res['011']<=1350 and 1150<=res['111']<=1350
    True
    """
    if isinstance(number_of_qubits, str):
        raise TypeError("number of qubits must be a integer.")
    if number_of_qubits <= 0:
        raise ValueError("number of qubits must be > 0.")
    if math.floor(number_of_qubits) != number_of_qubits:
        raise ValueError("number of qubits must be exact integer.")
    if number_of_qubits > 10:
        raise ValueError("number of qubits too large to simulate(>10).")

    qr = QuantumRegister(number_of_qubits, "qr")
    cr = ClassicalRegister(number_of_qubits, "cr")

    quantum_circuit = QuantumCircuit(qr, cr)

    counter = number_of_qubits

    for i in range(counter):
        quantum_circuit.h(number_of_qubits - i - 1)
        counter -= 1
        for j in range(counter):
            quantum_circuit.cp(np.pi / 2 ** (counter - j), j, counter)

    for k in range(number_of_qubits // 2):
        quantum_circuit.swap(k, number_of_qubits - k - 1)

    # 测量所有量子比特
    quantum_circuit.measure(qr, cr)

    # 使用纯 Python BasicSimulator 模拟 10000 次；设置运行种子，确保上方
    # doctest 的观测结果可复现。
    backend = BasicSimulator()
    transpiled_circuit = transpile(quantum_circuit, backend)
    job = backend.run(transpiled_circuit, shots=10_000, seed_simulator=42)

    return job.result().get_counts(quantum_circuit)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Total count for quantum Fourier transform state is:")
    print(f"{quantum_fourier_transform(3) = }")
