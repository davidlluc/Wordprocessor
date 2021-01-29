import sys

from PyQt5.QtWidgets import (QLineEdit, QPushButton, QApplication, QVBoxLayout, QDialog, QFormLayout,QLabel,QSlider, QDialogButtonBox, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class scale_dialog(QDialog):


    def __init__(self,picture, dimx, dimy, *args, **kwargs):

        QDialog.__init__(self, *args, **kwargs)

        # Create widgets
        self.setWindowTitle('Redim picture')
        box = QVBoxLayout()
        self.mpPreview = QLabel(picture, self)
        self.pixmap = QPixmap(picture)
        self.pixmap2=self.pixmap.scaled(float(dimx), float(dimy), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.mpPreview.setPixmap(self.pixmap2)
        self.mpPreview.setFixedSize(600, 600)
        self.mpPreview.setAlignment(Qt.AlignCenter)
        self.mpPreview.setObjectName("labelPreview")
        self.mpPreview.setStyleSheet("background-color: white; border: 1px solid black;") 
        box.addWidget(self.mpPreview)
        self.sl = QSlider(Qt.Horizontal)
        self.sl.setMinimum(0)
        self.sl.setMaximum(100)
        self.sl.setValue(50)
        self.sl.setTickPosition(QSlider.TicksBelow)
        self.sl.setTickInterval(5)
        box.addWidget(self.sl)
        self.sl.valueChanged.connect(self.valuechange)
 
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) 
        # adding action when form is accepted 
        self.buttonBox.accepted.connect(self.accept)
        # addding action when form is rejected 
        self.buttonBox.rejected.connect(self.close) 
        mainLayout = QVBoxLayout()  
        mainLayout.addLayout(box)
        # adding button box to the layout 
        mainLayout.addWidget(self.buttonBox) 
        # setting lay out 
        self.setLayout(mainLayout) 

    def getvalue(self) :
        return self.scalax, self.scalay

    def valuechange(self):
        size = self.sl.value()*2
        
        if not(self.pixmap2.isNull()):
            self.scalax=self.pixmap2.width()*(size/100)
            self.scalay=self.pixmap2.height()*(size/100)

        self.pixmap3=self.pixmap2.scaled(int(self.scalax), int(self.scalay), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.mpPreview.setPixmap(self.pixmap3)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    form = scale_dialog('100','100')
    form.show()
    sys.exit(app.exec_())