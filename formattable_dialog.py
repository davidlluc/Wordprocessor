import sys
import os 
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QFormLayout,QLabel,QSpinBox, QDialogButtonBox, QCheckBox,QAction,QColorDialog,QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from formatcell_dialog import *

class formattable_dialog(formatcell_dialog):


    def __init__(self,width, *args, **kwargs):

        formatcell_dialog.__init__(self, *args, **kwargs)
        align= {'' : '', 'Left' : Qt.AlignLeft,'Center' : Qt.AlignCenter ,'Right' :Qt.AlignRight}
        self.setWindowTitle("Table Format")
        self.width=None
        self.sp = QSpinBox()
        self.sp.setMinimum(1)
        self.sp.setMaximum(1000)
        self.sp.setValue(width)
        self.sp.setSpecialValueText(' ')
        self.sp.valueChanged.connect(self.valuewidthchange) 
        self.layoutform.addRow(QLabel("Width: "), self.sp) 
        self.alignment = QComboBox()
        for x,y in align.items() :
            self.alignment.addItem(x,y)
        self.layoutform.addRow(QLabel("Alignment"), self.alignment) 

    def valuewidthchange(self):
        self.width=self.sp.value()

        
    def getvalue(self) :
        return self.borderline, self.bordercol, self.backgroundcol ,self.alignment.currentData(),self.width

if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = formattable_dialog(100)
    form.show()
    sys.exit(app.exec_())