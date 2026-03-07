import os
import csv
from backtracking_solver import solve_kakurasu_backtracking
from ac3_solver import solve_with_ac3

# Folder with puzzle files
PUZZLE_DIR = "puzzles"  # put your .txt puzzles here
OUTPUT_CSV = "experimental_results.csv"

# Read puzzle file (expects your 3-line format)
def read_puzzle(filepath):
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    n = int(lines[0])
    row_targets = [int(x) for x in lines[1].split(",")]
    col_targets = [int(x) for x in lines[2].split(",")]
    return n, row_targets, col_targets

# Prepare CSV
with open(OUTPUT_CSV, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Puzzle ID", "Grid Size", "Solver", "Status", "Runtime (s)", "Nodes Visited"])

    for puzzle_file in sorted(os.listdir(PUZZLE_DIR)):
        if not puzzle_file.endswith(".txt"):
            continue
        puzzle_id = os.path.splitext(puzzle_file)[0]
        n, row_targets, col_targets = read_puzzle(os.path.join(PUZZLE_DIR, puzzle_file))
        grid_size = f"{n}x{n}"

        # Run Backtracking
        result_bt = solve_kakurasu_backtracking(row_targets, col_targets)
        writer.writerow([
            puzzle_id,
            grid_size,
            "Backtracking",
            result_bt["status"],
            f"{result_bt['time_elapsed']:.4f}",
            result_bt["nodes_visited"]
        ])

        # Run AC-3
        result_ac3 = solve_with_ac3(row_targets, col_targets)
        writer.writerow([
            puzzle_id,
            grid_size,
            "AC-3",
            result_ac3["status"],
            f"{result_ac3['time_elapsed']:.4f}",
            result_ac3["nodes_visited"]
        ])

print(f"Results saved to {OUTPUT_CSV}")