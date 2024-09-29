

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit,
                             QPushButton, QApplication, QHBoxLayout, QSpinBox,
                             QDoubleSpinBox, QCheckBox, QDateEdit, QDateTimeEdit, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import pyqtSlot
from pydantic import BaseModel, Field
from typing import Literal, get_args, get_origin
from datetime import date, datetime
import sys


class DynamicFormApp(QWidget):
    """
    Dynamic form app to generate input fields based on the attributes of a Pydantic class.

    Parameters:
    -----------
    model_class : Type[BaseModel]
        The Pydantic class that defines the attributes and their types.
    title : str
        The title of the form window.
    description : str
        The description displayed at the top of the form window.
    default_fields : list of str, optional
        A list of field names (attributes) to be rendered by default when the form is initialized.
    mode : str, optional
        If set to "all", all the fields defined in the Pydantic class will be rendered initially.
    init_values : dict, optional
        A dictionary of initial values for the form fields, where the keys are field names and the values are the initial data.
    """

    def __init__(self, model_class, title, description, default_fields=None, mode=None, init_values=None):
        super().__init__()
        self.model_class = model_class
        self.title = title
        self.description = description
        self.default_fields = default_fields or []
        self.mode = mode
        self.init_values = init_values or {}
        self.available_attributes = list(model_class.__fields__.keys())  # Pydantic attributes
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
        self.updateOptions()  # Populate the options initially
        self.add_selector_layout.addWidget(self.option_menu)

        self.add_button = QPushButton('+', self)
        self.add_button.clicked.connect(self.addFormRow)
        self.add_selector_layout.addWidget(self.add_button)
        self.layout.addLayout(self.add_selector_layout)

        # Layout for form rows (dynamic rows)
        self.rows_layout = QVBoxLayout()
        self.layout.addLayout(self.rows_layout)

        # Add Submit button
        submit_button = QPushButton('Submit', self)
        submit_button.clicked.connect(self.onSubmit)
        self.layout.addWidget(submit_button)

        # Render default fields or all fields if specified
        if self.mode == 'all':
            for field_name in self.available_attributes[:]:
                self.addFormRow(field_name)
        elif self.default_fields:
            for field_name in self.default_fields:
                self.addFormRow(field_name)

        # Set main layout
        self.setLayout(self.layout)
        self.show()

    def getFieldDescriptions(self):
        """ Returns the descriptions or field names if no description exists """
        descriptions = []
        for field_name, field_info in self.model_class.__fields__.items():
            if field_info.description:
                descriptions.append(field_info.description)
            else:
                descriptions.append(field_name)
        return descriptions

    def addFormRow(self, specific_field=None):
        """ Add a new form row with attribute name, input field, and 'x' button """
        if specific_field:
            selected_option = specific_field
        else:
            selected_option = self.getFieldNameFromDescription(self.option_menu.currentText())

        if selected_option not in self.available_attributes:
            return  # Do nothing if there's no valid selection

        # Get the attribute type from the Pydantic class
        attr_type = self.model_class.__annotations__[selected_option]
        field_info = self.model_class.__fields__[selected_option]

        # Create a new horizontal layout for the row
        row_layout = QHBoxLayout()

        # Display the selected attribute's description or name
        attribute_label = QLabel(field_info.description if field_info.description else selected_option, self)
        attribute_label.setFixedWidth(150)  # Ensures consistent label width
        row_layout.addWidget(attribute_label)

        # Add spacer to align the input fields
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        row_layout.addItem(spacer)

        # Create input widget based on the attribute type
        input_widget = self.createInputField(attr_type, selected_option)
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

        # Hide the add button and option menu if all fields are rendered
        if not self.available_attributes:
            self.option_menu.hide()
            self.add_button.hide()

    def getFieldNameFromDescription(self, description):
        """ Get the field name by matching the description or defaulting to name """
        for field_name, field_info in self.model_class.__fields__.items():
            if field_info.description == description or field_name == description:
                return field_name
        return description

    def createInputField(self, attr_type, field_name):
        """
        Create appropriate input field based on the attribute type,
        and pre-fill it if initial values are provided.
        """
        origin = get_origin(attr_type)
        initial_value = self.init_values.get(field_name)

        if origin == Literal:  # If it's a Literal, create a dropdown
            options = get_args(attr_type)
            combo_box = QComboBox(self)
            combo_box.addItems(map(str, options))  # Add the literal options
            if initial_value is not None:
                combo_box.setCurrentText(str(initial_value))
            return combo_box

        # Handle common types
        if attr_type == str:
            line_edit = QLineEdit(self)
            if initial_value is not None:
                line_edit.setText(str(initial_value))
            return line_edit
        elif attr_type == int:
            spin_box = QSpinBox(self)
            spin_box.setMaximum(1000000)  # Set a sensible maximum for integers
            if initial_value is not None:
                spin_box.setValue(int(initial_value))
            return spin_box
        elif attr_type == float:
            double_spin_box = QDoubleSpinBox(self)
            double_spin_box.setDecimals(2)  # Allow two decimal places
            if initial_value is not None:
                double_spin_box.setValue(float(initial_value))
            return double_spin_box
        elif attr_type == bool:
            check_box = QCheckBox(self)
            if initial_value is not None:
                check_box.setChecked(bool(initial_value))
            return check_box
        elif attr_type == date:
            date_edit = QDateEdit(self)
            if initial_value is not None:
                date_edit.setDate(initial_value)
            return date_edit
        elif attr_type == datetime:
            datetime_edit = QDateTimeEdit(self)
            if initial_value is not None:
                datetime_edit.setDateTime(initial_value)
            return datetime_edit

        # Fallback to text input if type is not recognized
        line_edit = QLineEdit(self)
        if initial_value is not None:
            line_edit.setText(str(initial_value))
        return line_edit

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

        # Show the add button and option menu if any fields are left to add
        if self.available_attributes:
            self.option_menu.show()
            self.add_button.show()

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
        self.option_menu.addItems([self.model_class.__fields__[field_name].description if self.model_class.__fields__[
            field_name].description else field_name for field_name in self.available_attributes])
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


def open_dynamic_form(model_class, title, description, default_fields=None, mode=None, init_values=None):
    app = QApplication(sys.argv)
    form = DynamicFormApp(model_class, title, description, default_fields, mode, init_values)
    form.show()
    app.exec()
    return form.getResult()




if __name__ == "__main__":
    # Example Pydantic class with various types
    class PersonModel(BaseModel):
        name: str = Field(default='', description='Name of the person')
        age: int = Field(default=0, description='Age of the person')
        salary: float = Field(default=0.0, description='Person\'s salary')
        birthdate: date = Field(default=None, description='Birthdate')
        last_logged_in: datetime = Field(default=None, description='Last login time')
        is_employee: bool = Field(default=False, description='Is the person an employee?')
        gender: Literal['Male', 'Female', 'Other'] = Field(default=None, description='Gender')


    # Test case with default fields and mode, and initial values
    title = "Person Form"
    description = "Fill out the details below. You can add or remove fields dynamically."
    default_fields = ["name", "age"]
    init_values = {"name": "John Doe", "age": 30, "gender": "Male"}

    result = open_dynamic_form(PersonModel, title, description, default_fields=default_fields, mode='all',
                               init_values=init_values)
    if result:
        print(result)
    else:
        print("Form was closed or no data was submitted.")
