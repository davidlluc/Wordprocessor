import sys
import os 
from PyQt5.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QFormLayout,QLabel,QSpinBox, QDialogButtonBox, QCheckBox,QAction,QColorDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor

class formatcell_dialog(QDialog):


    def __init__(self, *args, **kwargs):

        QDialog.__init__(self, *args, **kwargs)
        self.borderline=None
        self.setWindowTitle("Cell Format")
        # Create widgets
        self.box = QVBoxLayout()
        self.layoutform = QFormLayout() 
        self.sp1 = QSpinBox()
        self.sp1.setRange(-1,10)
        self.sp1.setSingleStep(1)
        self.sp1.setValue(-1)
        self.sp1.setSpecialValueText(' ')
        self.sp1.valueChanged.connect(self.valuechange)
        self.bordercolor_button = QPushButton("",self)
        self.backgroundcolor_button = QPushButton("",self)
        self.bordercolor_button.clicked.connect(self.bordercolor)
        self.backgroundcolor_button.clicked.connect(self.backgroundcolor)
        # adding rows 
        self.layoutform.addRow(QLabel("Borderline :"), self.sp1) 
        self.layoutform.addRow(QLabel("Bordercolor :"), self.bordercolor_button) 
        self.layoutform.addRow(QLabel("Backgroundcolor :"), self.backgroundcolor_button) 
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) 
        # adding action when form is accepted 
        self.buttonBox.accepted.connect(self.accept)
        # addding action when form is rejected 
        self.buttonBox.rejected.connect(self.close) 
        self.box.addLayout(self.layoutform)
        # adding button box to the layout 
        self.box.addWidget(self.buttonBox) 
        # setting layout 
        self.setLayout(self.box) 
        self.bordercol=None
        self.backgroundcol=None
        self.borderline=None


    def valuechange(self):
        self.borderline=self.sp1.value()

    def bordercolor(self):
        color_dialog=QColorDialog()
        if color_dialog.exec_() == QColorDialog.Accepted:
            self.bordercol = color_dialog.currentColor()
            qss = 'background-color: %s' % self.bordercol.name()
            self.bordercolor_button.setStyleSheet(qss)


    def backgroundcolor(self):
        color_dialog=QColorDialog()
        if color_dialog.exec_() == QColorDialog.Accepted:
            self.backgroundcol = color_dialog.currentColor()
            qss = 'background-color: %s' % self.backgroundcol.name()
            self.backgroundcolor_button.setStyleSheet(qss)

    def getvalue(self) :
        return self.borderline, self.bordercol, self.backgroundcol

if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = formatcell_dialog()
    form.show()
    sys.exit(app.exec_())