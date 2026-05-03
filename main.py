import sys
from PyQt5.QtWidgets import QApplication
from gui.start_window import StartWindow

app = QApplication(sys.argv)
window = StartWindow()
window.show()

sys.exit(app.exec_())