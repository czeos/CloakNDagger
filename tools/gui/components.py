import tkinter as tk
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit,
                             QPushButton, QApplication, QHBoxLayout, QSpinBox,
                             QDoubleSpinBox, QCheckBox, QDateEdit, QDateTimeEdit)
from PyQt6.QtCore import pyqtSlot
from pydantic import BaseModel
from typing import Literal, get_args, get_origin
from datetime import date, datetime
import sys

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


class MessageBox(QWidget):
    def __init__(self, message, title, description):
        super().__init__()
        self.initUI(message, title, description)

    def initUI(self, message, title, description):
        layout = QVBoxLayout()

        # Set window title
        self.setWindowTitle(title)

        # Add message label
        message_label = QLabel(message, self)
        layout.addWidget(message_label)

        # Add description label
        description_label = QLabel(description, self)
        layout.addWidget(description_label)

        # Add submit button
        submit_button = QPushButton('OK', self)
        submit_button.clicked.connect(self.onSubmit)
        layout.addWidget(submit_button)

        self.setLayout(layout)
        self.show()

    @pyqtSlot()
    def onSubmit(self):
        self.close()


def message_box(message, title, description):
    app = QApplication(sys.argv)
    ex = MessageBox(message, title, description)
    ex.show()
    app.exec()


