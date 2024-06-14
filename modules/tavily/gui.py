import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QComboBox, QCheckBox, QSpinBox, QPushButton, \
    QLabel, QTextEdit, QScrollArea
from PyQt6.QtCore import pyqtSlot
from modules.tavily.models import Tavily


class SearchRequestForm(QWidget):
    """
    Usage example

    app = QApplication(sys.argv)
    form = SearchRequestForm()
    form.show()
    app.exec()
    return form.search_request
    """

    def __init__(self, request: Tavily, title: str, description: str):
        super().__init__()
        self.request = request

        self.setWindowTitle(title)

        self.layout = QVBoxLayout()

        # Add description label
        description_label = QLabel(description)
        self.layout.addWidget(description_label)

        self.query_input = QTextEdit(self)
        self.query_input.setPlaceholderText('Query')
        self.query_input.setText(self.request.query)
        self.query_input.setMaximumHeight(60)  # Limit height to 60 pixels
        self.layout.addWidget(self.query_input)

        self.search_depth_input = QComboBox(self)
        self.search_depth_input.addItems(['basic', 'advanced'])
        self.search_depth_input.setCurrentText(self.request.search_depth)
        self.layout.addWidget(self.search_depth_input)

        self.include_answer_input = QCheckBox('Include Answer', self)
        self.include_answer_input.setChecked(self.request.include_answer)
        self.layout.addWidget(self.include_answer_input)

        self.include_images_input = QCheckBox('Include Images', self)
        self.include_images_input.setChecked(self.request.include_images)
        self.layout.addWidget(self.include_images_input)

        self.include_raw_content_input = QCheckBox('Include Raw Content', self)
        self.include_raw_content_input.setChecked(self.request.include_raw_content)
        self.layout.addWidget(self.include_raw_content_input)

        self.max_results_input = QSpinBox(self)
        self.max_results_input.setMaximum(20)
        self.max_results_input.setValue(self.request.max_results)
        self.layout.addWidget(self.max_results_input)

        self.include_domains_input = QTextEdit(self)
        self.include_domains_input.setPlaceholderText('Include Domains (comma separated)')
        self.include_domains_input.setText(', '.join(self.request.include_domains))
        self.include_domains_input.setMaximumHeight(60)  # Limit height to 60 pixels
        self.layout.addWidget(self.include_domains_input)

        self.exclude_domains_input = QTextEdit(self)
        self.exclude_domains_input.setPlaceholderText('Exclude Domains (comma separated)')
        self.exclude_domains_input.setText(', '.join(self.request.exclude_domains))
        self.exclude_domains_input.setMaximumHeight(60)  # Limit height to 60 pixels
        self.layout.addWidget(self.exclude_domains_input)

        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

        self.search_request = None

    @pyqtSlot()
    def submit(self):
        query = self.query_input.toPlainText()
        search_depth = self.search_depth_input.currentText()
        include_answer = self.include_answer_input.isChecked()
        include_images = self.include_images_input.isChecked()
        include_raw_content = self.include_raw_content_input.isChecked()
        max_results = self.max_results_input.value()
        include_domains = self.include_domains_input.toPlainText().split(',')
        exclude_domains = self.exclude_domains_input.toPlainText().split(',')

        self.search_request = Tavily(
            api_key=self.request.api_key,
            query=query,
            search_depth=search_depth,
            include_answer=include_answer,
            include_images=include_images,
            include_raw_content=include_raw_content,
            max_results=max_results,
            include_domains=[domain.strip() for domain in include_domains],
            exclude_domains=[domain.strip() for domain in exclude_domains]
        )

        self.close()


def request_form(request: Tavily, title: str, description: str):
    app = QApplication(sys.argv)
    form = SearchRequestForm(request=request, title=title, description=description)
    form.show()
    app.exec()
    return form.search_request


# Example usage
if __name__ == '__main__':
    from modules.tavily.models import Tavily  # Assuming Tavily is defined here

    request = Tavily(
        api_key='your_api_key',
        query='initial query',
        search_depth='basic',
        include_answer=True,
        include_images=False,
        include_raw_content=False,
        max_results=10,
        include_domains=['example.com'],
        exclude_domains=['example.org']
    )

    title = 'Search Request Form'
    description = 'Please fill out the search request form and click Submit.'

    search_request = request_form(request, title, description)
    print('Search Request:', search_request)
