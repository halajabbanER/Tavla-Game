import json

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QPushButton
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QPolygon, QColor, QRadialGradient, QPen


class DiceLabel(QLabel):
    clicked = pyqtSignal(int)

    def __init__(self, dice_index):
        super().__init__("⚀")
        self.dice_index = dice_index
        self.selected = False

    def mousePressEvent(self, event):
        self.clicked.emit(self.dice_index)

    def set_selected(self, selected):
        self.selected = selected
        border = "4px solid yellow" if selected else "3px solid #2B120C"

        self.setStyleSheet(f"""
            QLabel {{
                background-color: white;
                color: black;
                border: {border};
                border-radius: 10px;
                font-size: 36px;
                font-weight: bold;
            }}
        """)


class TriangleWidget(QWidget):
    clicked = pyqtSignal(object)

    def __init__(self, color, upside=True, index=0):
        super().__init__()
        self.color = color
        self.upside = upside
        self.index = index
        self.checkers = []
        self.highlighted = False
        self.setFixedSize(80, 230)

    def set_checkers(self, checkers):
        self.checkers = checkers
        self.update()

    def set_highlighted(self, highlighted):
        self.highlighted = highlighted
        self.update()

    def mousePressEvent(self, event):
        self.clicked.emit(self)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(self.color))
        painter.setPen(Qt.NoPen)

        if self.upside:
            triangle = QPolygon([
                QPoint(0, 0),
                QPoint(self.width(), 0),
                QPoint(self.width() // 2, self.height())
            ])
        else:
            triangle = QPolygon([
                QPoint(0, self.height()),
                QPoint(self.width(), self.height()),
                QPoint(self.width() // 2, 0)
            ])

        painter.drawPolygon(triangle)

        if self.highlighted:
            painter.setPen(QPen(QColor("yellow"), 4))
            painter.drawRect(self.rect())

        checker_size = 44
        x = (self.width() - checker_size) // 2

        for index, checker_color in enumerate(self.checkers[:5]):
            y = 8 + index * 38 if self.upside else self.height() - checker_size - 8 - index * 38
            self.draw_checker(painter, x, y, checker_size, checker_color)

    def draw_checker(self, painter, x, y, size, checker_color):
        if checker_color == "white":
            base = QColor("#F4D7C5")
            edge = QColor("#B87D5B")
            light = QColor("#FFFFFF")
        else:
            base = QColor("#7A1E32")
            edge = QColor("#2B0A12")
            light = QColor("#B84A63")

        gradient = QRadialGradient(x + size * 0.35, y + size * 0.25, size * 0.7)
        gradient.setColorAt(0, light)
        gradient.setColorAt(0.55, base)
        gradient.setColorAt(1, edge)

        painter.setBrush(gradient)
        painter.setPen(QPen(edge, 3))
        painter.drawEllipse(x, y, size, size)


class BarWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.white_checkers = []
        self.dark_checkers = []
        self.setFixedWidth(45)

    def set_checkers(self, white_checkers, dark_checkers):
        self.white_checkers = white_checkers
        self.dark_checkers = dark_checkers
        self.update()

    def mousePressEvent(self, event):
        self.clicked.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor("#2B120C"))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        checker_size = 32
        x = (self.width() - checker_size) // 2

        for i, _ in enumerate(self.white_checkers[:5]):
            self.draw_checker(painter, x, 20 + i * 35, checker_size, "white")

        for i, _ in enumerate(self.dark_checkers[:5]):
            self.draw_checker(painter, x, self.height() - 55 - i * 35, checker_size, "dark")

    def draw_checker(self, painter, x, y, size, checker_color):
        if checker_color == "white":
            base = QColor("#F4D7C5")
            edge = QColor("#B87D5B")
            light = QColor("#FFFFFF")
        else:
            base = QColor("#7A1E32")
            edge = QColor("#2B0A12")
            light = QColor("#B84A63")

        gradient = QRadialGradient(x + size * 0.35, y + size * 0.25, size * 0.7)
        gradient.setColorAt(0, light)
        gradient.setColorAt(0.55, base)
        gradient.setColorAt(1, edge)

        painter.setBrush(gradient)
        painter.setPen(QPen(edge, 2))
        painter.drawEllipse(x, y, size, size)


class GameWindow(QWidget):
    server_message_signal = pyqtSignal(object)

    def __init__(self, client=None):
        super().__init__()

        self.client = client
        self.points = []
        self.current_dice = []
        self.selected_dice_index = 0
        self.is_my_turn = False
        self.my_symbol = None
        self.current_board = []
        self.current_bar = {"1": 0, "-1": 0}
        self.game_over = False

        self.setWindowTitle("Backgammon Board")
        self.resize(1150, 650)
        self.setMinimumSize(1050, 600)
        self.setStyleSheet("background-color: #070B2A; color: white;")

        self.dice1_label = DiceLabel(0)
        self.dice2_label = DiceLabel(1)

        for dice in [self.dice1_label, self.dice2_label]:
            dice.setAlignment(Qt.AlignCenter)
            dice.setFixedSize(58, 58)
            dice.set_selected(False)
            dice.clicked.connect(self.select_dice)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(14, 14, 14, 14)
        main_layout.setSpacing(18)

        board_frame = QFrame()
        board_frame.setStyleSheet("""
            QFrame {
                background-color: #4A2418;
                border: 6px solid #2B120C;
                border-radius: 18px;
            }
        """)

        board_main = QHBoxLayout()
        board_main.setContentsMargins(14, 14, 14, 14)
        board_main.setSpacing(0)

        left_half = self.create_half_board(show_dice=False)
        middle_separator = self.create_bar()
        self.bar_widget.clicked.connect(self.enter_from_bar)
        right_half = self.create_half_board(show_dice=True)

        board_main.addWidget(left_half)
        board_main.addWidget(middle_separator)
        board_main.addWidget(right_half)
        board_frame.setLayout(board_main)

        side_panel = QVBoxLayout()
        side_panel.setSpacing(15)

        self.roll_btn = QPushButton("Roll Dice")
        self.state_btn = QPushButton("Get State")
        self.bar_btn = QPushButton("Enter Bar")
        self.skip_btn = QPushButton("Skip Dice")
        self.exit_btn = QPushButton("Exit")

        for btn in [self.roll_btn, self.state_btn, self.bar_btn, self.skip_btn, self.exit_btn]:
            btn.setFixedHeight(55)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #151B46;
                    border: 2px solid #5EF6FF;
                    border-radius: 12px;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #7B2CFF;
                }
                QPushButton:disabled {
                    background-color: #333333;
                    border: 2px solid #777777;
                    color: #AAAAAA;
                }
            """)

        self.roll_btn.clicked.connect(self.send_roll_dice)
        self.state_btn.clicked.connect(self.get_state)
        self.bar_btn.clicked.connect(self.enter_from_bar)
        self.skip_btn.clicked.connect(self.skip_dice)
        self.exit_btn.clicked.connect(self.close)

        self.status_label = QLabel("Status: Waiting...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("""
            color: #5EF6FF;
            font-size: 16px;
            font-weight: bold;
        """)

        side_panel.addSpacing(40)
        side_panel.addWidget(self.roll_btn)
        side_panel.addWidget(self.state_btn)
        side_panel.addWidget(self.bar_btn)
        side_panel.addWidget(self.skip_btn)
        side_panel.addWidget(self.exit_btn)
        side_panel.addSpacing(20)
        side_panel.addWidget(self.status_label)
        side_panel.addStretch()

        main_layout.addWidget(board_frame, 6)
        main_layout.addLayout(side_panel, 1)
        self.setLayout(main_layout)

        self.setup_starting_checkers()
        self.bar_widget.set_checkers([], [])

        self.roll_btn.setEnabled(False)
        self.bar_btn.setEnabled(False)
        self.skip_btn.setEnabled(False)

        self.server_message_signal.connect(self.update_from_server)

        if self.client:
            self.client.start_listening(self.handle_server_message)

    def handle_server_message(self, data):
        self.server_message_signal.emit(data)

    def update_from_server(self, data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                return

        message = data.get("message")

        if "state" in data:
            state = data["state"]

            if "board" in state:
                self.current_board = state["board"]
                self.update_board(self.current_board)

            if "bar" in state:
                self.current_bar = state["bar"]
                white_bar = self.current_bar.get(1, self.current_bar.get("1", 0))
                dark_bar = self.current_bar.get(-1, self.current_bar.get("-1", 0))
                self.bar_widget.set_checkers(["white"] * white_bar, ["dark"] * dark_bar)

            self.current_dice = state.get("current_dice", [])
            self.game_over = state.get("game_over", False)

            if self.selected_dice_index >= len(self.current_dice):
                self.selected_dice_index = 0

            self.refresh_dice_display()

            current_turn = state.get("current_turn")

            if self.client:
                my_id = str(self.client.socket.getsockname())
                self.is_my_turn = str(current_turn) == my_id

                for player in state.get("players", []):
                    if str(player.get("id")) == my_id:
                        self.my_symbol = player.get("symbol")

                has_bar_checker = self.has_my_checker_on_bar()

                self.roll_btn.setEnabled(
                    self.is_my_turn and len(self.current_dice) == 0 and not self.game_over
                )

                self.bar_btn.setEnabled(
                    self.is_my_turn and bool(self.current_dice) and has_bar_checker and not self.game_over
                )

                self.skip_btn.setEnabled(
                    self.is_my_turn and bool(self.current_dice) and not self.game_over
                )

                if not self.game_over:
                    if self.is_my_turn:
                        if has_bar_checker and self.current_dice:
                            self.status_label.setText("Status: Enter from bar first")
                        elif self.current_dice:
                            self.status_label.setText("Status: Your turn - choose dice/checker")
                        else:
                            self.status_label.setText("Status: Your turn - roll dice")
                    else:
                        self.status_label.setText("Status: Waiting for opponent")

            self.update_highlights()

            if self.game_over:
                winner = state.get("winner", "Player")
                self.status_label.setText(f"🎉 {winner} wins!\nGame Over")
                self.roll_btn.setEnabled(False)
                self.state_btn.setEnabled(False)
                self.bar_btn.setEnabled(False)
                self.skip_btn.setEnabled(False)

                for point in self.points:
                    point.set_highlighted(False)

                return

        if "dice" in data:
            self.current_dice = data["dice"]
            self.selected_dice_index = 0
            self.refresh_dice_display()
            self.roll_btn.setEnabled(False)
            self.skip_btn.setEnabled(self.is_my_turn and bool(self.current_dice))
            self.bar_btn.setEnabled(self.is_my_turn and self.has_my_checker_on_bar())
            self.update_highlights()

        if message:
            if message == "Not your turn":
                self.status_label.setText("Status: Not your turn")
            elif message == "Room full. Please wait...":
                self.status_label.setText("Status: Room is full")
                self.roll_btn.setEnabled(False)
                self.bar_btn.setEnabled(False)
                self.skip_btn.setEnabled(False)
            elif message == "Checker moved":
                self.status_label.setText("Status: Checker moved")
            elif message == "Dice rolled":
                if self.has_my_checker_on_bar():
                    self.status_label.setText("Status: Dice rolled - enter from bar")
                else:
                    self.status_label.setText("Status: Dice rolled - choose dice/checker")
            elif message == "Dice skipped":
                self.status_label.setText("Status: Dice skipped")
            elif message == "You must enter from the bar first":
                self.status_label.setText("Status: You must enter from the bar first")
                self.bar_btn.setEnabled(True)
                self.skip_btn.setEnabled(True)
            elif message == "Target point is blocked":
                self.status_label.setText("Status: Target blocked - choose another dice or skip")
                self.skip_btn.setEnabled(True)
            else:
                self.status_label.setText("Status: " + message)

    def select_dice(self, dice_index):
        if dice_index >= len(self.current_dice):
            return

        self.selected_dice_index = dice_index
        self.refresh_dice_display()
        self.update_highlights()

        dice_value = self.current_dice[self.selected_dice_index]
        self.status_label.setText(f"Status: Selected dice {dice_value}")

    def refresh_dice_display(self):
        dice_faces = {
            1: "⚀", 2: "⚁", 3: "⚂",
            4: "⚃", 5: "⚄", 6: "⚅"
        }

        if len(self.current_dice) == 0:
            self.dice1_label.setText("⚀")
            self.dice2_label.setText("⚀")
            self.dice1_label.set_selected(False)
            self.dice2_label.set_selected(False)

        elif len(self.current_dice) == 1:
            self.dice1_label.setText(dice_faces.get(self.current_dice[0], "⚀"))
            self.dice2_label.setText("-")
            self.dice1_label.set_selected(self.selected_dice_index == 0)
            self.dice2_label.set_selected(False)

        else:
            self.dice1_label.setText(dice_faces.get(self.current_dice[0], "⚀"))
            self.dice2_label.setText(dice_faces.get(self.current_dice[1], "⚀"))
            self.dice1_label.set_selected(self.selected_dice_index == 0)
            self.dice2_label.set_selected(self.selected_dice_index == 1)

    def get_selected_dice_value(self):
        if not self.current_dice:
            return None

        if self.selected_dice_index >= len(self.current_dice):
            self.selected_dice_index = 0

        return self.current_dice[self.selected_dice_index]

    def has_my_checker_on_bar(self):
        if self.my_symbol is None:
            return False

        count = self.current_bar.get(
            self.my_symbol,
            self.current_bar.get(str(self.my_symbol), 0)
        )

        return count > 0

    def is_target_blocked(self, target_index):
        if target_index < 0 or target_index >= 24:
            return False

        if self.my_symbol is None:
            return True

        value = self.current_board[target_index]
        return value * self.my_symbol < -1

    def can_move_from_point(self, from_index):
        dice_value = self.get_selected_dice_value()

        if dice_value is None:
            return False

        if self.my_symbol == 1:
            target = from_index + dice_value
        else:
            target = from_index - dice_value

        return not self.is_target_blocked(target)

    def update_highlights(self):
        for point in self.points:
            point.set_highlighted(False)

        if self.game_over or not self.is_my_turn or not self.current_dice:
            return

        if self.my_symbol is None:
            return

        if self.has_my_checker_on_bar():
            return

        for index, value in enumerate(self.current_board):
            if index >= len(self.points):
                break

            if value * self.my_symbol > 0 and self.can_move_from_point(index):
                self.points[index].set_highlighted(True)

    def point_clicked(self, point):
        if self.game_over:
            self.status_label.setText("Game over")
            return

        if not self.is_my_turn:
            self.status_label.setText("Status: Not your turn")
            return

        if not self.current_dice:
            self.status_label.setText("Status: Roll dice first")
            return

        if self.has_my_checker_on_bar():
            self.status_label.setText("Status: You must enter from the bar first")
            return

        if not point.checkers:
            self.status_label.setText("Status: No checker here")
            return

        if not point.highlighted:
            self.status_label.setText("Status: This checker cannot move with selected dice")
            return

        self.send_move(point.index)

    def enter_from_bar(self):
        if self.game_over:
            self.status_label.setText("Game over")
            return

        if not self.is_my_turn:
            self.status_label.setText("Status: Not your turn")
            return

        if not self.current_dice:
            self.status_label.setText("Status: Roll dice first")
            return

        if not self.has_my_checker_on_bar():
            self.status_label.setText("Status: No checker on bar")
            return

        dice_value = self.get_selected_dice_value()

        if dice_value is None:
            self.status_label.setText("Status: Select dice first")
            return

        if self.client:
            self.client.send({
                "action": "move",
                "from": -1,
                "dice": dice_value
            })

        self.status_label.setText(f"Status: Entering from bar using dice {dice_value}")

    def skip_dice(self):
        dice_value = self.get_selected_dice_value()

        if dice_value is None:
            self.status_label.setText("Status: No dice to skip")
            return

        if not self.is_my_turn:
            self.status_label.setText("Status: Not your turn")
            return

        if self.client:
            self.client.send({
                "action": "skip",
                "dice": dice_value
            })

        self.status_label.setText(f"Status: Skipped dice {dice_value}")

    def send_move(self, from_index):
        dice_value = self.get_selected_dice_value()

        if dice_value is None:
            self.status_label.setText("Status: Select dice first")
            return

        if self.client:
            self.client.send({
                "action": "move",
                "from": from_index,
                "dice": dice_value
            })

        self.status_label.setText(f"Status: Move from {from_index} using dice {dice_value}")

    def send_roll_dice(self):
        if self.game_over:
            return

        if not self.is_my_turn:
            self.status_label.setText("Status: Not your turn")
            return

        if self.current_dice:
            self.status_label.setText("Status: Use current dice first")
            return

        if self.client:
            self.client.send({"action": "roll"})

        self.roll_btn.setEnabled(False)
        self.status_label.setText("Status: Rolling dice...")

    def get_state(self):
        if self.client:
            self.client.send({"action": "state"})

    def create_half_board(self, show_dice=False):
        half = QFrame()
        half.setStyleSheet("""
            QFrame {
                background-color: #C8873D;
                border: 4px solid #2B120C;
                border-radius: 8px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(0)

        top_row = QHBoxLayout()
        bottom_row = QHBoxLayout()
        top_row.setSpacing(0)
        bottom_row.setSpacing(0)

        for i in range(6):
            color = "#990000" if i % 2 == 0 else "#E8BD6B"
            point = TriangleWidget(color, upside=True, index=len(self.points))
            point.clicked.connect(self.point_clicked)
            self.points.append(point)
            top_row.addWidget(point)

        for i in range(6):
            color = "#E8BD6B" if i % 2 == 0 else "#990000"
            point = TriangleWidget(color, upside=False, index=len(self.points))
            point.clicked.connect(self.point_clicked)
            self.points.append(point)
            bottom_row.addWidget(point)

        middle_area = QHBoxLayout()
        middle_area.setAlignment(Qt.AlignCenter)

        if show_dice:
            middle_area.addWidget(self.dice1_label)
            middle_area.addSpacing(10)
            middle_area.addWidget(self.dice2_label)

        layout.addLayout(top_row)
        layout.addStretch()
        layout.addLayout(middle_area)
        layout.addStretch()
        layout.addLayout(bottom_row)

        half.setLayout(layout)
        return half

    def create_bar(self):
        self.bar_widget = BarWidget()
        self.bar_widget.setStyleSheet("""
            QWidget {
                background-color: #2B120C;
                border-left: 3px solid #8B5A2B;
                border-right: 3px solid #8B5A2B;
            }
        """)
        return self.bar_widget

    def update_board(self, board):
        for i, value in enumerate(board):
            if i >= len(self.points):
                break

            if value > 0:
                self.points[i].set_checkers(["white"] * value)
            elif value < 0:
                self.points[i].set_checkers(["dark"] * abs(value))
            else:
                self.points[i].set_checkers([])

    def setup_starting_checkers(self):
        self.points[0].set_checkers(["white"] * 2)
        self.points[5].set_checkers(["dark"] * 5)
        self.points[7].set_checkers(["dark"] * 3)
        self.points[11].set_checkers(["white"] * 5)
        self.points[12].set_checkers(["dark"] * 5)
        self.points[16].set_checkers(["white"] * 3)
        self.points[18].set_checkers(["white"] * 5)
        self.points[23].set_checkers(["dark"] * 2)