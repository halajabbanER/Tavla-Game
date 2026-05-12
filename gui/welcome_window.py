from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from gui.start_window import StartWindow


class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.start_window = None

        self.setWindowTitle("Backgammon Game")
        self.setGeometry(200, 100, 900, 650)

        self.set_background()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        start_btn = QPushButton("START GAME")
        start_btn.setFixedSize(300, 70)
        start_btn.setCursor(Qt.PointingHandCursor)

        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B2CFF;
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 20px;
                border: 3px solid #FFD700;
            }

            QPushButton:hover {
                background-color: #9B4DFF;
            }

            QPushButton:pressed {
                background-color: #4B0082;
            }
        """)

        start_btn.clicked.connect(self.open_start_window)

        layout.addStretch()
        layout.addSpacing(380)
        layout.addWidget(start_btn, alignment=Qt.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)

    def set_background(self):
        pixmap = QPixmap("style/background.png")

        if pixmap.isNull():
            self.setStyleSheet("background-color: #070B2A;")
            return

        palette = QPalette()
        palette.setBrush(
            QPalette.Window,
            QBrush(
                pixmap.scaled(
                    self.size(),
                    Qt.IgnoreAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        )

        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def resizeEvent(self, event):
        self.set_background()
        super().resizeEvent(event)

    def open_start_window(self):
        self.start_window = StartWindow()
        self.start_window.show()
        self.close()