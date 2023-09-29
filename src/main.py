from PyQt5.QtWidgets import QApplication, QWidget
import sys
import mainWindow
import strategy
from PyQt5.QtGui import QFont

font_size = 12
window_size = (700, 700)

custom_font = QFont()
custom_font.setPointSize(font_size)
QApplication.setFont(custom_font)


app = QApplication(sys.argv)
window = mainWindow.mainWindow()
window.setBaseSize(*window_size)


strat = strategy.strategy(window)

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


