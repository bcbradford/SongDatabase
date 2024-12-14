''' MainWindow class used to interact with the database '''

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QSizePolicy, QTableView, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QScreen, QAction, QStandardItem, QStandardItemModel
import songdatabase.queries as qs
from songdatabase.errors.app_error import AppError
from songdatabase.errors.database_error import DatabaseQueryError
from songdatabase.gui.table_dialog import init_table_dialog
from songdatabase.gui.create_entry_dialog import init_create_entry_dialog
from songdatabase.gui.update_entry_dialog import init_update_entry_dialog
from songdatabase.gui.delete_entry_dialog import init_delete_entry_dialog
from songdatabase.gui.song_update_dialog import init_song_update_dialog

class MainWindow(QMainWindow):

    def __init__(self, config: dict, logger: "logger", db: "Database"):
        super().__init__()
        self._window_config = config['main_window']
        self._table_config = config['database_tables']
        self._logger = logger
        self._db = db
        self._column_names = []
        self._init_window()

    def _init_window(self):
        self.setWindowTitle(self._window_config.get('title', 'App'))
        self._set_size()
        self._create_menubar()
        self._create_widgets()

    def _set_size(self):
        x = self._window_config.get("x", 1024)
        y = self._window_config.get("y", 768)
        self.setFixedSize(x, y)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def _create_menubar(self):
        menubar = self.menuBar()

        # Dictionary: { "Menu_Name": {"Action_Name": (Action, Event, LineSeparator)} }
        menus = {
            "File": {
                "Exit": (QAction("Exit", self), self._exit_clicked, False)
            },
            "Database": {
                "Show": (QAction("Show", self), self._show_clicked, False),
                "Update Song": (QAction("Update Song", self), self._update_song_clicked, True),
                "Create Entry": (QAction("Create Entry", self), self._create_entry_clicked, False),
                "Delete Entry": (QAction("Delete Entry", self), self._delete_entry_clicked, False),
                "Update Entry": (QAction("Update Entry", self), self._update_entry_clicked, False)
            }
        }

        for menu_name, actions in menus.items():
            self._create_menu(menubar, menu_name, actions)

    def _create_menu(self, menubar, menu_name: str, actions: dict):
        menu = menubar.addMenu(menu_name)

        for action_name, (action, event, separator) in actions.items():
            menu.addAction(action)
            action.triggered.connect(event)
            if separator: menu.addSeparator()

    def _create_widgets(self):
        self._create_table_view()

    def _create_table_view(self):
        # add entities only to our table view
        self._column_names = [
            "Song Title",
            "Artist Name",
            "Album Title",
            "Category"
        ]

        self._model = QStandardItemModel(0, 4)
        self._model.setHorizontalHeaderLabels(self._column_names)
        self._song_label = QLabel("Song Database")
        self._song_label.setStyleSheet("font-size: 32px;")

        self._table_view = QTableView()
        self._table_view.setModel(self._model)
        self._update_table()
        self._table_view.horizontalHeader().setMinimumSectionSize(200)

        self._table_view.setStyleSheet("font-size: 18px;")

        layout = QVBoxLayout()
        layout.addWidget(self._song_label)
        layout.addWidget(self._table_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _update_table(self):
        self._model.clear()
        self._model.setHorizontalHeaderLabels(self._column_names)
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

    def _exit_clicked(self):
        self._logger.info("Exit Triggered")
        self.close()

    def _show_clicked(self):
        self._logger.info("Show Triggered")
        dialog = init_table_dialog(self._db)
        if dialog is None: return
        dialog.exec()

    def _update_song_clicked(self):
        self._logger.info("Update Song Triggered")
        dialog = init_song_update_dialog(self._db)
        if dialog is None: return
        dialog.exec()
        self._update_table()

    def _create_entry_clicked(self):
        self._logger.info("Create Entry Triggered")
        dialog = init_create_entry_dialog(self._db)
        if dialog is None: return
        dialog.exec()
        self._update_table()

    def _delete_entry_clicked(self):
        self._logger.info("Delete Entry Triggered")
        dialog = init_delete_entry_dialog(self._db)
        if dialog is None: return
        dialog.exec()
        self._update_table()

    def _update_entry_clicked(self):
        self._logger.info("Update Entry Triggered")
        dialog = init_update_entry_dialog(self._db)
        if dialog is None: return
        dialog.exec()
        self._update_table()

def init_main_window(app: "QApplication", config: dict, logger: "Logger", db: "Database"):
    logger.info("Creating Main Window")
    window = None

    try:
        window = MainWindow(config, logger, db)
        # center window
        screen = QScreen.availableGeometry(app.primaryScreen())
        screen_center = screen.center()
        window_frame = window.frameGeometry()
        window_frame.moveCenter(screen_center)

        window.move(window_frame.topLeft())

        logger.info("Main Window Created")
    except DatabaseQueryError as e:
        print(e.to_string())
        logger.error(e.get_logger_ouput())
    except AppError as e:
        print(e.to_string())
        logger.error(e.get_logger_output())
    except Exception as e:
        print("An unhandled error occured.")
        logger.error(f"{e}")
    finally:
        db.close()
        return window
