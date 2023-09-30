import sys, os, random
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QEvent, QTimer, QRect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPen, QTabletEvent, QFont
from PyQt5.QtWidgets import QLayout
from selectionLayout import selectionLayout
import importlib.util
import os.path as P
import json

class mainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.strategy = None

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

    def setStrategy(self, params):
        spec = importlib.util.spec_from_file_location("strategy", P.join(params["strategyPath"], "strategy.py"))
        strat = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(strat)

        del self.strategy
        self.strategy = strat.strategy(self, params["strategyPath"])
        self.strategy.begin(params)
        
    def setFirstScreen(self):
        layout = selectionLayout()

        strategies_names = []
        strategies_dict = {}


        for dir in os.listdir("strategies"):
            strat_path = P.join("strategies", dir)
            info_file = P.join(strat_path, "info.json")
            with open(info_file, encoding="utf-8") as f:
                info = json.load(f)
            strategies_names.append(info["name"])
            strategies_dict[info["name"]] = {"description" : info["description"], "file" : strat_path}

        strategy_selection_list = [
            {"type" : "text", "text" : "Set parameters", "fontSize" : 15},
            {"key" : "strategy", "textBefore" : "selection", "textAfter" : "letter", "type" : "selectionInput", "items" : strategies_names}
        ]

        desc_label = QLabel()
        desc_label.setWordWrap(True)

        def updateDesc(params):
            desc_label.setText("Description of strategy: " + strategies_dict[params["strategy"]]["description"])
        
        strategy_selection_outputs = layout.addSelection(strategy_selection_list, updateDesc, triggerOnce=True)
        layout.addWidget(desc_label)

        param_selecton_list = [
            {"type" : "textInput", "key" : "title", "textBefore" : "Title: "},
            {"type" : "textInput", "key" : "subtitle", "textBefore" : "Subtitle: "},
            {"type" : "textInput", "key" : "folder", "textBefore" : "Folder: "},
            {"type" : "selectionInput", "key" : "lang", "textBefore" : "Language: ", "items" : ["CZECH", "ENGLISH"]},
        ]

        layout.addSelectionButton(strategy_selection_outputs, self.setStrategy, "Continue")
        layout.addStretch()

        self.setCentralLayout(layout)
