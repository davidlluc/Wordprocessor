import sys

from PyQt5.QtWidgets import (QComboBox, QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QFormLayout,QLabel,QSpinBox, QDialogButtonBox, QCheckBox,QComboBox)
from PyQt5.QtCore import Qt

class parasettings_dialog(QDialog):

    def __init__(self,StartIndent,MarginLeft,MarginRight,MarginBottom,MarginTop, *args, **kwargs):

        QDialog.__init__(self, *args, **kwargs)
        linespacing= {'Single' : 100,'1,5' : 150 ,'Double' :200}
        # Create widgets
        self.setWindowTitle('Paragraph settings')
        box = QVBoxLayout()
        self.layoutform = QFormLayout() 
        self.sp1 = QSpinBox()
        self.sp1.setMinimum(0)
        self.sp1.setMaximum(200)
        self.sp1.setValue(int(StartIndent))
        self.sp2 = QSpinBox()
        self.sp2.setMinimum(0)
        self.sp2.setMaximum(200)
        self.sp2.setValue(int(MarginLeft))
        self.sp3 = QSpinBox()
        self.sp3.setMinimum(0)
        self.sp3.setMaximum(200)
        self.sp3.setValue(int(MarginRight))
        self.sp4 = QSpinBox()
        self.sp4.setMinimum(0)
        self.sp4.setMaximum(200)
        self.sp4.setValue(int(MarginTop))
        self.sp5 = QSpinBox()
        self.sp5.setMinimum(0)
        self.sp5.setMaximum(200)
        self.sp5.setValue(int(MarginBottom))
        # adding rows 
        self.layoutform.addRow(QLabel("Start Indent :"), self.sp1) 
        self.layoutform.addRow(QLabel("Left Margin :"), self.sp2) 
        self.layoutform.addRow(QLabel("RightMargin : "), self.sp3) 
        self.layoutform.addRow(QLabel("TopMargin : "), self.sp4) 
        self.layoutform.addRow(QLabel("BottomMargin : "), self.sp5)
        self.linespace = QComboBox() 
        for x,y in linespacing.items() :
            self.linespace.addItem(x,y)
        self.layoutform.addRow(QLabel("Line Spacing"), self.linespace) 
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) 
        # adding action when form is accepted 
        self.buttonBox.accepted.connect(self.accept)
        # addding action when form is rejected 
        self.buttonBox.rejected.connect(self.close) 
        box.addLayout(self.layoutform)
        # adding button box to the layout 
        box.addWidget(self.buttonBox) 
        # setting layout 
        self.setLayout(box) 

    def getvalue(self) :
        return self.sp1.value(), self.sp2.value(), self.sp3.value(), self.sp4.value(),self.sp5.value(),self.linespace.currentData()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = parasettings_dialog()
    form.show()
    sys.exit(app.exec_())