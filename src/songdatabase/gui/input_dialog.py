''' Dialog window that returns inputs for fields '''

from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QTableView, QComboBox, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QMessageBox, QLineEdit

class InputDialog(QDialog):
    def __init__(self, title, widget_name_list):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(300, 200)
        self._widgets = {}
        self._create_widgets(widget_name_list)

    def _create_widgets(self, widget_name_list):
        x = 10
        y = 30
        for label_name in widget_name_list:
            label = QLabel(label_name)
            label.setParent(self)
            label.setStyleSheet("font-size: 18px;")
            label.setGeometry(x, y, 75, 30)
            
            x += 70

            text_box = QLineEdit()
            text_box.setParent(self)
            text_box.setStyleSheet("font-size: 18px;")
            text_box.setGeometry(x, y, 210, 30)

            self._widgets[label_name] = text_box
            y += 40
            x = 10

        self._submit_button = QPushButton("Submit", self)
        self._submit_button.setGeometry(190, 170, 100, 30)
        self._submit_button.setStyleSheet("font-size: 18px;")
        self._submit_button.clicked.connect(self._submit_clicked)

    def _submit_clicked(self):
        for widget_name, text_box in self._widgets.items():
            if text_box.text() == "":
                self._display_message("Error", f"{widget_name} can't be empty")
                return

        self.close()

    def get_inputs(self):
        result = []
        for _, text_box in self._widgets.items():
            text = text_box.text()
            text = self._validate_input(text)
            result.append(text)
        return result

    def _validate_input(self, text):
        has_injection = False
        if '--' in text:
            has_injection = True
            text = text.replace('--', '__')

        if ';' in text:
            has_injection = True
            text = text.replace(';', ',')

        if has_injection:
            print("Hello, Little Johny Drop Tables! :)")

        return text

    def _display_message(self, title, msg):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(msg)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.resize(300, 200)
        message_box.exec()

def init_input_dialog(title, widget_name_list):
    return InputDialog(title, widget_name_list)
