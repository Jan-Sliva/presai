import sys, os, random
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent, QTimer, QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPen, QTabletEvent, QFont


class selectionLayout(QtWidgets.QVBoxLayout):

    def __init__(self):
        super().__init__()

    def processSelectionList(selectionOutputs, sendOutput):
            ret = {k: v() for k, v in selectionOutputs.items()}
            sendOutput(ret)

    def addSelectionButton(self, selectionOutputs, sendOutput, buttonText="Continue"):

        button = QPushButton(buttonText)
        button.clicked.connect(lambda: selectionLayout.processSelectionList(selectionOutputs, sendOutput))

        self.addWidget(button)

    def addLabel(self, text, fontSize):
        w = QLabel(text)
        font = w.font()
        font.setPointSize(fontSize)
        w.setFont(font)
        self.addWidget(w)

    def addSelection(self, selectionList, onChanged = None, triggerOnce = False):
        selectionOutputs = {}

        if onChanged != None:
            f = lambda: selectionLayout.processSelectionList(selectionOutputs, onChanged)
        else:
            f = lambda: None

        for item in selectionList:
            if "Input" in item["type"]:
                sub_layout = QtWidgets.QHBoxLayout()
                if "textBefore" in item:
                    sub_layout.addWidget(QLabel(item["textBefore"]))

                if item["type"] == "boolInput":
                    w = QCheckBox()
                    w.stateChanged.connect(f)
                    selectionOutputs[item["key"]] = w.isChecked
                elif item["type"] == "selectionInput":
                    w = QComboBox()
                    w.addItems(item["items"])
                    w.activated.connect(f)
                    selectionOutputs[item["key"]] = w.currentText
                elif item["type"] == "textInput":
                    w = QLineEdit()
                    w.setText(item.get("default", ""))
                    w.textChanged.connect(f)
                    selectionOutputs[item["key"]] = w.text
                elif item["type"] == "numberInput":
                    w = QSpinBox()
                    w.setMinimum(item.get("min", 0))
                    w.setMaximum(item.get("max", 99))
                    w.setValue(item.get("default", w.minimum()))
                    w.textChanged.connect(f)
                    selectionOutputs[item["key"]] = w.value
                
                sub_layout.addWidget(w)
                if "textAfter" in item:
                    sub_layout.addWidget(QLabel(item["textAfter"]))
                sub_layout.addStretch()
                self.addLayout(sub_layout)

            elif item["type"] == "text":
                self.addLabel(item["text"], item["fontSize"])

        if triggerOnce:
            f()
        
        return selectionOutputs

