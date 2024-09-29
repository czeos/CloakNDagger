import tkinter as tk
from tkinter import ttk
from typing import Dict

from pydantic import BaseModel, Field


class FormOutput(BaseModel):
    name: str | None = Field(default=None)
    ico: str | None = Field(default=None)
    sidlo: str | None = Field(default=None)


class InputForm:
    def __init__(self, window, params: Dict[str, str]):
        self.window = window
        self.entries = {}
        self.data = None
        labels = ['name','ico','adress']

        # Define styles for labels and entries
        style = ttk.Style()
        style.configure("TLabel", background="#30343F", foreground="#FFFFFF", font=("Arial", 12))
        style.configure("TButton", background="#808080", foreground="#000000", font=("Arial", 12))  # Change button color to grey
        style.configure("TEntry", fieldbackground="#FFFFFF", font=("Arial", 12))

        
        for i, label in enumerate(labels):
            ttk.Label(window, text=f"{label.capitalize()}:", style="TLabel").grid(row=i, column=0, padx=10, pady=5, sticky="E")
            self.entries[label] = ttk.Entry(window, width=20, style="TEntry",name=label)  # Change input field width to 20
            self.entries[label].grid(row=i, column=1, padx=10, pady=5)
            self.entries[label].insert(0, params[label] if label in params else "")

        
        button = ttk.Button(window, text="OK", command=self.on_button_click, style="TButton")  # Change button text to "OK"
        button.grid(row=len(labels), column=1, pady=20)

        window.grid_columnconfigure(1, weight=1)

    def on_button_click(self):
        self.data = FormOutput(name=self.entries["name"].get(), ico=self.entries["ico"].get(), sidlo=self.entries["adress"].get())
        self.window.destroy()

    def get_data(self):
        return self.data

def show_form(params: Dict[str, str]):
    window = tk.Tk()
    window.title("Input Form")
    window.configure(bg="#30343F")  # Set background color
    window.resizable(False, False)    # Get the cursor position
    x, y = window.winfo_pointerxy()

    # Set the initial position of the window
    window.geometry(f"+{x}+{y}")

    form = InputForm(window,params)
    window.mainloop()
    return form.get_data()

if __name__ == "__main__":
    print(show_form({'name': 'alza'}))