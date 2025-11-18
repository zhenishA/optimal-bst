"""
Optimal Binary Search Tree (OBST) — пример реализации (Python).

Этот скрипт вычисляет DP-таблицы e (ожидаемая стоимость), w (веса) и root (корни)
по классическому алгоритму CLRS (с учётом q — вероятностей неудачных поисков).
В конце печатается таблица root в виде, аналогичном примеру в README.
"""

from typing import List, Tuple


def optimal_bst(p: List[float], q: List[float], n: int) -> Tuple[List[List[float]], List[List[int]]]:
    """
    Compute expected cost table e and root table for Optimal Binary Search Tree.

    Args:
        p: list of probabilities of successful searches (length n), 1..n mapped to p[0]..p[n-1]
        q: list of probabilities of unsuccessful searches (length n+1), q[0]..q[n]
        n: number of keys

    Returns:
        e: (n+2) x (n+1) table (we use 1-based indexing for keys)
        root: (n+2) x (n+1) table of chosen roots (indices 1..n)
    """
    # Allocate tables with indices up to n+1 (1-based convenient)
    e = [[0.0] * (n + 1) for _ in range(n + 2)]
    w = [[0.0] * (n + 1) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 2)]

    # Base cases: e[i][i-1] = q[i-1], w[i][i-1] = q[i-1]
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]

    # Main DP
    for length in range(1, n + 1):                # length = number of keys in interval
        for i in range(1, n - length + 2):        # start index
            j = i + length - 1                    # end index
            e[i][j] = float("inf")
            # compute weight w[i][j]
            w[i][j] = w[i][j - 1] + p[j - 1] + q[j]

            # try all possible roots r in [i..j]
            for r in range(i, j + 1):
                cost = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if cost < e[i][j]:
                    e[i][j] = cost
                    root[i][j] = r

    return e, root


def print_root_table(root: List[List[int]], n: int) -> None:
    """
    Print root table in rectangular form matching README example
    (rows and columns from 0..n to show base row/column).
    """
    print("Таблица корней (root[i][j])")
    # header
    header = ["i\\j"] + [str(j) for j in range(0, n + 1)]
    print("  ".join(f"{h:>3}" for h in header))
    for i in range(0, n + 1):
        row_vals = []
        for j in range(0, n + 1):
            # We print root[i][j] when indices valid (i and j in 1..n and i<=j),
            # else print 0 to match the example layout.
            if 1 <= i <= n and 1 <= j <= n:
                row_vals.append(str(root[i][j]))
            else:
                row_vals.append("0")
        print(f"{i:>3}  " + "  ".join(f"{v:>2}" for v in row_vals))


if __name__ == "__main__":
    # Пример из README
    p = [0.15, 0.10, 0.05]                # p1, p2, p3
    q = [0.05, 0.10, 0.05, 0.05]          # q0, q1, q2, q3
    n = len(p)

    e_table, root_table = optimal_bst(p, q, n)

    # Печать ожидаемой таблицы корней в формате, похожем на пример
    print_root_table(root_table, n)

    # Показать главный корень (root[1][n])
    print("\nГлавный корень:")
    print(f"root[1][n] = {root_table[1][n]}  (означает k_{root_table[1][n]} как корень)")

    # (Опционально) распечатать таблицу e — ожидаемых стоимостей (форматированно)
    print("\nТаблица ожидаемых стоимостей e[i][j] (1-based indices):")
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            val = e_table[i][j] if j >= i else 0.0
            row.append(f"{val:6.2f}")
        print(" ".join(row))
