import sys, os, random
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent, QTimer, QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPen, QTabletEvent, QFont
from PyQt5.QtWidgets import QLayout
from selectionLayout import selectionLayout


class mainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

    def setCentralLayout(self, layout: QLayout) -> None:
        w = QtWidgets.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)

    def setSelectionWithButton(self, selectionList, sendOutput, buttonText="Continue"):
        layout = selectionLayout()
        selectionOutputs = layout.addSelection(selectionList)   
        layout.addSelectionButton(selectionOutputs, sendOutput, buttonText)
        layout.addStretch()
        
        self.setCentralLayout(layout)
