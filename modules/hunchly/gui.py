
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QErrorMessage, QCheckBox
)
from PyQt6.QtCore import pyqtSlot
from pydantic import BaseModel, Field, AnyUrl
from typing import List, Optional, Callable
from datetime import datetime
import sys


class CheckBoxAppOutput(BaseModel):
    case_name: str | None = Field(default=None)
    case_id: int | None = Field(default=None)
    title: str | None = Field(default=None)
    id: int | None = Field(default=None)


class CheckBoxApp(QWidget):
    """
    Example of usage
    """

    def __init__(self, title, description, case_names, case_ids, api_function):
        super().__init__()
        self.case_names = case_names
        self.case_ids = case_ids
        self.api_function = api_function
        self.selected_page_title = None
        self.selected_page_id = None
        self.hunchly_pages = None
        self.initUI(title, description)

    def initUI(self, title, description):
        layout = QVBoxLayout()

        # Set window title
        self.setWindowTitle(title)

        # Add description label
        description_label = QLabel(description, self)
        layout.addWidget(description_label)

        # Add case name and case id fields
        case_layout = QHBoxLayout()
        self.case_name_combo = QComboBox(self)
        self.case_name_combo.addItems(self.case_names)
        self.case_name_combo.currentIndexChanged.connect(self.onCaseNameChanged)
        case_name_label = QLabel("Case name:", self)
        case_layout.addWidget(case_name_label)
        case_layout.addWidget(self.case_name_combo)

        self.case_id_combo = QComboBox(self)
        self.case_id_combo.addItems([str(id) for id in self.case_ids])
        self.case_id_combo.currentIndexChanged.connect(self.onCaseIdChanged)
        case_id_label = QLabel("Case id:", self)
        case_layout.addWidget(case_id_label)
        case_layout.addWidget(self.case_id_combo)

        get_pages_button = QPushButton('Get Pages', self)
        get_pages_button.clicked.connect(self.onGetPages)
        case_layout.addWidget(get_pages_button)

        layout.addLayout(case_layout)

        # Add select page by title
        title_layout = QVBoxLayout()
        title_label = QLabel("Select page by title:", self)
        title_layout.addWidget(title_label)

        self.title_combo = QComboBox(self)
        self.title_combo.setEnabled(False)
        self.title_combo.currentIndexChanged.connect(self.onTitleChanged)
        title_layout.addWidget(self.title_combo)

        layout.addLayout(title_layout)

        # Add select page by id
        id_layout = QVBoxLayout()
        id_label = QLabel("Select page by id:", self)
        id_layout.addWidget(id_label)

        self.id_combo = QComboBox(self)
        self.id_combo.setEnabled(False)
        self.id_combo.currentIndexChanged.connect(self.onIdChanged)
        id_layout.addWidget(self.id_combo)

        layout.addLayout(id_layout)

        # Add submit button
        submit_button = QPushButton('Submit', self)
        submit_button.clicked.connect(self.onSubmit)
        layout.addWidget(submit_button)

        self.setLayout(layout)
        self.show()

    @pyqtSlot(int)
    def onCaseNameChanged(self, index):
        self.case_id_combo.setCurrentIndex(index)

    @pyqtSlot(int)
    def onCaseIdChanged(self, index):
        self.case_name_combo.setCurrentIndex(index)

    @pyqtSlot()
    def onGetPages(self):
        case_id_text = self.case_id_combo.currentText()
        if case_id_text:
            case_id = int(case_id_text)
            self.hunchly_pages = self.api_function(case_id_text)
            self.populatePageFields()
        else:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage('Please select a valid Case ID.')
            error_dialog.exec()

    def populatePageFields(self):
        self.title_combo.clear()
        self.id_combo.clear()
        if self.hunchly_pages:
            self.title_combo.addItems([page.title for page in self.hunchly_pages.data])
            self.id_combo.addItems([str(page.id) for page in self.hunchly_pages.data])
            self.title_combo.setEnabled(True)
            self.id_combo.setEnabled(True)

    @pyqtSlot(int)
    def onTitleChanged(self, index):
        self.id_combo.setCurrentIndex(index)

    @pyqtSlot(int)
    def onIdChanged(self, index):
        self.title_combo.setCurrentIndex(index)

    @pyqtSlot()
    def onSubmit(self):
        selected_case_name = self.case_name_combo.currentText()
        selected_case_id = self.case_id_combo.currentText()

        if not selected_case_name and not selected_case_id:
            error_dialog = QErrorMessage(self)
            error_dialog.showMessage('At least one of Case name or Case id must be set.')
            error_dialog.exec()
            return

        self.selected_page_title = self.title_combo.currentText()
        self.selected_page_id = self.id_combo.currentText()

        self.close()

    def getSelectedData(self):
        return CheckBoxAppOutput(**{
            'case_name': self.case_name_combo.currentText(),
            'case_id': self.case_id_combo.currentText(),
            'title': self.selected_page_title,
            'id': self.selected_page_id
        })


