''' Dialog window that creates a database entity '''

import songdatabase.queries as qs
from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QTableView, QComboBox, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt
from songdatabase.errors.app_error import *
from songdatabase.errors.database_error import DatabaseQueryError
from songdatabase.gui.input_dialog import init_input_dialog

class CreateEntryDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Create Entry")
        self.resize(460, 460)
        self._db = db
        self._create_widgets()
    
    def _create_widgets(self):
        self._create_table_combo_box()
        self._create_submit_button()
        self._create_table_view()
        
    def _create_table_combo_box(self):
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
        self._table_cb.setCurrentIndex(-1)
        self._table_cb.currentIndexChanged.connect(self._cb_index_changed)

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

    def _cb_index_changed(self):
        self._update_table_view()

    def _submit_clicked(self):
        if self._table_cb.currentIndex() == -1:
            self._display_message("Error", "Please select a table.")
            return

        table = self._table_cb.currentText()

        if table == "":
            self._display_message("Error", f"Please select the type to create.")
            return

        self._execute_create(table)
        self._update_table_view()
        
    def _execute_create(self, table):
        query = ""
        dialog = None

        match (table):
            case 'Song':
                query = qs.create_new_song()
                dialog = init_input_dialog("Song", ["Title"])
            case 'Artist':
                query = qs.create_new_artist()
                dialog = init_input_dialog("Artist", ["Name"])
            case 'Category':
                query = qs.create_new_category()
                dialog = init_input_dialog("Category", ["Name"])
            case 'Album':
                query = qs.create_new_album()
                dialog = init_input_dialog("Album", ["Title", "Year"])
            case _:
                self._display_message("Error", f"Invalid table {table}")
                return

        dialog.exec()
        values = dialog.get_inputs()
        if values[0] == "": return

        self._db.execute(query, values)

    def _get_query(self):
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
                columns.append("CategoryName")
            case 'Album':
                query = qs.get_all_albums()
                columns.append("Title")
                columns.append("Year")
            case _:
                return None

        return (columns, query)

    def _update_table_view(self):
        table_name = self._table_cb.currentText()
        columns, query = self._get_query()

        self._model.clear()
        self._model.setHorizontalHeaderLabels(columns)
        rows = self._db.select_all(query)

        for row in rows:
            items = []
            for value in row:
                item = QStandardItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                items.append(item)
            self._model.appendRow(items)

        self._table_view.resizeColumnsToContents()

    def _display_message(self, title, msg):
        message_box = QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(msg)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.resize(300, 200)
        message_box.exec()

def init_create_entry_dialog(db):
    return CreateEntryDialog(db)
