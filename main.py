import tkinter as tk

class ExpandableGrid:
    def __init__(self, master: tk.Tk | tk.Toplevel, rows: int, columns: int):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.widgets: list[tk.Widget] = []

        # Configure the grid rows and columns to expand with the window
        for row in range(rows):
            self.master.grid_rowconfigure(row, weight=1, uniform="expand")
        for col in range(columns):
            self.master.grid_columnconfigure(col, weight=1, uniform="expand")

    def add_widget(self, widget: tk.Widget, row: int, column: int, rowspan: int = 1, columnspan: int = 1, sticky: str = "nsew"):
        self.widgets.append(widget)
        widget.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)

    def remove_widgets(self):
        # Destroy all widgets in the grid
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()


def gameloop(root: tk.Tk | tk.Toplevel, word_list: list[tuple[str, int]], word_index: int = 0):
    grid = ExpandableGrid(root, 3, 5)  # Adjusted for displaying the current word and buttons
    
    # Clear the previous widgets
    grid.remove_widgets()

    # Get the current word and correct answer
    word, correct_answer = word_list[word_index]

    # Label showing the word
    grid.add_widget(tk.Label(root, text=word, font=("Arial", 20)), 0, 0, columnspan=5)

    # Function to handle button clicks
    def check_answer(selected_answer: int):
        if selected_answer == correct_answer:
            result_label.config(text=f"Correct! The answer is {correct_answer}.", fg="green")
        else:
            result_label.config(text=f"Incorrect. The correct answer was {correct_answer}.", fg="red")

    # Add buttons for each possible answer (for example: 1, 2, 3, 4)
    for i in range(1, 5):
        grid.add_widget(tk.Button(root, text=f"Answer {i}", command=lambda i=i: check_answer(i)), 1, i - 1)

    # Result label (shows if answer is correct or incorrect)
    result_label = tk.Label(root, text="", font=("Arial", 14))
    grid.add_widget(result_label, 2, 0, columnspan=5)

    # Add a "Next" button to go to the next word
    if word_index + 1 < len(word_list):
        next_button = tk.Button(root, text="Next", command=lambda: gameloop(root, word_list, word_index + 1))
        next_button.grid(row=3, column=0, columnspan=5)

# Create the main Tkinter window
root = tk.Tk()

# List of tuples where the first value is the word and the second value is the correct answer (1-4 for example)
word_list = [(str(i), i % 6) for i in range(1, 21)]

# Run the game loop to show the first word
gameloop(root, word_list)

# Start the Tkinter event loop
root.mainloop()