# TODO: change to decorator
def check_box_form(title, description, case_names, case_ids, api_function):
    app = QApplication(sys.argv)
    ex = CheckBoxApp(title, description, case_names, case_ids, api_function)
    ex.show()
    app.exec()
    return ex.getSelectedData()
# TODO:Generlized


class CaseSelectionApp(QWidget):
    """
    Application to select case name and ID, with option to check all.
    """

    def __init__(self, title, description, case_names, case_ids):
        super().__init__()
        self.case_names = case_names
        self.case_ids = case_ids
        self.selected_case_names = []
        self.selected_case_ids = []
        self.initUI(title, description)

    def initUI(self, title, description):
        layout = QVBoxLayout()

        # Set window title
        self.setWindowTitle(title)

        # Add description label
        description_label = QLabel(description, self)
        layout.addWidget(description_label)

        # Add case name and case id fields
        case_layout = QHBoxLayout()
        self.case_name_combo = QComboBox(self)
        self.case_name_combo.addItems(self.case_names)
        self.case_name_combo.currentIndexChanged.connect(self.onCaseNameChanged)
        case_name_label = QLabel("Case name:", self)
        case_layout.addWidget(case_name_label)
        case_layout.addWidget(self.case_name_combo)

        self.case_id_combo = QComboBox(self)
        self.case_id_combo.addItems([str(id) for id in self.case_ids])
        self.case_id_combo.currentIndexChanged.connect(self.onCaseIdChanged)
        case_id_label = QLabel("Case id:", self)
        case_layout.addWidget(case_id_label)
        case_layout.addWidget(self.case_id_combo)

        layout.addLayout(case_layout)

        # Add check all checkbox
        self.check_all_checkbox = QCheckBox("Check All", self)
        self.check_all_checkbox.stateChanged.connect(self.onCheckAll)
        layout.addWidget(self.check_all_checkbox)

        # Add submit button
        submit_button = QPushButton('Submit', self)
        submit_button.clicked.connect(self.onSubmit)
        layout.addWidget(submit_button)

        self.setLayout(layout)
        self.show()

    @pyqtSlot(int)
    def onCaseNameChanged(self, index):
        self.case_id_combo.setCurrentIndex(index)

    @pyqtSlot(int)
    def onCaseIdChanged(self, index):
        self.case_name_combo.setCurrentIndex(index)

    @pyqtSlot()
    def onCheckAll(self, state):
        if state == 2:  # Checked
            self.case_name_combo.setEnabled(False)
            self.case_id_combo.setEnabled(False)
        else:
            self.case_name_combo.setEnabled(True)
            self.case_id_combo.setEnabled(True)

    @pyqtSlot()
    def onSubmit(self):
        if self.check_all_checkbox.isChecked():
            self.selected_case_names = self.case_names
            self.selected_case_ids = self.case_ids
        else:
            selected_case_name = self.case_name_combo.currentText()
            selected_case_id = self.case_id_combo.currentText()

            if not selected_case_name or not selected_case_id:
                error_dialog = QErrorMessage(self)
                error_dialog.showMessage('Both Case name and Case id must be selected.')
                error_dialog.exec()
                return

            self.selected_case_names = [selected_case_name]
            self.selected_case_ids = [selected_case_id]

        self.close()

    def getSelectedData(self):
        return {
            'case_names': self.selected_case_names,
            'case_ids': self.selected_case_ids
        }


def case_selection_form(title, description, case_names, case_ids):
    app = QApplication(sys.argv)
    ex = CaseSelectionApp(title, description, case_names, case_ids)
    ex.show()
    app.exec()
    return ex.getSelectedData()
