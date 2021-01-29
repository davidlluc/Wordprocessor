from PyQt5 import QtPrintSupport
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import treeview3
from treeview3 import *
from scale_dialog import *
from createtable_dialog import *
from page_dialog import *
from formattable_dialog import *
from formatcell_dialog import *
from columnwidth_dialog import *
from parasettings_dialog import *
import os
import sys
import uuid
import ast

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]
IMAGE_EXTENSIONS = ['.jpg','.png','.jpeg']
HTML_EXTENSIONS = ['.htm', '.html']
def hexuuid():
    return uuid.uuid4().hex

def splitext(p):
    #return extension. (index 0 : return path except extension)
    return os.path.splitext(p)[1].lower()

class TextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super(QTextEdit, self).__init__(*args, **kwargs)
       
    def canInsertFromMimeData(self, source):

        if source.hasImage():
            return True
        else:
            #bool value returned by textedit class)
            return super(TextEdit, self).canInsertFromMimeData(source)

    def insertFromMimeData(self, source):
        document=self.document()
        cursor = self.textCursor()

        if source.hasUrls():
            # return a list of expressions like : [PyQt5.QtCore.QUrl('file:///home/david/Bureau/python/qt/qaction/qaction.py')]
            for u in source.urls():
                file_ext = splitext(str(u.toLocalFile()))
                # str(u.toLocalFile()) : return a path : /home/david/Bureau/python/qt/qaction/qaction.py
                if u.isLocalFile() and file_ext in IMAGE_EXTENSIONS:
                    imageformat=QTextImageFormat()
                    imageformat.setName(u.toLocalFile())
                    document.addResource(QTextDocument.ImageResource, u, imageformat)
                    image = QImage(u.toLocalFile())
                    imageformat.setWidth(image.width())
                    imageformat.setHeight(image.height())
                    cursor.insertImage(imageformat)
                else:
                    # If we hit a non-image or non-local URL break the loop and fall out
                    # to the super call & let Qt handle it
                    break

            else:
                # If all were valid images, finish here.
                return

        elif source.hasImage():
            image = source.imageData()
            uuid = hexuuid()
            document.addResource(QTextDocument.ImageResource, uuid, image)
            cursor.insertImage(uuid)
            return

        super(TextEdit, self).insertFromMimeData(source)

