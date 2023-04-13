from PySide6.QtWidgets import QApplication
from libs.windows import main_window as mw
import sys

app = QApplication(sys.argv)
window = mw.MainWindow()
window.show()
app.exec()