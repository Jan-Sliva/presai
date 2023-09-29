from PyQt5.QtWidgets import QApplication, QWidget
import sys
import mainWindow
from PyQt5.QtGui import QFont
import importlib.util

spec = importlib.util.spec_from_file_location("strategy", "strategies/outlineFirst/strategy.py")
strategy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(strategy)

font_size = 12
window_size = (700, 700)

custom_font = QFont()
custom_font.setPointSize(font_size)
QApplication.setFont(custom_font)


app = QApplication(sys.argv)
window = mainWindow.mainWindow()
window.setBaseSize(*window_size)


strat = strategy.strategy(window, "strategies/outlineFirst")

def sendOutput(text):
    for k, v in text.items():
        print(k + ": " + str(v))
    strat.setFirstPromptScreen()
    


window.setSelectionWithButton([{"key" : "bool1", "textAfter" : "OK", "type" : "boolInput"},
                               {"key" : "selection1", "textBefore" : "selection", "textAfter" : "letter", "type" : "selectionInput", "items" : ["A", "B", "C"]},
                               {"key" : "text1", "textBefore" : "Text: ", "textAfter" : "lol", "type" : "textInput"},
                               {"type" : "text", "text" : "cyrz kacyrz", "fontSize" : 50}], sendOutput)


window.resize(*window_size)
window.show()



app.exec_()


