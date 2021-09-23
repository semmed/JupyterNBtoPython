## This converts one or more Jupyter Notebooks to Python scripts
# This could be expanded to have a GIThub browser and all the works.
# At the moment the user is expected to retrieve the Notebooks and then
# convert them locally.
#
# Semme J. Dijkstra         9/23/2021

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

import nbformat

if __name__ == '__main__':

    # Create a GUI named root
    root = tk.Tk()

    # Hide the GUI from view
    root.withdraw()

    # Get the file names from a file dialog
    ipynb_file_names = filedialog.askopenfilenames(filetypes=(("Jupyter Notebooks", "*.ipynb"), ("All files", "*.*")))

    # Loop though all the selected files
    for f in ipynb_file_names:
        # We already know that the notebook exists as we used the file dialog to open it
        # Read the notebook keeping the structure
        notebook_file = open(f, 'r')
        notebook_content = nbformat.read(notebook_file, nbformat.NO_CONVERT)
        notebook_file.close()

        # Create a list for the lines of code
        code_lines = []

        # The contents of the notebook are now contained in a list called 'cells'
        # Some of these are code cells, others Markdown cells, heading cells, etc.
        for cells in notebook_content.cells:
            # We only care about the code cells
            if not cells.cell_type == 'code':
                continue
            # Now split the cell source code in lines
            # We want to keep this a one dimensional list, use the + operator
            code_lines += cells.source.splitlines()

        # the output file name should be the same, the extension should be replaced
        base, _ = os.path.splitext(f)
        py_file_name = base + ".py"

        # Open the output file for writing - but only if it does not already exists
        if Path(py_file_name).exists():
            # Warn the user
            warning = "A file by the name " + py_file_name + "exists, please select another filename"
            messagebox.showwarning(title=None, message=warning)
            # Allow the user to enter a different file name (the user may opt to use the same and will receive another
            # warning
            py_file_name = filedialog.asksaveasfilename(filetypes=[("Jupyter Notebooks", "*.py")],
                                                        initialfile=py_file_name,
                                                        defaultextension='.py')

        py_file = open(py_file_name, 'w')
        for code_line in code_lines:
            if '%load_ext autoreload' in code_line:
                continue
            if '%autoreload 2' in code_line:
                continue
            if '%matplotlib inline' in code_line:
                continue
            py_file.write(code_line + '\n')
        py_file.close()
