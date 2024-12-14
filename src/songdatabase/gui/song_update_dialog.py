''' Dialog window that updates a songs relations (e.g. Category, Artist, Album) '''

import songdatabase.queries as qs
from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QTableView, QComboBox, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt
from songdatabase.errors.app_error import *
from songdatabase.errors.database_error import DatabaseQueryError
from songdatabase.gui.song_input_dialog import init_song_input_dialog

class SongUpdateDialog(QDialog):
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

        query = qs.get_all_fields()
        rows = self._db.select_all(query)
        song_names = [str(row[0]) for row in rows]

        self._table_cb = QComboBox()
        self._table_cb.setParent(self)
        self._table_cb.addItem("")
        self._table_cb.addItems(song_names)
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
        song = self._table_cb.currentText()
        
        if song == "":
            self._display_message("Error", "Please select a song.")
            return

        tables = [
                "Artist",
                "Category",
                "Album"
        ]

        dialog = init_song_input_dialog(f"{song} Update", tables, self._db)
        dialog.exec()
        results_dict = dialog.get_inputs()

        self._update_song(song, results_dict)
        self._update_table_view()

    def _update_song(self, song, results_dict):
        for table, value in results_dict.items():
            if value == "": continue
            query = ""

            match (table):
                case 'Artist':
                    query = qs.update_song_artist()
                    self._db.execute(query, (value, song))
                case 'Category':
                    query = qs.update_song_category()
                    self._db.execute(query, (value, song))
                case 'Album':
                    query = qs.update_song_album()
                    self._db.execute(query, (song, value))
            
    def _update_table_view(self):
        self._model.clear()
        columns = ['Song Title', 'Artist Name', 'Album Title', 'Category']
        self._model.setHorizontalHeaderLabels(columns)
        query = qs.get_all_fields()
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

def init_song_update_dialog(db):
    return SongUpdateDialog(db)
