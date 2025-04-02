import tkinter as tk

class ExpandableGrid:
    def __init__(self, master, rows, columns):
        self.master = master
        self.rows = rows
        self.columns = columns

        # Configure the grid rows and columns to expand with the window
        for row in range(rows):
            self.master.grid_rowconfigure(row, weight=1, uniform="expand")
        for col in range(columns):
            self.master.grid_columnconfigure(col, weight=1, uniform="expand")

    def add_widget(self, widget, row, column, rowspan=1, columnspan=1, sticky="nsew"):
        widget.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)

# Create the main Tkinter window
root = tk.Tk()

# Create an ExpandableGrid with 2 rows and 2 columns
grid = ExpandableGrid(root, 2, 2)

# Create buttons and add them to the expandable grid
grid.add_widget(tk.Button(root, text="double test"), 0, 0, columnspan=2)
grid.add_widget(tk.Button(root, text="test"), 1, 0)
grid.add_widget(tk.Button(root, text="test"), 1, 1)

root.mainloop()
