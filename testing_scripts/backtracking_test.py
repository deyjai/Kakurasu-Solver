import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backtracking_solver  import solve_kakurasu_backtracking
from timeout_util import run_with_timeout

def test_backtracking_solver_no_solution():

    # Test case 1: Simple 5x5 puzzle with no solution
    # Check row 0 and column 0 weights that cannot be satisfied together
    print("Testing backtracking solver with no solution case.")
    row_targets = [0, 7, 5, 6, 4]
    col_targets = [16, 6, 4, 7, 3]
    result = solve_kakurasu_backtracking(row_targets, col_targets)  
    assert result["status"] == "no_solution", "Expected no solution"
    assert result["solution"] is None, "Expected solution to be None"   

def test_backtracking_solver_solved():

    # Test case 2: Simple 5x5 puzzle with a solution
    print("Testing backtracking solver with a solvable case.")
    row_targets = [1, 15, 2, 4, 7]
    col_targets = [3, 5, 7, 11, 2]
    result = solve_kakurasu_backtracking(row_targets, col_targets)
    assert result["status"] == "solved", "Expected solved status"
    assert result["solution"] is not None, "Expected a solution grid"

def test_backtracking_solver_timeout():

    # Test case 3: Larger 9x9 puzzle that may cause timeout
    print("Testing backtracking solver with a potentially unsolvable case to trigger timeout.")
    row_targets = [45, 44, 43, 42, 41, 40, 39, 38, 37]
    col_targets = [45, 44, 43, 42, 41, 40, 39, 38, 37]
    result = solve_kakurasu_backtracking(row_targets, col_targets)  
    assert result["status"] == "timeout", "Expected timeout status"

def test_backtracking_solver_edge_case():
    # all weights are zero, should be solved with all cells not selected
    print("Testing backtracking solver with edge case of all zero targets.")
    row_targets = [0, 0, 0, 0, 0]
    col_targets = [0, 0, 0, 0, 0]
    result = solve_kakurasu_backtracking(row_targets, col_targets)  
    assert result["status"] == "solved", "Expected solved status"

def test_backtracking_solver_exception():
    # Test case 4: Mismatched row and column lengths should raise ValueError
    print("Testing backtracking solver with mismatched row and column lengths to trigger exception.")
    row_targets = [3, 7, 5]
    col_targets = [5, 6, 4, 7]
    try:
        solve_kakurasu_backtracking(row_targets, col_targets)
        assert False, "Expected ValueError due to mismatched lengths"
    except ValueError as e:
        assert str(e) == "Row and column target lists must be of the same length.", "Unexpected error message"


print("Running backtracking solver tests...")
print("="*60)
test_backtracking_solver_solved()
test_backtracking_solver_no_solution()
try:
    run_with_timeout(test_backtracking_solver_timeout, timeout=3)
except TimeoutError:
    print("Timeout test passed.")
test_backtracking_solver_edge_case()
test_backtracking_solver_exception()
print("="*60)  
os.abort()
