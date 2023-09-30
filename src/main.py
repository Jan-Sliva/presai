from PyQt5.QtWidgets import QApplication, QWidget
import sys
import mainWindow
from PyQt5.QtGui import QFont
import importlib.util

spec = importlib.util.spec_from_file_location("strategy", "strategies/outlineFirst/strategy.py")
strat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(strat)

font_size = 12
window_size = (700, 700)

custom_font = QFont()
custom_font.setPointSize(font_size)
QApplication.setFont(custom_font)


app = QApplication(sys.argv)
window = mainWindow.mainWindow()
window.setBaseSize(*window_size)

window.setFirstScreen()

window.resize(*window_size)
window.show()



app.exec_()


