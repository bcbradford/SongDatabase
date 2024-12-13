''' MainWindow class used to interact with the database '''

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QSizePolicy
from PyQt6.QtGui import QScreen, QAction

class MainWindow(QMainWindow):

    def __init__(self, config: dict, logger: "logger"):
        super().__init__()
        self._window_config = config['main_window']
        self._tables_config = config['database_tables']
        self._logger = logger

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
                "Open": (QAction("Open", self), self._open_clicked, False),
                "Exit": (QAction("Exit", self), self._exit_clicked, False)
            },
            "Database": {
                "Show": (QAction("Show", self), self._show_clicked, False)
            },
            "Settings": {
                "Display": (QAction("Display", self), self._display_clicked, True)
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
        pass

    def _open_clicked(self):
        print("open clicked")
        self._logger.info("Open Triggered")

    def _exit_clicked(self):
        print("exit clicked")
        self._logger.info("Exit Triggered")
        self.close()

    def _show_clicked(self):
        print("show clicked")
        self._logger.info("Show Triggered")
    
    def _display_clicked(self):
        print("display clicked")
        self._logger.info("Display Triggered")


def init_main_window(app: "QApplication", config: dict, logger: "Logger"):
    logger.info("Creating Main Window")
    window = MainWindow(config, logger)

    # center window
    screen = QScreen.availableGeometry(app.primaryScreen())
    screen_center = screen.center()
    window_frame = window.frameGeometry()
    window_frame.moveCenter(screen_center)

    window.move(window_frame.topLeft())

    logger.info("Main Window Created")
    return window
