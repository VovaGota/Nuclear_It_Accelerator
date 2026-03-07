import numpy as np
from itertools import product

# Исходные параметры
alpha_i = -0.5
beta_i = 5
gamma_i = (1 + alpha_i**2) / beta_i

alpha_f = 0
beta_f = 8
gamma_f = (1 + alpha_f**2) / beta_f

M_i = np.array([[gamma_i, alpha_i],
                [alpha_i, beta_i]])
M_f = np.array([[gamma_f, alpha_f],
                [alpha_f, beta_f]])

# Возможные типы матриц
def drift(L):
    return np.array([[1, L],
                     [0, 1]])

def thin_lens(f):
    return np.array([[1, 0],
                     [-1/f, 1]])

def thin_lens_plus(f):
    return np.array([[1, 0],
                     [1/f, 1]])

matrix_types = [
    ('drift', drift, np.linspace(0.1, 10, 20)),
    ('lens-', thin_lens, np.linspace(0.1, 10, 20)),
    ('lens+', thin_lens_plus, np.linspace(0.1, 10, 20))
]

# Проверка равенства с точностью
def is_close(A, B, tol=1e-6):
    return np.all(np.abs(A - B) < tol)

# Генератор комбинаций параметров для последовательности
def parameter_combinations(seq):
    grids = [t[2] for t in seq]
    return product(*grids)

# Основная функция поиска решений
def find_solutions(max_length=4):
    solutions = []
    for length in range(1, max_length + 1):
        for types_seq in product(matrix_types, repeat=length):
            for params in parameter_combinations(types_seq):
                M = M_i.copy()
                for (m_type, m_func, _), p in zip(types_seq, params):
                    M = m_func(p) @ M
                if is_close(M, M_f):
                    solution = [(t[0], p) for t, p in zip(types_seq, params)]
                    solutions.append(solution)
    return solutions

# Пример поиска
max_length = 4
solutions = find_solutions(max_length)

if solutions:
    print(f"Найдено {len(solutions)} решений для цепочек до длины {max_length}:")
    for sol in solutions:
        print(sol)
else:
    print("Решений не найдено в выбранной сетке.")






