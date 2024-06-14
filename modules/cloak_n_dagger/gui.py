import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox, QLabel
from PyQt6.QtCore import pyqtSlot


class CheckBoxApp(QWidget):
    """
    example of usage
    """
    def __init__(self, options, title, description):
        super().__init__()
        self.selected_options = []
        self.initUI(options, title, description)

    def initUI(self, options, title, description):
        layout = QVBoxLayout()

        # Set window title
        self.setWindowTitle(title)

        # Add description label
        description_label = QLabel(description, self)
        layout.addWidget(description_label)

        # Create checkboxes
        self.checkboxes = []
        for option in options:
            checkbox = QCheckBox(option, self)
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        # Add submit button
        submit_button = QPushButton('Submit', self)
        submit_button.clicked.connect(self.onSubmit)
        layout.addWidget(submit_button)

        self.setLayout(layout)
        self.show()

    @pyqtSlot()
    def onSubmit(self):
        self.selected_options = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        self.close()

    def getSelectedOptions(self):
        return self.selected_options


def check_box_form(options, title, description):
    app = QApplication(sys.argv)
    ex = CheckBoxApp(options, title, description)
    ex.show()
    app.exec()
    return ex.getSelectedOptions()
