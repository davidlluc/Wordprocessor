import sys

from PyQt5.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QFormLayout,QLabel,QSpinBox, QDialogButtonBox, QCheckBox)
from PyQt5.QtCore import Qt

class createtable_dialog(QDialog):


    def __init__(self, *args, **kwargs):

        QDialog.__init__(self, *args, **kwargs)

        # Create widgets
        self.setWindowTitle('New Table')
        box = QVBoxLayout()
        self.layoutform = QFormLayout() 

        self.sp1 = QSpinBox()
        self.sp1.setMinimum(1)
        self.sp1.setMaximum(10)
        self.sp1.setValue(3)
        self.sp2 = QSpinBox()
        self.sp2.setMinimum(1)
        self.sp2.setMaximum(10)
        self.sp2.setValue(3)
        self.sp3 = QSpinBox()
        self.sp3.setMinimum(1)
        self.sp3.setMaximum(1000)
        self.sp3.setValue(500)
        # adding rows 
        self.layoutform.addRow(QLabel("Rows :"), self.sp1) 
        self.layoutform.addRow(QLabel("Columns :"), self.sp2) 
        self.layoutform.addRow(QLabel("Width: "), self.sp3) 
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
        return self.sp1.value(), self.sp2.value(), self.sp3.value()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = createtable_dialog()
    form.show()
    sys.exit(app.exec_())