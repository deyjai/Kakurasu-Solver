"""
AC-3 + Backtracking solver for Kakurasu.

Includes:
- Domain-based CSP model
- MRV heuristic
- LCV heuristic
- Forward checking
- AC-3 constraint propagation
- Node counting
- Timeout handling
"""

from __future__ import annotations
from typing import Dict, Tuple, Set, List
from collections import deque
import time
import copy

Variable = Tuple[int, int]


def solve_with_ac3(
    row_targets: List[int],
    col_targets: List[int],
) -> dict:

    if len(row_targets) != len(col_targets):
        raise ValueError("Row and column target lists must be same length.")

    n = len(row_targets)

    domains: Dict[Variable, Set[int]] = {
        (r, c): {0, 1}
        for r in range(n)
        for c in range(n)
    }

    nodes_visited = 0
    start_time = time.time()

    neighbors = build_neighbors(n)

    # Initial AC-3 pass
    if not ac3(domains, neighbors, row_targets, col_targets, n):
        return {
            "status": "no_solution",
            "solution": None,
            "nodes_visited": nodes_visited,
            "time_elapsed": 0,
        }

    def backtrack(current_domains):

        nonlocal nodes_visited
        nodes_visited += 1

        if time.time() - start_time > 60:
            return "timeout"

        if all(len(current_domains[v]) == 1 for v in current_domains):
            return current_domains

        var = select_mrv(current_domains)

        for value in order_lcv(var, current_domains, neighbors):
            new_domains = copy.deepcopy(current_domains)
            new_domains[var] = {value}

            if forward_check(var, value, new_domains, row_targets, col_targets, n):
                if ac3(new_domains, neighbors, row_targets, col_targets, n):
                    result = backtrack(new_domains)
                    if result == "timeout":
                        return "timeout"
                    if result:
                        return result

        return None

    result = backtrack(domains)
    time_elapsed = time.time() - start_time

    if result == "timeout":
        return {
            "status": "timeout",
            "solution": None,
            "nodes_visited": nodes_visited,
            "time_elapsed": time_elapsed,
        }

    if result:
        solution = domains_to_grid(result, n)
        return {
            "status": "solved",
            "solution": solution,
            "nodes_visited": nodes_visited,
            "time_elapsed": time_elapsed,
        }

    return {
        "status": "no_solution",
        "solution": None,
        "nodes_visited": nodes_visited,
        "time_elapsed": time_elapsed,
    }


# =============================
# Heuristics
# =============================

def select_mrv(domains):
    unassigned = [v for v in domains if len(domains[v]) > 1]
    return min(unassigned, key=lambda v: len(domains[v]))


def order_lcv(var, domains, neighbors):
    def conflicts(value):
        count = 0
        for n_var in neighbors[var]:
            if value in domains[n_var]:
                count += 1
        return count
    return sorted(domains[var], key=conflicts)


# =============================
# Forward Checking
# =============================

def forward_check(var, value, domains, row_targets, col_targets, n):
    return (
        check_row_feasible(var[0], domains, row_targets, n)
        and
        check_col_feasible(var[1], domains, col_targets, n)
    )


# =============================
# AC-3
# =============================

def ac3(domains, neighbors, row_targets, col_targets, n):

    queue = deque()

    for Xi in domains:
        for Xj in neighbors[Xi]:
            queue.append((Xi, Xj))

    while queue:
        Xi, Xj = queue.popleft()

        if revise(domains, Xi, Xj, row_targets, col_targets, n):
            if not domains[Xi]:
                return False

            for Xk in neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))

    return True


def revise(domains, Xi, Xj, row_targets, col_targets, n):

    revised = False
    to_remove = set()

    for vi in domains[Xi]:
        supported = False
        for vj in domains[Xj]:
            if locally_feasible(
                Xi, vi, Xj, vj,
                domains, row_targets, col_targets, n
            ):
                supported = True
                break
        if not supported:
            to_remove.add(vi)

    if to_remove:
        domains[Xi] -= to_remove
        revised = True

    return revised


# =============================
# Feasibility Checks
# =============================

def locally_feasible(Xi, vi, Xj, vj, domains, row_targets, col_targets, n):

    # Save original domains
    old_Xi = domains[Xi]
    old_Xj = domains[Xj]

    # Temporarily assign values
    domains[Xi] = {vi}
    domains[Xj] = {vj}

    feasible = (
        check_row_feasible(Xi[0], domains, row_targets, n)
        and
        check_col_feasible(Xi[1], domains, col_targets, n)
        and
        check_row_feasible(Xj[0], domains, row_targets, n)
        and
        check_col_feasible(Xj[1], domains, col_targets, n)
    )

    # Restore domains
    domains[Xi] = old_Xi
    domains[Xj] = old_Xj

    return feasible


def check_row_feasible(row, domains, row_targets, n):

    min_sum = 0
    max_sum = 0

    for col in range(n):
        var = (row, col)
        if domains[var] == {1}:
            min_sum += col + 1
            max_sum += col + 1
        elif 1 in domains[var]:
            max_sum += col + 1

    return min_sum <= row_targets[row] <= max_sum


def check_col_feasible(col, domains, col_targets, n):

    min_sum = 0
    max_sum = 0

    for row in range(n):
        var = (row, col)
        if domains[var] == {1}:
            min_sum += row + 1
            max_sum += row + 1
        elif 1 in domains[var]:
            max_sum += row + 1

    return min_sum <= col_targets[col] <= max_sum


# =============================
# Utility
# =============================

def build_neighbors(n):

    neighbors = {}

    for r in range(n):
        for c in range(n):
            var = (r, c)
            neighbors[var] = set()

            for k in range(n):
                if k != c:
                    neighbors[var].add((r, k))
                if k != r:
                    neighbors[var].add((k, c))

    return neighbors


def domains_to_grid(domains, n):

    grid = [[0 for _ in range(n)] for _ in range(n)]

    for (r, c), values in domains.items():
        grid[r][c] = next(iter(values))

    return grid