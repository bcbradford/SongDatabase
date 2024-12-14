''' Dialog window that deletes an entry from the database '''

import songdatabase.queries as qs
from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QTableView, QComboBox, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt
from songdatabase.errors.app_error import *
from songdatabase.errors.database_error import DatabaseQueryError

class DeleteEntryDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("Delete Entry")
        self.resize(460, 460)
        self._db = db
        self._create_widgets()
    
    def _create_widgets(self):
        self._create_table_combo_box()
        self._create_input_combo_box()
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

    def _create_input_combo_box(self):
        self._input_label = QLabel("Delete: ")
        self._input_label.setParent(self)
        self._input_label.setStyleSheet("font-size: 18px;")
        self._input_label.setGeometry(10, 70, 75, 30)

        self._input_cb = QComboBox()
        self._input_cb.setParent(self)
        self._input_cb.setEditable(False)
        self._input_cb.setStyleSheet("font-size: 18px;")
        self._input_cb.setGeometry(90, 70, 250, 30)

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
        self._table_view.setGeometry(10, 110, 440, 340)
        self._table_view.setStyleSheet("font-size: 18px;")
        self._table_view.horizontalHeader().setMinimumSectionSize(200)

    def _cb_index_changed(self):
        self._update_table_view()
        self._update_input_cb()

    def _update_input_cb(self):
        self._input_cb.clear()
        self._input_cb.setCurrentIndex(-1)
        columns, query = self._get_query()
        rows = self._db.select_all(query)
        
        for row in rows:
            self._input_cb.addItem(str(row[0]))

    def _submit_clicked(self):
        if self._table_cb.currentIndex() == -1:
            self._display_message("Error", "Please select a table.")
            return

        table = self._table_cb.currentText()
        item_string = self._input_cb.currentText()

        if item_string == "":
            self._display_message("Error", f"Please select the {table} to delete.")
            return

        result = self._get_confirm_delete(table, item_string)
        if result == QMessageBox.StandardButton.No: 
            return

        self._execute_delete(table, item_string)
        self._update_input_cb()
        self._update_table_view()
        
    def _execute_delete(self, table, item_string):
        query = ""

        match (table):
            case 'Song':
                query = qs.delete_song()
            case 'Artist':
                query = qs.delete_artist()
            case 'Category':
                query = qs.delete_category()
            case 'Album':
                query = qs.delete_album()
            case _:
                self._display_message("Error", f"Invalid table {table}")
                return

        self._db.execute(query, (item_string,))

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

    def _get_confirm_delete(self, table, item):
        message_box = QMessageBox()
        message_box.setWindowTitle("Confirm Delete")
        message_box.setText(f"Are you sure you want to delete {table}: {item}?")
        message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        message_box.resize(300, 200)
        result = message_box.exec()
        return result


def init_delete_entry_dialog(db):
    return DeleteEntryDialog(db)
