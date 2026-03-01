# -*- coding: utf-8 -*-
"""
Backtracking (DFS) solver for Kakurasu.

This implementation:
- Uses depth-first search
- Applies early pruning
- Counts visited nodes
- Returns structured result dictionary
"""
from __future__ import annotations
from typing import List


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
            - status: "solved" | "no_solution"
            - solution: 2D list of 0/1 values or None
            - nodes_visited: number of explored nodes
    """
    n = len(row_targets)

    grid = [[0 for _ in range(n)] for _ in range(n)]
    row_sums = [0] * n
    col_sums = [0] * n

    nodes_visited = 0

    def dfs(cell_index: int) -> bool:
        """
        Recursive DFS over grid cells.

        Args:
            cell_index: flattened index from 0 to n*n - 1

        Returns:
            True if solution found, False otherwise.
        """
        nonlocal nodes_visited
        nodes_visited += 1

        # All cells assigned
        if cell_index == n * n:
            return (
                row_sums == row_targets and
                col_sums == col_targets
            )

        row = cell_index // n
        col = cell_index % n

        # Try value 0 (unshaded)
        if dfs(cell_index + 1):
            return True

        # Try value 1 (shaded)
        row_value = col + 1
        col_value = row + 1

        # Apply shading
        grid[row][col] = 1
        row_sums[row] += row_value
        col_sums[col] += col_value

        # Prune if sums exceed targets
        if (
            row_sums[row] <= row_targets[row]
            and col_sums[col] <= col_targets[col]
        ):
            if dfs(cell_index + 1):
                return True

        # Backtrack
        grid[row][col] = 0
        row_sums[row] -= row_value
        col_sums[col] -= col_value

        return False

    solved = dfs(0)

    if solved:
        return {
            "status": "solved",
            "solution": grid,
            "nodes_visited": nodes_visited,
        }

    return {
        "status": "no_solution",
        "solution": None,
        "nodes_visited": nodes_visited,
    }
