"""
Backtracking (DFS) solver for Kakurasu.

This implementation:
- Uses depth-first search
- Applies early pruning
- Counts visited nodes
- Tracks runtime
- Supports timeout handling
"""
from __future__ import annotations
from typing import List
import time


def solve_kakurasu_backtracking(
    row_targets: List[int],
    col_targets: List[int],
) -> dict:
    """
    Solve Kakurasu using DFS backtracking.

    Args:
        row_targets: Target sums for each row.
        col_targets: Target sums for each column.

    Returns:
        Dictionary with:
            - status: "solved" | "no_solution" | "timeout"
            - solution: 2D list of 0/1 values or None
            - nodes_visited: number of explored nodes
            - time_elapsed: runtime in seconds
    """
    if len(row_targets) != len(col_targets):
        raise ValueError("Row and column target lists must be of the same length.")
    
    n = len(row_targets)

    grid = [[0 for _ in range(n)] for _ in range(n)]
    row_sums = [0] * n
    col_sums = [0] * n

    nodes_visited = 0
    start_time = time.time()
    TIMEOUT = 60  # seconds

    def dfs(cell_index: int) -> str | bool:
        """
        Recursive DFS over grid cells with timeout.

        Returns:
            True if solution found
            "timeout" if timeout reached
            False if no solution in this branch
        """
        nonlocal nodes_visited
        nodes_visited += 1

        # Check timeout
        if time.time() - start_time > TIMEOUT:
            return "timeout"

        # All cells assigned
        if cell_index == n * n:
            return row_sums == row_targets and col_sums == col_targets

        row = cell_index // n
        col = cell_index % n

        # Try value 0 (unshaded)
        result = dfs(cell_index + 1)
        if result == "timeout" or result is True:
            return result

        # Try value 1 (shaded)
        row_value = col + 1
        col_value = row + 1

        # Apply shading
        grid[row][col] = 1
        row_sums[row] += row_value
        col_sums[col] += col_value

        # Prune if sums exceed targets
        if row_sums[row] <= row_targets[row] and col_sums[col] <= col_targets[col]:
            result = dfs(cell_index + 1)
            if result == "timeout" or result is True:
                return result

        # Backtrack
        grid[row][col] = 0
        row_sums[row] -= row_value
        col_sums[col] -= col_value

        return False

    solved = dfs(0)
    time_elapsed = time.time() - start_time

    if solved == "timeout":
        return {
            "status": "timeout",
            "solution": None,
            "nodes_visited": nodes_visited,
            "time_elapsed": time_elapsed,
        }

    if solved:
        return {
            "status": "solved",
            "solution": grid,
            "nodes_visited": nodes_visited,
            "time_elapsed": time_elapsed,
        }

    return {
        "status": "no_solution",
        "solution": None,
        "nodes_visited": nodes_visited,
        "time_elapsed": time_elapsed,
    }