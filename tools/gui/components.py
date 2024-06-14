import tkinter as tk


class SelectorMenu:
    """
    A context manager for creating a Tkinter main window with a dropdown menu and a submit button.

    Example usage:
    --------------
    default_option = "Option 1"
    options = ["Option 1", "Option 2", "Option 3"]
    label_text = "Please select an option:"

    with SelectorMenu(default_option, options, label_text) as app:
        app.root.mainloop()
        selected_option = app.get_selected_value()

    print(f"Selected option: {selected_option}")
    """

    def __init__(self, default_option, options, label):
        self.default_option = default_option
        self.options = options
        self.label_text = label
        self.selected_value = None

    def __enter__(self):
        self.root = tk.Tk()
        self.root.title("SelectorMenu")
        self.root.geometry("300x200")

        self.selected_value = tk.StringVar()
        self.selected_value.set(self.default_option)  # Set default value

        self.label = tk.Label(self.root, text=self.label_text)
        self.label.pack(pady=10)

        self.dropdown = tk.OptionMenu(self.root, self.selected_value, *self.options)
        self.dropdown.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        return self

    def on_submit(self):
        self.result_label.config(text=f"Selected option: {self.selected_value.get()}")
        self.root.quit()

    def __exit__(self, exc_type, exc_value, traceback):
        self.root.destroy()

    def get_selected_value(self):
        return self.selected_value.get()


class MultiCheckboxMenu:
    """
    A context manager for creating a Tkinter main window with a multi-select menu and a submit button.

    Example usage:
    --------------
    options = ["Option 1", "Option 2", "Option 3"]
    label_text = "Please select options:"

    with SelectorMenu(options, label_text) as app:
        app.root.mainloop()
        selected_options = app.get_selected_values()

    print(f"Selected options: {selected_options}")
    """

    def __init__(self, options, label):
        self.options = options
        self.label_text = label
        self.selected_values = []

    def __enter__(self):
        self.root = tk.Tk()
        self.root.title("MultiSelectorMenu")

        self.label = tk.Label(self.root, text=self.label_text)
        self.label.pack(pady=10)

        self.check_vars = []
        self.checkbuttons = []
        for option in self.options:
            var = tk.IntVar()
            self.check_vars.append(var)
            checkbutton = tk.Checkbutton(self.root, text=option, variable=var)
            checkbutton.pack(anchor='w')
            self.checkbuttons.append(checkbutton)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)
        self.root.pack_propagate(True)

        return self

    def on_submit(self):
        self.selected_values = [option for option, var in zip(self.options, self.check_vars) if var.get() == 1]
        self.result_label.config(text=f"Selected options: {', '.join(self.selected_values)}")
        self.root.quit()

    def __exit__(self, exc_type, exc_value, traceback):
        self.root.destroy()

    def get_selected_values(self):
        return self.selected_values


class MultiSelectorMenu:
    """
    A context manager for creating a Tkinter main window with a multi-select menu and a submit button.

    Example usage:
    --------------
    options = ["Option 1", "Option 2", "Option 3"]
    label_text = "Please select options:"

    with MultiSelectorMenu(options, label_text) as app:
        app.root.mainloop()
        selected_options = app.get_selected_values()

    print(f"Selected options: {selected_options}")
    """

    def __init__(self, options, label):
        self.options = options
        self.label_text = label
        self.selected_values = []

    def __enter__(self):
        self.root = tk.Tk()
        self.root.title("MultiSelectorMenu")

        self.label = tk.Label(self.root, text=self.label_text)
        self.label.pack(pady=10)

        self.listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE)
        for option in self.options:
            self.listbox.insert(tk.END, option)
        self.listbox.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.on_submit)
        self.submit_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        self.root.pack_propagate(True)

        return self

    def on_submit(self):
        selected_indices = self.listbox.curselection()
        self.selected_values = [self.options[i] for i in selected_indices]
        self.result_label.config(text=f"Selected options: {', '.join(self.selected_values)}")
        self.root.quit()

    def __exit__(self, exc_type, exc_value, traceback):
        self.root.destroy()

    def get_selected_values(self):
        return self.selected_values

if __name__ == '__main__':
    default_option, options, label = 'options1', ['option1', 'options2', 'option3'] , 'Test widget'

    with MultiSelectorMenu(options=options, label=label ) as app:
        app.root.mainloop()
        selected_option = app.get_selected_values()
        pass