#    def paintEvent(self,event) :
#        p=QPainter(self.viewport())
#        pen=QPen(Qt.gray, 1,Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)
#        p.setPen(pen)
#        p.drawRect(QRectF(0,0,100,100))
#        super(TextEdit, self).paintEvent(event)
        


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.orientation=QPageLayout.Portrait
        self.textmargins=12
        self.bordermargins=10
        self.adict=None
        layout = QVBoxLayout()
        self.editor = TextEdit()
        self.docu = self.editor.document()
        #Vlayout=self.docu.documentLayout()
        #Vlayout.documentSizeChanged.connect(self.sizechanged)
        #Vlayout.pageCountChanged.connect(self.pagechanged)
        # Setup the QTextEdit editor configuration
        self.editor.setAutoFormatting(QTextEdit.AutoAll)
        self.editor.selectionChanged.connect(self.selectionChanged)
        # Initialize default font size.
        font = QFont('DejaVu Serif', 12)
        self.editor.setFont(font)
        # We need to repeat the size to init the current format.
        self.editor.setFontPointSize(12)
        self.txtcolor=QColor('black')
        self.bckcolor=QColor('white')
        self.editor.setTextColor(self.txtcolor)
        self.editor.setTextBackgroundColor(self.bckcolor)
        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None
        layout.addWidget(self.editor)
        container = QWidget()
        container.setLayout(layout)
        #central widget : any widget can be.
        self.setCentralWidget(container)
        self.configureprinter()
        self.paginate()

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(QIcon(os.path.join('icons', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('icons', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('icons', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        topdf_action = QAction(QIcon(os.path.join('icons', 'document-pdf.png')), "Write to pdf...", self)
        topdf_action.setStatusTip("Write to pdf")
        topdf_action.triggered.connect(self.writetopdf)
        file_menu.addAction(topdf_action)
        file_toolbar.addAction(topdf_action)

        preview_action = QAction(QIcon(os.path.join('icons', 'preview.png')), "Preview...", self)
        preview_action.setStatusTip("Preview current page")
        preview_action.triggered.connect(self.file_preview)
        file_menu.addAction(preview_action)
        file_toolbar.addAction(preview_action)

        print_action = QAction(QIcon(os.path.join('icons', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        mpage_action = QAction(QIcon(os.path.join('icons', 'portrait.png')), "Mise en page...", self)
        mpage_action.setStatusTip("Mise en page")
        mpage_action.triggered.connect(self.pagedialog)
        file_menu.addAction(mpage_action)
        file_toolbar.addAction(mpage_action)


        quit_action = QAction(QIcon(os.path.join('icons', 'exit.png')), "Quit", self)
        quit_action.setStatusTip("Quit")
        quit_action.triggered.connect(self.close)
        file_toolbar.addAction(quit_action)
        file_menu.addAction(quit_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(QIcon(os.path.join('icons', 'arrow-curve-180-left.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('icons', 'arrow-curve.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join('icons', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.setShortcut(QKeySequence.Cut)
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('icons', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        cut_action.setShortcut(QKeySequence.Copy)
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('icons', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        cut_action.setShortcut(QKeySequence.Paste)
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('icons', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        cut_action.setShortcut(QKeySequence.SelectAll)
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(QIcon(os.path.join('icons', 'arrow-continue.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        self.addToolBarBreak()

        format_toolbar = QToolBar("Format")
        format_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(format_toolbar)
        format_menu = self.menuBar().addMenu("&Format")

        # We need references to these actions/settings to update as selection changes, so attach to self.
        self.fonts = QFontComboBox()
        self.fonts.currentFontChanged.connect(self.editor.setCurrentFont)
        format_toolbar.addWidget(self.fonts)

        self.fontsize = QComboBox()
        self.fontsize.addItems([str(s) for s in FONT_SIZES])

        # Connect to the signal producing the text of the current selection. Convert the string to float
        # and set as the pointsize. We could also use the index + retrieve from FONT_SIZES.
        self.fontsize.currentIndexChanged[str].connect(lambda s: self.editor.setFontPointSize(float(s)) )
        format_toolbar.addWidget(self.fontsize)

        self.bold_action = QAction(QIcon(os.path.join('icons', 'edit-bold.png')), "Bold", self)
        self.bold_action.setStatusTip("Bold")
        self.bold_action.setShortcut(QKeySequence.Bold)
        self.bold_action.setCheckable(True)
        self.bold_action.toggled.connect(lambda x: self.editor.setFontWeight(QFont.Bold if x else QFont.Normal))
        format_toolbar.addAction(self.bold_action)
        format_menu.addAction(self.bold_action)

        self.italic_action = QAction(QIcon(os.path.join('icons', 'edit-italic.png')), "Italic", self)
        self.italic_action.setStatusTip("Italic")
        self.italic_action.setShortcut(QKeySequence.Italic)
        self.italic_action.setCheckable(True)
        self.italic_action.toggled.connect(self.editor.setFontItalic)
        format_toolbar.addAction(self.italic_action)
        format_menu.addAction(self.italic_action)

        self.underline_action = QAction(QIcon(os.path.join('icons', 'edit-underline.png')), "Underline", self)
        self.underline_action.setStatusTip("Underline")
        self.underline_action.setShortcut(QKeySequence.Underline)
        self.underline_action.setCheckable(True)
        #self.underline_action.toggled.connect(self.editor.setFontUnderline)
        self.underline_action.toggled.connect(self.editor.setFontUnderline)
        format_toolbar.addAction(self.underline_action)
        format_menu.addAction(self.underline_action)

        format_menu.addSeparator()

        self.alignl_action = QAction(QIcon(os.path.join('icons', 'edit-alignment.png')), "Align left", self)
        self.alignl_action.setStatusTip("Align text left")
        self.alignl_action.setCheckable(True)
        self.alignl_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignLeft))
        format_toolbar.addAction(self.alignl_action)
        format_menu.addAction(self.alignl_action)

        self.alignc_action = QAction(QIcon(os.path.join('icons', 'edit-alignment-center.png')), "Align center", self)
        self.alignc_action.setStatusTip("Align text center")
        self.alignc_action.setCheckable(True)
        self.alignc_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignCenter))
        format_toolbar.addAction(self.alignc_action)
        format_menu.addAction(self.alignc_action)

        self.alignr_action = QAction(QIcon(os.path.join('icons', 'edit-alignment-right.png')), "Align right", self)
        self.alignr_action.setStatusTip("Align text right")
        self.alignr_action.setCheckable(True)
        self.alignr_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignRight))
        format_toolbar.addAction(self.alignr_action)
        format_menu.addAction(self.alignr_action)

        self.alignj_action = QAction(QIcon(os.path.join('icons', 'edit-alignment-justify.png')), "Justify", self)
        self.alignj_action.setStatusTip("Justify text")
        self.alignj_action.setCheckable(True)
        self.alignj_action.triggered.connect(lambda: self.editor.setAlignment(Qt.AlignJustify))
        format_toolbar.addAction(self.alignj_action)
        format_menu.addAction(self.alignj_action)

        format_group = QActionGroup(self)
        format_group.setExclusive(True)
        format_group.addAction(self.alignl_action)
        format_group.addAction(self.alignc_action)
        format_group.addAction(self.alignr_action)
        format_group.addAction(self.alignj_action)

        forec_action = QAction(QIcon(os.path.join('icons', 'paint-brush-color.png')), "Forecolor", self)
        forec_action.setStatusTip("Forecolor")
        #self.forec_action.setCheckable(True)
        forec_action.triggered.connect(self.textcolor)
        #self.forec_action.setObjectName('forec')
        format_toolbar.addAction(forec_action)
        format_menu.addAction(forec_action)
        #self.format_toolbar.widgetForAction(self.forec_action).setObjectName('forec')

        backc_action = QAction(QIcon(os.path.join('icons', 'paint-can-color.png')), "Backgroundcolor", self)
        backc_action.setStatusTip("Backgroundcolor")
        #self.forec_action.setCheckable(True)
        backc_action.triggered.connect(self.backcolor)
        #self.backc_action.setObjectName('backc')
        format_toolbar.addAction(backc_action)
        format_menu.addAction(backc_action)
        #self.format_toolbar.widgetForAction(self.backc_action).setObjectName('backc')

        para_toolbar = QToolBar("Paragraphe")
        para_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(para_toolbar)
        para_menu = self.menuBar().addMenu("&Paragraphe")
        indent_action = QAction(QIcon(os.path.join('icons', 'indent.png')), "Indent", self)
        indent_action.setStatusTip("Indent")
        indent_action.triggered.connect(self.indent)
        para_toolbar.addAction(indent_action)
        para_menu.addAction(indent_action)

        outdent_action = QAction(QIcon(os.path.join('icons', 'outdent.png')), "Outdent", self)
        outdent_action.setStatusTip("Outdent")
        outdent_action.triggered.connect(self.outdent)
        para_toolbar.addAction(outdent_action)
        para_menu.addAction(outdent_action)


        m_pActionGrpBlockList = QActionGroup(self)
        m_pActionGrpBlockList.setExclusive(True)
        ActionInsUnorderedList =QAction(self)
        #ActionInsUnorderedList.setCheckable(True)
        ActionInsUnorderedList.setText("Unordered List")
        ActionInsUnorderedList.setIcon(QIcon(os.path.join('icons', 'edit-list.png')))
        BtnInsUnorderedList = QToolButton(self)
        #self.BtnInsUnorderedList.triggered.connect(self.cancellist)
        para_toolbar.addWidget(BtnInsUnorderedList)
        BtnInsUnorderedList.setDefaultAction(ActionInsUnorderedList)
        #self.BtnInsUnorderedList.setCheckable(True)
        unordered_style= {'Disc' : QTextListFormat.ListDisc, 'Circle' :QTextListFormat.ListCircle,'Square' : QTextListFormat.ListSquare}
        pMenu = QMenu(self)
        for x,y in unordered_style.items() :
            self.unordered_act=QAction(self)
            self.unordered_act.setText(x)
            self.unordered_act.setData(y)
            self.unordered_act.setCheckable(True)
            self.unordered_act.triggered.connect(self.onsetstyle)
            pMenu.addAction(self.unordered_act)
            m_pActionGrpBlockList.addAction(self.unordered_act)
        BtnInsUnorderedList.setPopupMode(QToolButton.MenuButtonPopup)
        BtnInsUnorderedList.setMenu(pMenu)

        ActionInsorderedList =QAction(self)
        #ActionInsorderedList.setCheckable(True)
        ActionInsorderedList.setText("Ordered List")
        ActionInsorderedList.setIcon(QIcon(os.path.join('icons', 'edit-list-order.png')))
        BtnInsorderedList = QToolButton(self)
        #self.BtnInsUnorderedList.triggered.connect(self.cancellist)
        para_toolbar.addWidget(BtnInsorderedList)
        BtnInsorderedList.setDefaultAction(ActionInsorderedList)
        #self.BtnInsUnorderedList.setCheckable(True)
        ordered_style= {'Decimal' : QTextListFormat.ListDecimal, 'Lower Alpha' :QTextListFormat.ListLowerAlpha,'Upper Alpha' : QTextListFormat.ListUpperAlpha, 'Lower Roman' :QTextListFormat.ListLowerRoman,'Upper Roman' : QTextListFormat.ListUpperRoman}
        pMenu = QMenu(self)
        for x,y in ordered_style.items() :
            self.ordered_act=QAction(self)
            self.ordered_act.setText(x)
            self.ordered_act.setData(y)
            self.ordered_act.setCheckable(True)
            self.ordered_act.triggered.connect(self.onsetstyle)
            pMenu.addAction(self.ordered_act)
            m_pActionGrpBlockList.addAction(self.ordered_act)
        BtnInsorderedList.setPopupMode(QToolButton.MenuButtonPopup)
        BtnInsorderedList.setMenu(pMenu)

        setting_action = QAction("Settings", self)
        setting_action.setStatusTip("Settings")
        setting_action.triggered.connect(self.parasettings)
        #self.para_toolbar.addAction(self.outdent_action)
        para_menu.addAction(setting_action)

        self.addToolBarBreak()
        picture_toolbar = QToolBar("Image")
        picture_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(picture_toolbar)
        picture_menu = self.menuBar().addMenu("&Image")
        picture_action = QAction(QIcon(os.path.join('icons', 'picture.png')), "Insert picture", self)
        picture_action.setStatusTip("Insert a picture")
        picture_action.triggered.connect(self.insertpicture)
        picture_toolbar.addAction(picture_action)
        picture_menu.addAction(picture_action)

        self.scalepicture_action = QAction(QIcon(os.path.join('icons', 'scale_img.png')), "Resize picture", self)
        self.scalepicture_action.setStatusTip("Resize a picture")
        self.scalepicture_action.triggered.connect(self.scalepicture)
        self.scalepicture_action.setDisabled(True)
        picture_toolbar.addAction(self.scalepicture_action)
        picture_menu.addAction(self.scalepicture_action)

        table_toolbar = QToolBar("Table")
        table_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(table_toolbar)
        table_menu = self.menuBar().addMenu("&Table")
        inserttable_action = QAction(QIcon(os.path.join('icons', 'table.png')), "Insert Table", self)
        inserttable_action.setStatusTip("Insert table")
        inserttable_action.triggered.connect(self.inserttable)
        table_toolbar.addAction(inserttable_action)
        table_menu.addAction(inserttable_action)

        self.insertrow_action = QAction(QIcon(os.path.join('icons', 'table-insert-row.png')), "Insert row", self)
        self.insertrow_action.setStatusTip("Insert Row")
        self.insertrow_action.triggered.connect(self.insertrow)
        self.insertrow_action.setDisabled(True)
        table_toolbar.addAction(self.insertrow_action)
        table_menu.addAction(self.insertrow_action)

        self.deleterow_action = QAction(QIcon(os.path.join('icons', 'delete-row.png')), "Delete row", self)
        self.deleterow_action.setStatusTip("Delete Row")
        self.deleterow_action.triggered.connect(self.deleterow)
        self.deleterow_action.setDisabled(True)
        table_toolbar.addAction(self.deleterow_action)
        table_menu.addAction(self.deleterow_action)

        self.insertcol_action = QAction(QIcon(os.path.join('icons', 'table-insert-column.png')), "Insert col", self)
        self.insertcol_action.setStatusTip("Insert Col")
        self.insertcol_action.triggered.connect(self.insertcol)
        self.insertcol_action.setDisabled(True)
        table_toolbar.addAction(self.insertcol_action)
        table_menu.addAction(self.insertcol_action)

        self.deletecol_action = QAction(QIcon(os.path.join('icons', 'delete-col.png')), "Delete col", self)
        self.deletecol_action.setStatusTip("Delete Col")
        self.deletecol_action.triggered.connect(self.deletecol)
        self.deletecol_action.setDisabled(True)
        table_toolbar.addAction(self.deletecol_action)
        table_menu.addAction(self.deletecol_action)

        self.mergecell_action = QAction(QIcon(os.path.join('icons', 'table-join.png')), "Merge cells", self)
        self.mergecell_action.setStatusTip("Merge Cells")
        self.mergecell_action.triggered.connect(self.mergecell)
        self.mergecell_action.setDisabled(True)
        table_toolbar.addAction(self.mergecell_action)
        table_menu.addAction(self.mergecell_action)

        self.splitcell_action = QAction(QIcon(os.path.join('icons', 'table-split.png')), "Split cell", self)
        self.splitcell_action.setStatusTip("Split Cell")
        self.splitcell_action.triggered.connect(self.splitcell)
        self.splitcell_action.setDisabled(True)
        table_toolbar.addAction(self.splitcell_action)
        table_menu.addAction(self.splitcell_action)

        self.resizecolumn_action = QAction(QIcon(os.path.join('icons', 'resize-column.png')), "Resize column", self)
        self.resizecolumn_action.setStatusTip("Resize column")
        self.resizecolumn_action.triggered.connect(self.resizecolumn)
        self.resizecolumn_action.setDisabled(True)
        table_toolbar.addAction(self.resizecolumn_action)
        table_menu.addAction(self.resizecolumn_action)


        self.formatcell_action = QAction(QIcon(os.path.join('icons', 'table-pencil.png')), "Format Cell", self)
        self.formatcell_action.setStatusTip("FormatCell")
        self.formatcell_action.triggered.connect(self.formatcell)
        self.formatcell_action.setDisabled(True)
        table_toolbar.addAction(self.formatcell_action)
        table_menu.addAction(self.formatcell_action)

        self.formattable_action = QAction(QIcon(os.path.join('icons', 'table-draw.png')), "Format Table", self)
        self.formattable_action.setStatusTip("FormatTable")
        self.formattable_action.triggered.connect(self.formattable)
        self.formattable_action.setDisabled(True)
        table_toolbar.addAction(self.formattable_action)
        table_menu.addAction(self.formattable_action)

        about_menu = self.menuBar().addMenu("&?")
        about_action=QAction('&About',self)
        about_menu.addAction(about_action)
        about_action.triggered.connect(self.about)
        # A list of all format-related widgets/actions, so we can disable/enable signals when updating.
        self._format_actions = [
            self.fonts,
            self.fontsize,
            self.bold_action,
            self.italic_action,
            self.underline_action,
            #self.forec_action,
            #self.backc_action
            # We don't need to disable signals for alignment, as they are paragraph-wide.
        ]

        # Initialize.
        self.update_format()
        self.update_title()
        self.show()

#    def handle(self) :
#        self.paginate()

#    def cancellist(self) :
#        if self.BtnInsUnorderedList.isChecked()==False :
#            cursor=self.editor.textCursor()
#            currentList=cursor.currentList()
#            currentBlock = cursor.block()
#            currentList.remove(currentBlock)
#            blockFormat = cursor.blockFormat()
#            blockFormat.setIndent(0)
#            cursor.setBlockFormat(blockFormat)

    def onsetstyle(self):
        cursor=self.editor.textCursor()
        paction=self.unordered_act.sender()
        #style= self.unordered_act.data()
        style=paction.data()
        cursor.createList(style)

    def parasettings(self):
        cursor=self.editor.textCursor()
        fmt=QTextBlockFormat(cursor.blockFormat())
        StartIndent =fmt.textIndent()
        MarginLeft = fmt.leftMargin()
        MarginRight = fmt.rightMargin()
        MarginTop = fmt.topMargin()
        MarginBottom = fmt.bottomMargin()
        paraset_dialog=parasettings_dialog(StartIndent,MarginLeft,MarginRight,MarginBottom,MarginTop)
        if paraset_dialog.exec_() == paraset_dialog.Accepted :
            StartIndent, MarginLeft, MarginRight, MarginTop, MarginBottom, linespace= paraset_dialog.getvalue()
            fmt.setTextIndent(StartIndent)
            fmt.setLeftMargin(MarginLeft)
            fmt.setRightMargin(MarginRight)
            fmt.setTopMargin(MarginTop)
            fmt.setBottomMargin(MarginBottom)
            fmt.setLineHeight(linespace,QTextBlockFormat.ProportionalHeight)
            cursor.mergeBlockFormat(fmt)

    def indent(self) :
        cursor=self.editor.textCursor()
        fmt=cursor.blockFormat()
        fmt.setIndent(fmt.indent()+ 1)
        cursor.mergeBlockFormat(fmt)

    def outdent(self) :
        cursor=self.editor.textCursor()
        fmt=cursor.blockFormat()
        if fmt.indent()>0 :
            fmt.setIndent(fmt.indent()- 1)
            cursor.mergeBlockFormat(fmt)

    def textcolor(self):
        color_dialog=QColorDialog(self.txtcolor)
        if color_dialog.exec_() == QColorDialog.Accepted:
            self.txtcolor = color_dialog.currentColor()
            #qss = "QToolButton#forec { background-color: %s;border-radius: 1px;}" % self.txtcolor.name() 
            #qss2 = "QToolButton#backc { background-color: %s;border-radius: 1px;}" % self.bckcolor.name()
            #self.format_toolbar.setStyleSheet(qss+qss2)
            self.editor.setTextColor(self.txtcolor)

    def backcolor(self):
        color_dialog=QColorDialog(self.bckcolor)
        if color_dialog.exec_() == QColorDialog.Accepted:
            self.bckcolor = color_dialog.currentColor()
            #qss2 = "QToolButton#forec { background-color: %s;border-radius: 1px;}" % self.txtcolor.name() 
            #qss = "QToolButton#backc { background-color: %s;border-radius: 1px;}" % self.bckcolor.name()
            #self.format_toolbar.setStyleSheet(qss2+qss)
            self.editor.setTextBackgroundColor(self.bckcolor)


#    def sizechanged(self) :
#        self.paginate()

#    def pagechanged(self) :
#        print ('pagecountChanged')

#    def resizeEvent(self, event) :
#        self.paginate()
#        return super().resizeEvent(event)

#    def togglehtml(self) :
#        str=self.editor.toHtml()
#        self.editor.clear()
#        self.editor.insertHtml(str)

    def selectionChanged(self) :  #cursorpositionchanged
        self.updatewidgets()
        self.update_format()

    def updatewidgets(self) :
        cursor=self.editor.textCursor()
        if (cursor.charFormat().isValid() and cursor.hasSelection()and cursor.charFormat().isImageFormat()):
            self.scalepicture_action.setDisabled(False)
            self.pwidth = cursor.charFormat().toImageFormat().width()
            self.pheight = cursor.charFormat().toImageFormat().height()
            self.namepicture=cursor.charFormat().toImageFormat().name()
        else:
            self.scalepicture_action.setDisabled(True)

        table=cursor.currentTable()
        if (table) :
            self.insertcol_action.setDisabled(False)
            self.insertrow_action.setDisabled(False)
            self.mergecell_action.setDisabled(False)
            self.splitcell_action.setDisabled(False)
            self.formattable_action.setDisabled(False)
            self.formatcell_action.setDisabled(False)
            self.resizecolumn_action.setDisabled(False)
            self.deletecol_action.setDisabled(False)
            self.deleterow_action.setDisabled(False)
        else:
            self.insertcol_action.setDisabled(True)
            self.insertrow_action.setDisabled(True)
            self.mergecell_action.setDisabled(True)
            self.splitcell_action.setDisabled(True)
            self.formattable_action.setDisabled(True)
            self.formatcell_action.setDisabled(True)
            self.resizecolumn_action.setDisabled(True)
            self.deletecol_action.setDisabled(True)
            self.deleterow_action.setDisabled(True)

    def block_signals(self, objects, b):
        for o in objects:
            o.blockSignals(b)

    def update_format(self):
        """
        Update the font format toolbar/actions when a new text selection is made. This is neccessary to keep
        toolbars/etc. in sync with the current edit state.
        :return:
        """
        # Disable signals for all format widgets, so changing values here does not trigger further formatting.
        self.block_signals(self._format_actions, True)

        self.fonts.setCurrentFont(self.editor.currentFont())
        # Nasty, but we get the font-size as a float but want it was an int
        self.fontsize.setCurrentText(str(int(self.editor.fontPointSize())))
        #qss1 = "QToolButton#forec { background-color: %s ;border-radius: 1px;}" % self.editor.textColor().name()
        #qss = "QToolButton#backc { background-color: %s ;border-radius: 1px;}" % self.editor.textBackgroundColor().name()
        #self.format_toolbar.setStyleSheet(qss1+qss)
        self.italic_action.setChecked(self.editor.fontItalic())
        self.underline_action.setChecked(self.editor.fontUnderline())
        self.bold_action.setChecked(self.editor.fontWeight() == QFont.Bold)

        self.alignl_action.setChecked(self.editor.alignment() == Qt.AlignLeft)
        self.alignc_action.setChecked(self.editor.alignment() == Qt.AlignCenter)
        self.alignr_action.setChecked(self.editor.alignment() == Qt.AlignRight)
        self.alignj_action.setChecked(self.editor.alignment() == Qt.AlignJustify)

        self.block_signals(self._format_actions, False)

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        filters = "Text files (*.txt);;HTML documents (*.html);;All files (*.*)"
        selected_filter = "All files (*.*)"
        path, _ = QFileDialog.getOpenFileName(self, " Open file ", "", filters, selected_filter)
        if path :
            try:
                count = len(open(path).readlines(  ))
                with open(path, 'r') as f:
                    text = [next(f) for x in range(count-1)]
                    text2=next(f)

            except Exception as e:
                self.dialog_critical('File IO error')

            else:
                str=""    
                str=str.join(text)
                if self.adict :
                    self.adict=ast.literal_eval(text2)
                    self.orientation=self.adict['orientation']
                    self.textmargins=self.adict['textmargins']
                self.path = path
                # Qt will automatically try and guess the format as txt/html
                self.editor.clear()
                self.editor.setHtml(str)
                self.docu=self.editor.document()
                self.update_title()
 
                self.miseenpage()


    def insertpicture(self) :
        path=""
        filedialog = QFileDialogPreview(self,"Open File","","Image Files (*.png *.jpg *.jpeg)")
        filedialog.setFileMode(QFileDialog.ExistingFile)
        if filedialog.exec_() == QFileDialogPreview.Accepted:
            path, scalax, scalay=filedialog.getFileSelected()
        cursor = self.editor.textCursor()
        try:
            if path :
                imageformat=QTextImageFormat()
                imageformat.setName(path)
                imageformat.setWidth(scalax)
                imageformat.setHeight(scalay)
                cursor.insertImage(imageformat)
        except Exception as e:
            self.dialog_critical(str(e))

    def scalepicture(self):
        scaledialog=scale_dialog(self.namepicture, str(self.pwidth),str(self.pheight))
        if scaledialog.exec_() == scale_dialog.Accepted :
            scalax, scalay = scaledialog.getvalue()
            cursor = self.editor.textCursor()
            imgf=cursor.charFormat().toImageFormat()
            imgf.setWidth(float(scalax))
            imgf.setHeight(float(scalay))
            cursor.setCharFormat(imgf)

    def rotatepicture(self):
        print("rotate")

    def inserttable(self) :
        inserttable_dialog=createtable_dialog()
        if inserttable_dialog.exec_() == inserttable_dialog.Accepted :
            row, col, totalwidth = inserttable_dialog.getvalue()
            cursor = self.editor.textCursor()
            tableformat=QTextTableFormat()
            tableformat.setBorderCollapse(True)
            tableformat.setBorder(0)
            tableformat.setCellSpacing(0)
            tableformat.setCellPadding(3)
            tableformat.setWidth(QTextLength(QTextLength.FixedLength, totalwidth))
            fixedwidth=int(totalwidth/col)
            columnWidth=[QTextLength()]
            columnWidth.clear()
            for i in range(0,col) :
                columnWidth.append(QTextLength(QTextLength.FixedLength, fixedwidth))
            tableformat.setColumnWidthConstraints(columnWidth)
            cursor.insertTable(row,col, tableformat)
            table=cursor.currentTable()
            cursor.beginEditBlock()
            for r in range (row) :
                for c in range(col) :
                    cell = table.cellAt(r,c)
                    cell.firstCursorPosition().insertText(" ")
                    cellformat=cell.format().toTableCellFormat()
                    cellformat.setBackground(QColor('white'))
                    cellformat.setBorderBrush(QColor('black'))
                    cellformat.setBorder(1)
                    cellformat.setBorderStyle(QTextFrameFormat.BorderStyle_Solid)
                    cell.setFormat(cellformat)
            cursor.endEditBlock()

    def insertrow(self) :
        cursor = self.editor.textCursor()
        table=cursor.currentTable()
        if (table) :
            existingcell = QTextTable.cellAt(table,cursor)
            cellrow = existingcell.row()
            table.insertRows(cellrow,1)
            for x in range(table.columns()) :
                cell = table.cellAt(cellrow,x)
                cell.firstCursorPosition().insertText(" ")

    def deleterow(self) :
        cursor = self.editor.textCursor()
        table=cursor.currentTable()
        if (table) :
            existingcell = QTextTable.cellAt(table,cursor)
            cellrow = existingcell.row()
            cellcol=existingcell.column()
            for cell in range(cellcol) :
                cell = table.cellAt(cellrow,cellcol)
                table.splitCell(cellrow, cellcol,1,1)
            table.removeRows(cellrow,1)

    def insertcol(self) :
        cursor = self.editor.textCursor()
        table=cursor.currentTable()
        if (table) :
            existingcell = QTextTable.cellAt(table,cursor)
            cellcol = existingcell.column()
            table.insertColumns(cellcol,1)
            for x in range(table.rows()) :
                cell = table.cellAt(x,cellcol)
                cell.firstCursorPosition().insertText(" ")


    def deletecol(self) :
        cursor = self.editor.textCursor()
        table=cursor.currentTable()
        if (table) :
            existingcell = QTextTable.cellAt(table,cursor)
            cellcol = existingcell.column()
            cellrow=existingcell.row()
            for cell in range(cellrow) :
                cell = table.cellAt(cellrow,cellcol)
                table.splitCell(cellrow, cellcol,1,1)
            table.removeColumns(cellcol,1)
    
    def mergecell(self):
        cursor = self.editor.textCursor()
        table=cursor.currentTable()
        if (table) :
            table.mergeCells(cursor)

    def splitcell(self):
        cursor = self.editor.textCursor()
        table=cursor.currentTable()
        if (table) :
            existingcell = QTextTable.cellAt(table,cursor)
            table.splitCell(existingcell.row(), existingcell.column(),1,1)

    def formatcell(self) :
        cursor = self.editor.textCursor()
        table=cursor.currentTable()
        selectedcells = cursor.selectedTableCells()
        if not(cursor.hasSelection()) :
            existingcell = QTextTable.cellAt(table,cursor)
            selectedcells = existingcell.row(), 1,existingcell.column(),1
        formatcell_dlg=formatcell_dialog()
        if formatcell_dlg.exec_() == formatcell_dialog.Accepted :
            borderline, bordercolor, backgroundcolor = formatcell_dlg.getvalue()
            cursor.beginEditBlock()
            for r in range (selectedcells[0],selectedcells[0] + selectedcells[1]) :
                for c in range(selectedcells[2],selectedcells[2] + selectedcells[3]) :
                    cell = table.cellAt(r,c)
                    cellformat=cell.format().toTableCellFormat()
                    if backgroundcolor :
                        cellformat.setBackground(backgroundcolor)
                    if borderline!=None:
                        cellformat.setBorder(borderline)
                    if bordercolor :
                        cellformat.setBorderBrush(bordercolor)
                    cell.setFormat(cellformat)
            cursor.endEditBlock()
               
    def formattable(self):
        cursor = self.editor.textCursor()
        table=cursor.currentTable()   
        if (table) :
            tableformat=table.format()
            formattable_dlg=formattable_dialog(tableformat.width().rawValue())
            if formattable_dlg.exec_() == formattable_dialog.Accepted :
                borderline, bordercolor, backgroundcolor,align, totalwidth= formattable_dlg.getvalue()
                cursor.beginEditBlock()
                for r in range (0,table.rows()) :
                    for c in range(0,table.columns()) :
                        cell = table.cellAt(r,c)
                        cellformat=cell.format().toTableCellFormat()
                        if backgroundcolor :
                            cellformat.setBackground(backgroundcolor)

                        if borderline!=None :
                            cellformat.setBorder(borderline)
                        if bordercolor :
                            cellformat.setBorderBrush(bordercolor)
                        cell.setFormat(cellformat)
                cursor.endEditBlock()
                if totalwidth:
                    tableformat.clearColumnWidthConstraints()
                    tableformat.setWidth(QTextLength(QTextLength.FixedLength, totalwidth))
                    fixedwidth=int(totalwidth/table.columns())
                    columnWidth=[QTextLength()]
                    columnWidth.clear()
                    for i in range(0,table.columns()) :
                        columnWidth.append(QTextLength(QTextLength.FixedLength, fixedwidth))
                        tableformat.setColumnWidthConstraints(columnWidth)
                if align :
                    tableformat.setAlignment(Qt.AlignmentFlag(align))
                table.setFormat(tableformat)

    def resizecolumn(self) :
        cursor = self.editor.textCursor()
        table=cursor.currentTable() 
        if (table) :
            actualcell = QTextTable.cellAt(table,cursor)
            actualcolumn=actualcell.column()
            tableformat=table.format()
            resizecolumn_dlg=columnwidth_dialog(table,tableformat,actualcolumn)
            resizecolumn_dlg.exec_()
            
    def file_save(self):
        self.adict = {"orientation" : self.orientation, "textmargins" : self.textmargins}
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()
        text = self.editor.toHtml() if splitext(self.path) in HTML_EXTENSIONS else self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
                f.write('\n')
                f.write("%s" %(self.adict))

        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        filters = "Text files (*.txt);;HTML documents (*.html);;All files (*.*)"
        selected_filter = "All files (*.*)"
        self.path, _ = QFileDialog.getSaveFileName(self, " Save file ", "", filters, selected_filter)
        if self.path is None:
            return
        self.file_save()
        self.update_title()

    def handlePaintRequest(self, printer):
        painter=QPainter(printer)
        firstPage = True
        pgeCount=self.docu.pageCount()
        for page in range(pgeCount) :
            if not(firstPage):
                printer.newPage()
            self.paintPage(page,printer,painter)
            firstPage = False
        painter.end()

    def paintPage(self,page,printer,painter) :
        mmtopixels=self.bordermargins*0.0039370147*printer.resolution()
        pagesize=QSizeF(printer.paperRect().size())
        borderRect=QRect(int(mmtopixels),int(mmtopixels),int(pagesize.width()-2*mmtopixels),int(pagesize.height()-2*mmtopixels))
        tmtopixels= self.textmargins*0.0039370147*printer.resolution()
        textrect=QRectF(tmtopixels,tmtopixels,pagesize.width()-2*tmtopixels,pagesize.height()-2*tmtopixels)
        self.docu.setPageSize(textrect.size())
        painter.drawRect(borderRect)
        painter.save()
        textpageRect=QRectF(0,page*self.docu.pageSize().height(), self.docu.pageSize().width(),self.docu.pageSize().height())
        painter.setClipRect(textrect)
        painter.translate(0,-textpageRect.top())
        painter.translate(textrect.left(),textrect.top())
        self.docu.drawContents(painter)
        painter.restore()
#        footerHeight = painter.fontMetrics().height()
#        footerRect = QRectF(textrect)
#        footerRect.setTop(textrect.bottom())
#        footerRect.setHeight(footerHeight)
#       if page == self.pageCount - 1 :
#           painter.drawText(footerRect, Qt.AlignCenter, "Fin ")
#      else :
#        painter.drawText(footerRect, Qt.AlignVCenter | Qt.AlignRight, "Page {}".format(page+1))

        #self.editor.render(QPainter(printer))

    def paginate (self) :
        mmtopixels=self.bordermargins*0.0039370147*self.printer.resolution()
        pagesize=QSizeF(self.printer.paperRect().size())
        tmtopixels= self.textmargins*0.0039370147*self.printer.resolution()
        textRect=QRectF(tmtopixels,tmtopixels,pagesize.width()-2*tmtopixels,pagesize.height()-2*tmtopixels)
        self.docu.setPageSize(textRect.size())
        self.docu.setDocumentMargin(self.textmargins)

    def configureprinter (self) :
        printerList=QPrinterInfo.availablePrinters()
        self.printer=QPrinter()
        self.printer.setPrinterName(printerList[0].printerName())
        self.printer.setPageOrientation(self.orientation)
        self.printer.setPageMargins(self.textmargins,self.textmargins,self.textmargins,self.textmargins, QPrinter.Millimeter)
        self.printer.setFullPage(True)

    def pagedialog(self):
        page_dlg=page_dialog(self.textmargins,self.orientation)   
        if page_dlg.exec_() == page_dialog.Accepted : 
            self.textmargins,self.orientation= page_dlg.getvalue()  
            self.miseenpage()
    
    def miseenpage(self):
            self.printer.setPageOrientation(self.orientation)       
            self.paginate()
            self.resize(int(self.docu.pageSize().width()),int(self.docu.pageSize().height()))
            self.printer.setPageMargins(self.textmargins,self.textmargins,self.textmargins,self.textmargins, QPrinter.Millimeter)

    def writetopdf(self) :
        self.paginate()
        printer= QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        filename, _ = QFileDialog.getSaveFileName(self, 'Save to PDF')
        if filename:
            printer.setOutputFileName(filename)
            printer.setPageOrientation(self.orientation)    
            printer.setFullPage(True)
            firstPage = True
            pageCount=self.docu.pageCount()
            painter=QPainter(printer)
            for page in range(pageCount) :
                if not(firstPage):
                    printer.newPage()
                self.paintPage(page,printer,painter)
                firstPage = False
            painter.end()

    def file_preview(self):
        self.paginate()
        dialog = QtPrintSupport.QPrintPreviewDialog(self.printer)
        dialog.paintRequested.connect(lambda :self.handlePaintRequest(self.printer))
        dialog.exec_()
        
    def file_print(self):
        self.paginate()
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer(self.printer))

    def update_title(self):
        self.setWindowTitle("%s" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )

    def about(self) :
        dlg = QMessageBox(self)
        dlg.setText('Based on :\nMegasolid Idiom Editor project\n Easy Editor project\nand others contributions')
        dlg.setIcon(QMessageBox.Information)
        dlg.show()

    def closeEvent(self, event):
        if self.docu.isModified() :
            quit_msg = "Save before exit?"
            reply = QMessageBox.question(self, 'Message',quit_msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.No:
                event.accept()
            else:
                self.file_save()
                event.accept()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("Dad's TT")
    window = MainWindow()
    window.resize(800,600)
    size_ecran = QDesktopWidget().screenGeometry()
    size_fenetre = window.geometry()
    window.move(int((size_ecran.width()-size_fenetre.width())/2), int((size_ecran.height()-size_fenetre.height())/2))
    app.exec_()

