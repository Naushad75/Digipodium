from PyQt5.QtWidgets import *
import sys
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt

class Window(QWidget):
    def _init_(self):
        QWidget._init_(self)
        
        layout = QGridLayout()
        self.setLayout(layout)
        self.listwidget = QListWidget()
        files=os.listdir('motion_data')
        for i in files:
           self.listwidget.insertItem(0, i) 
       
        self.listwidget.clicked.connect(self.clicked)
        layout.addWidget(self.listwidget)

    def clicked(self, qmodelindex):
        item = self.listwidget.currentItem()
        print(item.text())

app = QApplication(sys.argv)
screen = Window()
screen.show()
sys.exit(app.exec_())