class DynamicFormApp(QWidget):
    """
    Dynamic form app to generate input fields based on Pydantic class attributes.
    """
    def __init__(self, model_class, title, description):
        super().__init__()
        self.model_class = model_class
        self.title = title
        self.description = description
        self.available_attributes = list(model_class.__annotations__.keys())  # Pydantic attributes
        self.form_rows = []
        self.result = None  # Default result to avoid AttributeError if closed without submission
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.layout = QVBoxLayout()

        # Add title and description
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout.addWidget(title_label)

        description_label = QLabel(self.description)
        self.layout.addWidget(description_label)

        # Add the option menu and '+' button
        self.add_selector_layout = QHBoxLayout()
        self.option_menu = QComboBox(self)
        self.option_menu.addItems(self.available_attributes)
        self.add_selector_layout.addWidget(self.option_menu)

        add_button = QPushButton('+', self)
        add_button.clicked.connect(self.addFormRow)
        self.add_selector_layout.addWidget(add_button)
        self.layout.addLayout(self.add_selector_layout)

        # Layout for form rows (dynamic rows)
        self.rows_layout = QVBoxLayout()
        self.layout.addLayout(self.rows_layout)

        # Add Submit button
        submit_button = QPushButton('Submit', self)
        submit_button.clicked.connect(self.onSubmit)
        self.layout.addWidget(submit_button)

        # Set main layout
        self.setLayout(self.layout)
        self.show()

    def addFormRow(self):
        """ Add a new form row with attribute name, input field, and 'x' button """
        selected_option = self.option_menu.currentText()
        if selected_option not in self.available_attributes:
            return  # Do nothing if there's no valid selection

        # Get the attribute type from the Pydantic class
        attr_type = self.model_class.__annotations__[selected_option]

        # Create a new horizontal layout for the row
        row_layout = QHBoxLayout()

        # Display the selected attribute
        attribute_label = QLabel(selected_option, self)
        row_layout.addWidget(attribute_label)

        # Create input widget based on the attribute type
        input_widget = self.createInputField(attr_type)
        row_layout.addWidget(input_widget)

        # Create "Remove" button ('x')
        remove_button = QPushButton('x', self)
        remove_button.clicked.connect(lambda: self.removeFormRow(row_layout, selected_option))
        row_layout.addWidget(remove_button)

        # Add this row layout to the main layout
        self.rows_layout.addLayout(row_layout)
        self.form_rows.append((selected_option, input_widget, row_layout))

        # Remove the selected option from the dropdown and update
        self.available_attributes.remove(selected_option)
        self.updateOptions()

    def createInputField(self, attr_type):
        """ Create appropriate input field based on the attribute type """
        origin = get_origin(attr_type)
        if origin == Literal:  # If it's a Literal, create a dropdown
            options = get_args(attr_type)
            combo_box = QComboBox(self)
            combo_box.addItems(map(str, options))  # Add the literal options
            return combo_box

        # Handle common types
        if attr_type == str:
            return QLineEdit(self)
        elif attr_type == int:
            spin_box = QSpinBox(self)
            spin_box.setMaximum(1000000)  # Set a sensible maximum for integers
            return spin_box
        elif attr_type == float:
            double_spin_box = QDoubleSpinBox(self)
            double_spin_box.setDecimals(2)  # Allow two decimal places
            return double_spin_box
        elif attr_type == bool:
            return QCheckBox(self)
        elif attr_type == date:
            return QDateEdit(self)
        elif attr_type == datetime:
            return QDateTimeEdit(self)

        # Fallback to text input if type is not recognized
        return QLineEdit(self)

    def removeFormRow(self, row_layout, attribute_name):
        """ Remove a row and return the attribute to the dropdown """
        for selected_option, input_field, layout in self.form_rows:
            if layout == row_layout:
                self.form_rows.remove((selected_option, input_field, layout))
                # Make sure to delete all widgets safely
                self.delete_widgets(layout)
                self.rows_layout.removeItem(layout)

        # Add the removed attribute back to the dropdown options
        self.available_attributes.append(attribute_name)
        self.updateOptions()

    def delete_widgets(self, layout):
        """ Safely delete all widgets from the layout """
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def updateOptions(self):
        """ Update the available options in the dropdown menu """
        # Safely disconnect signals before updating to avoid recursive call
        self.option_menu.blockSignals(True)
        self.option_menu.clear()
        self.option_menu.addItems(self.available_attributes)
        self.option_menu.blockSignals(False)

    @pyqtSlot()
    def onSubmit(self):
        """ Handle form submission """
        form_data = {}
        for selected_option, input_widget, _ in self.form_rows:
            # Extract the value from the appropriate widget
            if isinstance(input_widget, QLineEdit):
                form_data[selected_option] = input_widget.text() if input_widget.text() else None
            elif isinstance(input_widget, QSpinBox):
                form_data[selected_option] = input_widget.value()
            elif isinstance(input_widget, QDoubleSpinBox):
                form_data[selected_option] = input_widget.value()
            elif isinstance(input_widget, QComboBox):
                form_data[selected_option] = input_widget.currentText()
            elif isinstance(input_widget, QCheckBox):
                form_data[selected_option] = input_widget.isChecked()
            elif isinstance(input_widget, QDateEdit):
                form_data[selected_option] = input_widget.date().toPyDate()
            elif isinstance(input_widget, QDateTimeEdit):
                form_data[selected_option] = input_widget.dateTime().toPyDateTime()

        # Create Pydantic class instance with form data
        try:
            model_instance = self.model_class(**form_data)
            self.result = model_instance
        except Exception as e:
            print(f"Error creating Pydantic instance: {e}")
            self.result = None

        # Close the window
        self.close()

    def getResult(self):
        return self.result


def open_dynamic_form(model_class, title, description):
    app = QApplication(sys.argv)
    form = DynamicFormApp(model_class, title, description)
    form.show()
    app.exec()
    return form.getResult()


# Example Pydantic class with various types
class PersonModel(BaseModel):
    name: str = None
    age: int = None
    salary: float = None
    birthdate: date = None
    last_logged_in: datetime = None
    is_employee: bool = None
    gender: Literal['Male', 'Female', 'Other'] = None  # Literal will be a dropdown


if __name__ == "__main__":
    # Test case
    title = "Person Form"
    description = "Fill out the details below. You can add or remove fields dynamically."
    result = open_dynamic_form(PersonModel, title, description)
    if result:
        print(result)
    else:
        print("Form was closed or no data was submitted.")
