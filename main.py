import tkinter as tk
from tkinter import ttk

class ExpandableGrid:
    def __init__(self, master: tk.Tk | tk.Toplevel, rows: int, columns: int):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.widgets: list[tk.Widget] = []

        for row in range(rows):
            self.master.grid_rowconfigure(row, weight=1, uniform="expand")
        for col in range(columns):
            self.master.grid_columnconfigure(col, weight=1, uniform="expand")

    def add_widget(self, widget: tk.Widget, row: int, column: int, rowspan: int = 1, columnspan: int = 1, sticky: str = "nsew"):
        self.widgets.append(widget)
        widget.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)

    def remove_widgets(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets.clear()

# Finnish locative forms
locative_forms = [
    "Nominatiivi",
    "Genetiivi",
    "Partitiivi",
    "Essiivi",
    "Translatiivi",
    "Paikallissija"
]

# Global word list
quiz_words: list[tuple[str, int]] = []

def show_create_quiz(root: tk.Tk):
    grid = ExpandableGrid(root, 5, 4)
    grid.remove_widgets()

    grid.add_widget(tk.Label(root, text="Sanojen lisääminen tietovisaan", font=("Arial", 20)), 0, 0, columnspan=4)

    grid.add_widget(tk.Label(root, text="Sana:"), 1, 0)
    word_entry = tk.Entry(root)
    grid.add_widget(word_entry, 1, 1, columnspan=3)

    grid.add_widget(tk.Label(root, text="Oikea sijamuoto:"), 2, 0)
    form_var = tk.StringVar(value=locative_forms[0])
    form_dropdown = ttk.Combobox(root, textvariable=form_var, values=locative_forms, state="readonly")
    grid.add_widget(form_dropdown, 2, 1, columnspan=3)

    added_label = tk.Label(root, text="", fg="green")
    grid.add_widget(added_label, 3, 0, columnspan=4)

    def add_word():
        word = word_entry.get().strip()
        if not word:
            added_label.config(text="Kirjoita sana!", fg="red")
            return
        index = locative_forms.index(form_var.get()) + 1
        quiz_words.append((word, index))
        word_entry.delete(0, tk.END)
        added_label.config(text=f"Sana '{word}' lisätty!", fg="green")

    grid.add_widget(tk.Button(root, text="Lisää", command=add_word), 4, 0, columnspan=2)
    grid.add_widget(tk.Button(root, text="Aloita peli", command=lambda: gameloop(root, quiz_words)), 4, 2, columnspan=2)

def gameloop(root: tk.Tk, word_list: list[tuple[str, int]], word_index: int = 0):
    # Clear all widgets before starting the game
    for widget in root.winfo_children():
        widget.destroy()

    # If quiz is over, just show the final message
    if word_index >= len(word_list):
        final_label = tk.Label(root, text="Peli ohi! Hyvää työtä!", font=("Arial", 24), fg="blue")
        final_label.pack(expand=True)
        return

    # Use 4 rows: row0: word, row1: answer buttons, row2: result label, row3: "Seuraava" button
    grid = ExpandableGrid(root, 4, 6)
    
    # Remove row 3 from the uniform group so it sizes naturally
    root.grid_rowconfigure(3, weight=0, uniform="")

    word, correct_answer = word_list[word_index]
    grid.add_widget(tk.Label(root, text=word, font=("Arial", 20)), 0, 0, columnspan=6)

    result_label = tk.Label(root, text="", font=("Arial", 14))
    grid.add_widget(result_label, 2, 0, columnspan=6)

    def check_answer(selected_answer: int):
        if selected_answer == correct_answer:
            result_label.config(text=f"Oikein! Vastaus oli {locative_forms[correct_answer - 1]}.", fg="green")
        else:
            result_label.config(text=f"Väärin. Vastaus oli {locative_forms[correct_answer - 1]}.", fg="red")

    for i in range(6):
        grid.add_widget(
            tk.Button(root, text=locative_forms[i], command=lambda i=i: check_answer(i + 1)),
            1, i
        )

    # "Seuraava" button in row 3, which now sizes to its natural height
    grid.add_widget(
        tk.Button(root, text="Seuraava", command=lambda: gameloop(root, word_list, word_index + 1)),
        3, 0, rowspan=2, columnspan=6, sticky="nsew"
    )

# Main window
root = tk.Tk()
root.title("Sijamuotopeli")

show_create_quiz(root)

root.mainloop()
