from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QApplication)
from PyQt6.QtCore import pyqtSlot
import sys


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


def create_message_box(message, title, description):
    app = QApplication(sys.argv)
    ex = MessageBox(message, title, description)
    ex.show()
    app.exec()