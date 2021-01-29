import sys
import os 
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QFormLayout,QLabel,QSpinBox, QDialogButtonBox, QCheckBox,QAction,QColorDialog,QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor,QPageLayout
from formatcell_dialog import *

class page_dialog(QDialog):


    def __init__(self,margins,orientation, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)
        orientpage= {'Portrait' : QPageLayout.Portrait,'Landscape' : QPageLayout.Landscape}

        self.sp = QSpinBox()
        self.sp.setMinimum(10)
        self.sp.setMaximum(100)
        self.sp.setValue(margins)
        self.box = QVBoxLayout()
        self.layoutform = QFormLayout() 
        self.layoutform.addRow(QLabel("Margins : "), self.sp) 
        self.orient = QComboBox()
        for x,y in orientpage.items() :
            self.orient.addItem(x,y)
        index = self.orient.findData(orientation)
        if index >= 0 :
            self.orient.setCurrentIndex(index)

        self.layoutform.addRow(QLabel("Orientation :"), self.orient) 
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) 
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close) 
        self.box.addLayout(self.layoutform)
        self.box.addWidget(self.buttonBox) 
        self.setLayout(self.box) 


        
    def getvalue(self) :
        return self.sp.value(),self.orient.currentData()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = page_dialog(20,'Landscape')
    form.show()
    sys.exit(app.exec_())