import sys, os, random, json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent, QTimer, QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPen, QTabletEvent, QFont
from selectionLayout import selectionLayout
import os.path as P


class strategy:

    def __init__(self, mainWindow, location) -> None:
        self.mainWindow = mainWindow
        self.location = location

        with open(P.join(self.location, "prompts/outline.txt"), encoding="utf-8") as f:
            self.outlinePrompt = f.read()
        

    def begin(self, par={}):
        selectionList = [{"type" : "text", "text" : "Set parameters", "fontSize" : 15},
                         {"type" : "textInput", "key" : "top", "textBefore" : "Topic:"},
                         {"type" : "numberInput", "key" : "len", "textBefore" : "Number of slides:", "default" : 10, "min" : 3},
                         {"type" : "textInput", "key" : "foc", "textBefore" : "Focus on:"},
                         {"type" : "textInput", "key" : "adj", "textBefore" : "Adjective (e.g. historical, detailed):"},
                         {"type" : "numberInput", "key" : "pointsMin", "textBefore" : "Minimum bullet point per slide:", "default" : 3, "min" : 2, "max" : 20},
                         {"type" : "numberInput", "key" : "pointsMax", "textBefore" : "Maximum bullet point per slide:", "default" : 7, "min" : 2, "max" : 20},
                         {"type" : "numberInput", "key" : "outlines", "textBefore" : "Number of outlines to choose from:", "default" : 3, "min" : 1, "max" : 5}
                        ]
        
        layout = selectionLayout()

        outlineWidget = QLabel()
        outlineWidget.setWordWrap(True)
        def updateOutlineWidget(selectionOutput):
            prompt = self.outlinePrompt.format(**selectionOutput)
            outlineWidget.setText(prompt)

        selectionOutputs = layout.addSelection(selectionList, updateOutlineWidget, True)
        
        layout.addStretch()

        layout.addLabel("First prompt to ask:", 15)

        layout.addWidget(outlineWidget)
        layout.addSelectionButton(selectionOutputs, self.predictOutlines)

        self.mainWindow.setCentralLayout(layout)
        
    def predictOutlines(self):
        pass