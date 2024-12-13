''' Dialog window that shows a table to the user '''

import songdatabase.queries as qs
from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QTableView, QComboBox, QVBoxLayout, QLabel
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from songdatabase.errors.app_error import *
from songdatabase.errors.database_error import DatabaseQueryError

class TableDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Table View")
        self.resize(460, 460)
        self._db = db
        self._create_widgets()
    
    def _create_widgets(self):
        self._create_combo_box()
        self._create_submit_button()
        self._create_table_view()

    def _create_combo_box(self):
        self._table_label = QLabel("Table: ")
        self._table_label.setParent(self)
        self._table_label.setStyleSheet("font-size: 18px;")
        self._table_label.setGeometry(10, 30, 75, 30)

        table_names = [
                "Category",
                "Song",
                "Artist",
                "Album"
        ]

        self._table_cb = QComboBox()
        self._table_cb.setParent(self)
        self._table_cb.addItems(table_names)
        self._table_cb.setEditable(False)
        self._table_cb.setStyleSheet("font-size: 18px;")
        self._table_cb.setGeometry(90, 30, 250, 30)

    def _create_submit_button(self):
        self._submit_button = QPushButton("Submit", self)
        self._submit_button.setGeometry(350, 30, 100, 30)
        self._submit_button.setStyleSheet("font-size: 18px;")
        self._submit_button.clicked.connect(self._submit_clicked)

    def _create_table_view(self):
        self._model = QStandardItemModel(0, 0)
        self._table_view = QTableView()
        self._table_view.setParent(self)
        self._table_view.setModel(self._model)
        self._table_view.setGeometry(10, 70, 440, 380)
        self._table_view.setStyleSheet("font-size: 18px;")
        self._table_view.horizontalHeader().setMinimumSectionSize(200)

    def _submit_clicked(self):
        self._update_table_view()

    def _update_table_view(self):
        table_name = self._table_cb.currentText()
        columns = []

        match (table_name):
            case 'Song':
                query = qs.get_all_songs()
                columns.append("Title")
            case 'Artist':
                query = qs.get_all_artists()
                columns.append("Name")
                columns.append("Songs")
            case 'Category':
                query = qs.get_all_categories()
                columns.append("Category Name")
            case 'Album':
                query = qs.get_all_albums()
                columns.append("Title")
                columns.append("Year")
            case _:
                return

        self._model.clear()
        self._model.setHorizontalHeaderLabels(columns)
        rows = self._db.select_all(query)

        for row in rows:
            items = [QStandardItem(str(value)) for value in row]
            self._model.appendRow(items)

        self._table_view.resizeColumnsToContents()

def init_table_dialog(db):
    return TableDialog(db)
