import os
from ac3 import solve_with_ac3
from timeout_util import run_with_timeout


def test_ac3_solver_no_solution():

    print("Testing AC-3 solver with no solution case.")

    row_targets = [0, 7, 5, 6, 4]
    col_targets = [16, 6, 4, 7, 3]

    result = solve_with_ac3(row_targets, col_targets)

    assert result["status"] == "no_solution", "Expected no solution"
    assert result["solution"] is None, "Expected solution to be None"


def test_ac3_solver_solved():

    print("Testing AC-3 solver with a solvable case.")

    row_targets = [1, 15, 2, 4, 7]
    col_targets = [3, 5, 7, 11, 2]

    result = solve_with_ac3(row_targets, col_targets)

    assert result["status"] == "solved", "Expected solved status"
    assert result["solution"] is not None, "Expected a solution grid"


def test_ac3_solver_timeout_or_hard_case():

    print("Testing AC-3 solver with a heavy case.")

    row_targets = [45, 44, 43, 42, 41, 40, 39, 38, 37]
    col_targets = [45, 44, 43, 42, 41, 40, 39, 38, 37]

    result = solve_with_ac3(row_targets, col_targets)

    # AC-3 may detect inconsistency early instead of timing out
    assert result["status"] in ["timeout", "no_solution"], \
        "Expected timeout or no_solution status"


def test_ac3_solver_edge_case():

    print("Testing AC-3 solver with edge case of all zero targets.")

    row_targets = [0, 0, 0, 0, 0]
    col_targets = [0, 0, 0, 0, 0]

    result = solve_with_ac3(row_targets, col_targets)

    assert result["status"] == "solved", "Expected solved status"
    assert result["solution"] is not None, "Expected a valid empty solution"


def test_ac3_solver_exception():

    print("Testing AC-3 solver with mismatched row and column lengths.")

    row_targets = [3, 7, 5]
    col_targets = [5, 6, 4, 7]

    try:
        solve_with_ac3(row_targets, col_targets)
        assert False, "Expected ValueError due to mismatched lengths"
    except ValueError as e:
        assert "length" in str(e)


print("Running AC-3 solver tests...")
print("=" * 60)

test_ac3_solver_solved()
test_ac3_solver_no_solution()

try:
    run_with_timeout(test_ac3_solver_timeout_or_hard_case, timeout=3)
except TimeoutError:
    print("Timeout test passed.")

test_ac3_solver_edge_case()
test_ac3_solver_exception()

print("=" * 60)

os.abort()