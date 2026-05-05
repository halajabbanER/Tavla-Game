from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFrame, QMessageBox
from PyQt5.QtCore import Qt
from gui.game_window import GameWindow
from client.client import Client


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.client = None
        self.game_window = None

        self.setWindowTitle("Backgammon Game")
        self.setGeometry(100, 100, 900, 650)
        self.setStyleSheet("""
            QWidget {
                background-color: #070B2A;
                color: white;
                font-family: Segoe UI;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        top_title = QLabel("Backgammon Game")
        top_title.setAlignment(Qt.AlignCenter)
        top_title.setStyleSheet("""
            color: #5EF6FF;
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 2px;
        """)

        card = QFrame()
        card.setFixedSize(620, 470)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(20, 25, 70, 210);
                border: 2px solid #8A5CFF;
                border-radius: 28px;
            }
        """)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(55, 35, 55, 35)
        card_layout.setSpacing(18)

        title = QLabel("BACKGAMMON")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: white;
            font-size: 44px;
            font-weight: bold;
        """)

        subtitle = QLabel("Online Tavla Game")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            color: #D7E8FF;
            font-size: 20px;
        """)

        # 🔥 الحقول (فاضية)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("👤 Player Name")

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("🖥️ Server IP")

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("🔌 Port")

        for input_box in [self.name_input, self.ip_input, self.port_input]:
            input_box.setFixedHeight(55)
            input_box.setStyleSheet("""
                QLineEdit {
                    background-color: rgba(255, 255, 255, 35);
                    border: 2px solid #79DFFF;
                    border-radius: 14px;
                    color: white;
                    font-size: 18px;
                    padding-left: 15px;
                }
                QLineEdit::placeholder {
                    color: #B8C7E0;
                }
                QLineEdit:focus {
                    border: 2px solid #F25CFF;
                    background-color: rgba(255, 255, 255, 50);
                }
            """)

        # الأزرار
        self.connect_btn = QPushButton("CONNECT")
        self.exit_btn = QPushButton("EXIT")

        self.connect_btn.setFixedHeight(58)
        self.exit_btn.setFixedHeight(58)

        self.exit_btn.clicked.connect(self.close)
        self.connect_btn.clicked.connect(self.connect_to_server)

        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B2CFF;
                border: 2px solid #41F4FF;
                border-radius: 14px;
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00A8FF;
            }
        """)

        self.exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #3A0B35;
                border: 2px solid #FF005C;
                border-radius: 14px;
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B0004B;
            }
        """)

        # ترتيب العناصر
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.name_input)
        card_layout.addWidget(self.ip_input)
        card_layout.addWidget(self.port_input)
        card_layout.addWidget(self.connect_btn)
        card_layout.addWidget(self.exit_btn)

        card.setLayout(card_layout)

        main_layout.addWidget(top_title)
        main_layout.addSpacing(20)
        main_layout.addWidget(card)

        self.setLayout(main_layout)

    # 🔥 الاتصال بالسيرفر
    def connect_to_server(self):
        name = self.name_input.text().strip()
        ip = self.ip_input.text().strip()
        port_text = self.port_input.text().strip()

        # تحقق من الإدخال
        if not name or not ip or not port_text:
            QMessageBox.warning(self, "Missing Data", "Please fill all fields.")
            return

        # تحقق من port
        try:
            port = int(port_text)
        except ValueError:
            QMessageBox.warning(self, "Invalid Port", "Port must be a number.")
            return

        # إنشاء client
        self.client = Client(ip, port)

        # محاولة الاتصال
        if not self.client.connect():
            QMessageBox.critical(self, "Connection Failed", f"Cannot connect to {ip}:{port}")
            return

        # إرسال join
        self.client.send({
            "action": "join",
            "name": name
        })

        print(f"Connected to {ip}:{port}")

        # فتح اللعبة
        self.open_game_window()

    def open_game_window(self):
        self.game_window = GameWindow(self.client)
        self.game_window.show()
        self.close()