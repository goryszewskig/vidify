from typing import Union, Callable

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QTimer


def printmsg():
    print("Event loop check")


class MainWindow(QMainWindow):
    def __init__(self, widget: Union['VLCPlayer', 'MpvPlayer'],
                 width: int = 800, height: int = 600,
                 fullscreen: bool = False) -> None:
        """
        Main window with whatever player is being used.
        """

        super().__init__()
        self.setWindowTitle('spotivids')
        self.setStyleSheet('background-color: #282828')

        if fullscreen:
            self.showFullScreen()
        if width is None:
            width = 800
        if height is None:
            height = 600
        self.resize(width, height)

        self.setCentralWidget(widget)

    def start_event_loop(self, event_loop: Callable, ms: int) -> None:
        """
        Starts a "manual" event loop with a timer every `ms` milliseconds.
        """

        timer = QTimer(self)
        timer.timeout.connect(event_loop)
        timer.start(ms)
