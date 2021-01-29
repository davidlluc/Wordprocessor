import sys

from PyQt5.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QFormLayout,QLabel,QSlider, QDialogButtonBox, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import *

class columnwidth_dialog(QDialog):


    def __init__(self, table, tableformat,column, *args, **kwargs):

        QDialog.__init__(self, *args, **kwargs)

        # Create widgets
        self.setWindowTitle('Redim column')
        self.ttable=table
        self.ttableformat=tableformat
        self.tcolumn=column
        box = QVBoxLayout()
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(50)
        self.oldsize=50
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(5)
        box.addWidget(self.sl)
        self.sl.valueChanged.connect(self.valuechange)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok) 
        # adding action when form is accepted 
        self.buttonBox.accepted.connect(self.accept)
        mainLayout = QVBoxLayout() 
        mainLayout.addLayout(box)
        # adding button box to the layout 
        mainLayout.addWidget(self.buttonBox) 
        # setting layout 
        self.setLayout(mainLayout) 

    def valuechange(self):
        size = self.sl.value()
        columnWidth=self.ttableformat.columnWidthConstraints()
        cwidth=columnWidth[self.tcolumn]
        
        if size>self.oldsize :
            length=(cwidth.rawValue())+4
            columnWidth[self.tcolumn]= QTextLength(QTextLength.FixedLength, length)
            self.ttableformat.setColumnWidthConstraints(columnWidth)
            self.ttableformat.setWidth(QTextLength(QTextLength.FixedLength, self.ttableformat.width().rawValue()+4))
            self.ttable.setFormat(self.ttableformat)
        else:
            if cwidth.rawValue()>3 :
                length=(cwidth.rawValue())-4
                columnWidth[self.tcolumn]= QTextLength(QTextLength.FixedLength, length)
                self.ttableformat.setColumnWidthConstraints(columnWidth)
                self.ttableformat.setWidth(QTextLength(QTextLength.FixedLength, self.ttableformat.width().rawValue()-4))
                self.ttable.setFormat(self.ttableformat)
        self.oldsize=size

if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = columnwidth_dialog('100','100',1)
    form.show()
    sys.exit(app.exec_())