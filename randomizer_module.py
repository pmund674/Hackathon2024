import tkinter as tk
from tkinter import messagebox
import random

class RandomizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Randomizer")

        # Input label
        self.label = tk.Label(root, text="Enter options (comma-separated):")
        self.label.pack(pady=10)

        # Input text box
        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=10)

        # Randomize button
        self.randomize_button = tk.Button(root, text="Randomize", command=self.randomize)
        self.randomize_button.pack(pady=10)

        # Result label
        self.result_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.result_label.pack(pady=10)

    def randomize(self):
        options = self.entry.get().strip().split(',')
        options = [option.strip() for option in options if option.strip()]
        
        if options:
            choice = random.choice(options)
            self.result_label.config(text=f"Random choice: {choice}")
        else:
            messagebox.showwarning("Warning", "Please enter at least one option.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomizerApp(root)
    root.mainloop()
