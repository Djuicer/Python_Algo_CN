"""
哈密顿量（Hamiltonian）是经典力学和量子力学中的核心概念。它表示系统的
总能量，用于描述系统随时间的演化。

经典力学：
    H = T + V
    其中 T 为动能，V 为势能。

量子力学（一维有限差分形式）：
    可将空间离散为点，并用有限差分法近似二阶导数，从而数值求解定态
    Schrodinger 方程 H|psi> = E|psi>。这样可将连续的哈密顿算符转为矩阵：

        H[i][i]   = hbar^2 / (m * dx^2) + V(x_i)
        H[i][i+1] = H[i][i-1] = -hbar^2 / (2 * m * dx^2)

参考资料：
    - https://en.wikipedia.org/wiki/Hamiltonian_mechanics
    - https://en.wikipedia.org/wiki/Hamiltonian_(quantum_mechanics)
    - https://en.wikipedia.org/wiki/Finite_difference_method
"""


def classical_hamiltonian(
    mass: float, velocity: float, potential_energy: float
) -> float:
    """
    计算粒子的经典哈密顿量 H = T + V，其中 T = 0.5 * m * v^2 为动能。

    >>> classical_hamiltonian(2, 3, 5)
    14.0
    >>> classical_hamiltonian(1, 0, 10)
    10.0
    >>> classical_hamiltonian(2, -4, 0)
    16.0
    >>> classical_hamiltonian(-1, 2, 5)
    Traceback (most recent call last):
        ...
    ValueError: mass must be positive
    """
    if mass <= 0:
        raise ValueError("mass must be positive")

    kinetic_energy = 0.5 * mass * velocity**2
    return kinetic_energy + potential_energy


def quantum_hamiltonian(
    num_points: int,
    potential: list[float],
    mass: float = 1.0,
    hbar: float = 1.0,
    dx: float = 1.0,
) -> list[list[float]]:
    """
    使用定态 Schrodinger 方程的有限差分离散，构造粒子在一维势场中的
    哈密顿矩阵。

    >>> quantum_hamiltonian(3, [0.0, 0.0, 0.0])
    [[1.0, -0.5, 0.0], [-0.5, 1.0, -0.5], [0.0, -0.5, 1.0]]
    >>> quantum_hamiltonian(2, [1.0, 2.0], mass=2.0, hbar=1.0, dx=1.0)
    [[1.5, -0.25], [-0.25, 2.5]]
    >>> quantum_hamiltonian(3, [0.0, 0.0])
    Traceback (most recent call last):
        ...
    ValueError: potential must have length num_points
    >>> quantum_hamiltonian(0, [])
    Traceback (most recent call last):
        ...
    ValueError: num_points must be positive
    """
    if num_points <= 0:
        raise ValueError("num_points must be positive")
    if len(potential) != num_points:
        raise ValueError("potential must have length num_points")

    diag_term = hbar**2 / (mass * dx**2)
    off_diag_term = -(hbar**2) / (2 * mass * dx**2)

    hamiltonian = [[0.0] * num_points for _ in range(num_points)]
    for i in range(num_points):
        hamiltonian[i][i] = diag_term + potential[i]
        if i > 0:
            hamiltonian[i][i - 1] = off_diag_term
        if i < num_points - 1:
            hamiltonian[i][i + 1] = off_diag_term

    return hamiltonian


if __name__ == "__main__":
    from doctest import testmod

    testmod()
