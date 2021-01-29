from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys

class QFileDialogPreview(QFileDialog):
    def __init__(self, *args, **kwargs):
        QFileDialog.__init__(self, *args, **kwargs)
        #options allow to subclass native widget for managing layout and items delegate
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        box = QVBoxLayout()
        # bring back dimensions from native widgets and enlarge it
        self.setFixedSize(self.width() + 250, self.height())
        self.pixmap = QPixmap()
        self.mpPreview = QLabel("Preview", self)
        self.mpPreview.setFixedSize(250, 250)
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
        self.scalax=100
        self.scalay=100
        box.addWidget(self.sl)
        self.sl.valueChanged.connect(self.valuechange)
        box.addStretch()
        #assuming native widget manage a gridlayout 
        #layout added row 3 column 1 rowspan  comumn span 1
        self.layout().addLayout(box, 1, 3, 1, 1)

        self.currentChanged.connect(self.onChange)
        self.fileSelected.connect(self.onFileSelected)
        self.filesSelected.connect(self.onFilesSelected)

        self._fileSelected = None
        self._filesSelected = None

    def valuechange(self):
        size = self.sl.value()*2
        if not(self.pixmap.isNull()):
                self.scalax=self.pixmap.width()*(size/100)
                self.scalay=self.pixmap.height()*(size/100)
                self.pixmap2=self.pixmap.scaled(int(self.scalax), int(self.scalay), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.mpPreview.setPixmap(self.pixmap2)


    def onChange(self, path):
        self.sl.setValue(50)
        self.pixmap = QPixmap(path)
        if(self.pixmap.isNull()):
            self.mpPreview.setText("Preview")
        else:
            self.mpPreview.setPixmap(self.pixmap)
            self.scalax=self.pixmap.width()
            self.scalay=self.pixmap.height()

    def onFileSelected(self, file):
        self._fileSelected = file

    def onFilesSelected(self, files):
        self._filesSelected = files

    def getFileSelected(self):
        return self._fileSelected, self.scalax, self.scalay

    def getFilesSelected(self):
        return self._filesSelected

    ## For selecting a single file
    def openBtn_single_clicked(self):
    
        filedialog = QFileDialogPreview(self,"Open File",
            "","Image Files (*.png *.jpg *.jpeg)")
        filedialog.setFileMode(QFileDialog.ExistingFile)
        if filedialog.exec_() == QFileDialogPreview.Accepted:
            print(filedialog.getFileSelected())

        return


## For selecting multiple files
    def openBtn_multiple_clicked(self):
        filedialog = QFileDialogPreview(self,"Open File",
            "","PDF Files (*.pdf)")
        filedialog.setFileMode(QFileDialog.ExistingFiles)
        if filedialog.exec_() == QFileDialogPreview.Accepted:
            print(filedialog.getFilesSelected())

        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fileExplorer = QFileDialogPreview()
    fileExplorer .show()
    sys.exit(app.exec_())