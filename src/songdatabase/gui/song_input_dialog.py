''' Dialog window that returns inputs for all tables in the table list '''

import songdatabase.queries as qs
from PyQt6.QtWidgets import QApplication, QDialog, QPushButton, QTableView, QComboBox, QVBoxLayout, QLabel
from PyQt6.QtWidgets import QMessageBox, QLineEdit

class SongInputDialog(QDialog):
    def __init__(self, title, table_list, db):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(400, 200)
        self._db = db
        self._widgets = {}
        self._create_widgets(table_list)

    def _create_widgets(self, table_list):
        x = 30
        y = 30
        for table in table_list:
            query = self._get_query(table)
            if query is None: continue

            label = QLabel(f"{table}: ")
            label.setParent(self)
            label.setStyleSheet("font-size: 18px;")
            label.setGeometry(x, y, 120, 30)
            
            x += 110

            combo_box = QComboBox()
            combo_box.setParent(self)
            combo_box.setStyleSheet("font-size: 18px;")
            combo_box.setGeometry(x, y, 210, 30)
            
            rows = self._db.select_all(query)
            values = [str(row[0]) for row in rows]
            
            combo_box.addItems([""])
            combo_box.addItems(values)
            combo_box.setEditable(False)
            
            self._widgets[table] = combo_box
            y += 40
            x = 30

        self._submit_button = QPushButton("Submit", self)
        self._submit_button.setGeometry(30, 150, 100, 30)
        self._submit_button.setStyleSheet("font-size: 18px;")
        self._submit_button.clicked.connect(self._submit_clicked)

    def _get_query(self, table):
        match (table):
            case 'Artist': return qs.get_all_artists()
            case 'Category': return qs.get_all_categories()
            case 'Album': return qs.get_all_albums()
            case _: return None

    def _submit_clicked(self):
        self.close()

    def get_inputs(self):
        result = {}
        for table, combo_box in self._widgets.items():
            result[table] = combo_box.currentText();
        return result

def init_song_input_dialog(title, table_list, db):
    return SongInputDialog(title, table_list, db)
