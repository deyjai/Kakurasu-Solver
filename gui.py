# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 18:49:52 2026

@author: jaide
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import solver
import ac3

class KakurasuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kakurasu Puzzle Loader")

        self.row_targets = []
        self.col_targets = []
        self.N = 0
        self.grid_labels = []

        # top buttons
        top = tk.Frame(root)
        top.pack(pady=10)

        self.load_button = tk.Button(top, text="Load Puzzle", command=self.load_puzzle)
        self.load_button.grid(row=0, column=0, padx=5)

        self.solve_button = tk.Button(top, text="Solve (Backtracking)", state=tk.DISABLED, command=self.solve_puzzle)
        self.solve_button.grid(row=0, column=1, padx=5)
        
        self.solve_ac3_button = tk.Button(
            top,
            text="Solve (AC-3)",
            state=tk.DISABLED,
            command=self.solve_puzzle_ac3
            )
        self.solve_ac3_button.grid(row=0, column=2, padx=5)

        self.status_label = tk.Label(top, text="No puzzle loaded")
        self.status_label.grid(row=1, column=0, columnspan=2, pady=5)

        # frame
        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack(pady=10)


    def load_puzzle(self):
        
        # select file
        filepath = filedialog.askopenfilename(
            title="Select Kakurasu puzzle file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return


        # validate file
        try:
            with open(filepath, "r") as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")
            return

        if len(lines) != 3:
            messagebox.showerror("Error", "File must contain exactly three lines:\nN\nRow targets\nColumn targets")
            return
        try:
            N = int(lines[0])
            row_targets = [int(x) for x in lines[1].split(",")]
            col_targets = [int(x) for x in lines[2].split(",")]
        except ValueError:
            messagebox.showerror("Error", "Invalid format. Ensure N and all targets are integers.")
            return
        if len(row_targets) != N or len(col_targets) != N:
            messagebox.showerror("Error", "Number of row/column targets must match N.")
            return
        
        
        # initialize grid
        self.row_targets = row_targets
        self.col_targets = col_targets
        self.N = len(row_targets)

        self.status_label.config(text=f"Loaded {self.N}×{self.N} puzzle")
        self.solve_button.config(state=tk.NORMAL)
        self.solve_ac3_button.config(state=tk.NORMAL)

        self.draw_grid()


    def clear_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

    def draw_grid(self):
        self.clear_grid()

        if self.N == 0:
            return

        # initialize null value (to leave the top left corner empty)
        tk.Label(self.grid_frame, text="").grid(row=0, column=0, padx=5, pady=5)

        # initialize columns
        for j in range(self.N):
            tk.Label(self.grid_frame, text=str(self.col_targets[j]), font=("Arial", 10, "bold")).grid(
                row=0, column=j + 1, padx=5, pady=5
            )

        # initialize rows and empty cells
        self.grid_labels = []
        for i in range(self.N):
            tk.Label(self.grid_frame, text=str(self.row_targets[i]), font=("Arial", 10, "bold")).grid(
                row=i + 1, column=0, padx=5, pady=5
            )

            row_labels = []
            for j in range(self.N):
                lbl = tk.Label(self.grid_frame, text="", width=3, height=1, relief="solid", bg="white")
                lbl.grid(row=i + 1, column=j + 1, padx=1, pady=1)
                row_labels.append(lbl)

            self.grid_labels.append(row_labels)

    def solve_puzzle(self):
        """Call the backtracking solver and display results in the GUI."""
        if self.N == 0:
            return

        # Run solver
        result = solver.solve_kakurasu_backtracking(self.row_targets, self.col_targets)

        status = result.get("status")
        nodes = result.get("nodes_visited", 0)
        runtime = result.get("time_elapsed", 0)

        if status == "solved":
            sol = result.get("solution")
            # Update grid display: shaded cells -> black, unshaded -> white
            for i in range(self.N):
                for j in range(self.N):
                    if sol and sol[i][j] == 1:
                        self.grid_labels[i][j].config(bg="black", text="")
                    else:
                        self.grid_labels[i][j].config(bg="white", text="")

            self.status_label.config(
                text=f"Solved — nodes: {nodes} | time: {runtime:.4f}s"
                )
            messagebox.showinfo(
                "Solved",
                f"Solution found.\nNodes visited: {nodes}\nRuntime: {runtime:.4f} seconds"
            )
        elif status == "timeout":
            self.status_label.config(text=f"Timeout — nodes visited: {nodes}")
            messagebox.showwarning("Timeout", f"Solver timed out after 60 seconds.\nNodes visited: {nodes}")
        else:
            self.status_label.config(text=f"No solution — nodes visited: {nodes}")
            messagebox.showwarning("No solution", f"No solution found.\nNodes visited: {nodes}")

    def solve_puzzle_ac3(self):
        """Call the AC-3 solver and display results in the GUI."""
        if self.N == 0:
            return
    
        result = ac3.solve_with_ac3(
            self.row_targets,
            self.col_targets
        )
    
        status = result.get("status")
        nodes = result.get("nodes_visited", 0)
        runtime = result.get("time_elapsed", 0)
    
        if status == "solved":
            sol = result.get("solution")
    
            for i in range(self.N):
                for j in range(self.N):
                    if sol and sol[i][j] == 1:
                        self.grid_labels[i][j].config(bg="black", text="")
                    else:
                        self.grid_labels[i][j].config(bg="white", text="")
    
            self.status_label.config(
                text=f"Solved — nodes: {nodes} | time: {runtime:.4f}s"
                )
            messagebox.showinfo(
                "Solved",
                f"Solution found.\nNodes visited: {nodes}\nRuntime: {runtime:.4f} seconds"
            )
    
        elif status == "timeout":
            self.status_label.config(text=f"Timeout (AC-3) — nodes visited: {nodes}")
            messagebox.showwarning("Timeout", f"AC-3 solver timed out.\nNodes visited: {nodes}")
    
        else:
            self.status_label.config(text=f"No solution (AC-3) — nodes visited: {nodes}")
            messagebox.showwarning("No solution", f"AC-3 found no solution.\nNodes visited: {nodes}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KakurasuGUI(root)
    root.mainloop()