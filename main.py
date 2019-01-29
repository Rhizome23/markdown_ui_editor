import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTextEdit, QDialog, QApplication, QMessageBox
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrintDialog, QPrinter

import ui_editor

import mistune
import css
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


# Highlight code section with Pygment
class HighlightRenderer(mistune.Renderer):

    def block_code(self, code, lang):
        lang = 'python'
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


class TextEditor(QtWidgets.QMainWindow, ui_editor.Ui_MainWindow):

    def __init__(self, parent=None):
        super(TextEditor, self).__init__(parent)

        self.filename = " "
        self.initUI()

    def initUI(self):
        # Set up the user interface from Designer. Create a inputText object
        self.setupUi(self)

        self.setWindowIcon(QtGui.QIcon("icons/app_icon.png"))

        self.title=" MD Writer"

        # Set up a title
        self.setWindowTitle(self.title)
        # x and y coordinates on the screen, width, height
        self.setGeometry(100, 100, 1030, 800)

        self.inputText.textChanged.connect(self.convert)


        # Connect up the buttons.
        self.actionOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionNew.triggered.connect(self.new)
        self.actionPrint.triggered.connect(self.print)
        self.actionPrintPreview.triggered.connect(self.preview)
        self.actionExportPDF.triggered.connect(self.pdf)
        self.actionUndo.triggered.connect(self.inputText.undo)
        self.actionRedo.triggered.connect(self.inputText.redo)
        self.actionBold.triggered.connect(self.bold)
        self.actionInsertline.triggered.connect(self.insertline)
        self.actionItalic.triggered.connect(self.italic)
        self.actionH1.triggered.connect(self.H1)
        self.actionH2.triggered.connect(self.H2)
        self.actionH3.triggered.connect(self.H3)
        self.actionIndent.triggered.connect(self.indent)
        self.actionInsertBlockquotes.triggered.connect(self.insertblockquotes)
        self.actionInsertLink.triggered.connect(self.link)
        self.actionList.triggered.connect(self.list)
        self.actionNumbererList.triggered.connect(self.numbererlist)
        self.actionInsertImage.triggered.connect(self.image)

    def new(self):
        spawn = TextEditor(self)
        spawn.show()

    def open(self):
        # Get filename and show only .md files
        self.filename = QFileDialog.getOpenFileName(self, 'Open File', ".", "(*.md)")[0]
        if self.filename :
            with open(self.filename, "rt") as file:
                self.setWindowTitle(self.title + " - " + self.parseFileName())
                self.inputText.setText(file.read())

    def save(self):
        # Only open dialog if there is no filename yet
        if self.filename == " ":
            self.filename = QFileDialog.getSaveFileName(self, 'Save File')[0]

        # Append extension if not there yet
        if not self.filename.endswith(".md"):
            self.filename += ".md"

        # We just store the contents of the text file along with the format in PlainText
        with open(self.filename, "wt") as file:
            file.write(self.inputText.toPlainText())
            self.statusbar.showMessage(self.parseFileName() + " saved")
            self.setWindowTitle(self.title + " - " + self.parseFileName())

    def preview(self):
        preview = QPrintPreviewDialog()
        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.outputText.print_(p))
        preview.exec_()

    def print(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.outputText.document().print_(dialog.printer())

    def pdf(self):
        self.filename = QFileDialog.getSaveFileName(self,
                                                    self.tr("Export document to PDF"),
                                                    "", self.tr("PDF files (*.pdf)"))[0]
        if self.filename:
            # Append extension if not there yet
            if not self.filename.endswith(".pdf"):
                self.filename += ".pdf"
            printer = QPrinter()
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(self.filename)
            self.outputText.document().print(printer)

    def bold(self):
        cursor = self.inputText.textCursor()
        if cursor.hasSelection():
            alpha = cursor.selectedText()
            beta = '**' + alpha + '**'
            cursor.insertText(beta)
        else:
            QMessageBox.about(self, "Message", "Please select some text")

    def italic(self):
        cursor = self.inputText.textCursor()
        if cursor.hasSelection():
            alpha = cursor.selectedText()
            beta = '*' + alpha + '*'
            cursor.insertText(beta)
        else:
            QMessageBox.about(self, "Message", "Please select some text")

    def H1(self):
        cursor = self.inputText.textCursor()
        alpha = cursor.selectedText()
        beta = '#' + alpha
        cursor.insertText(beta)

    def H2(self):
        cursor = self.inputText.textCursor()
        alpha = cursor.selectedText()
        beta = '##' + alpha
        cursor.insertText(beta)

    def H3(self):
        cursor = self.inputText.textCursor()
        alpha = cursor.selectedText()
        beta = '###' + alpha
        cursor.insertText(beta)

    def list(self):
        cursor = self.inputText.textCursor()
        # start = cursor.blockNumber()
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()
            # Move to the selection's last line
            cursor.setPosition(cursor.selectionEnd())
            # Calculate range of selection
            diff = cursor.blockNumber() - temp
            # Iterate over lines
            for n in range(diff + 1):
                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                # Insert tabbing
                cursor.insertText("- ")
                # And move back up
                cursor.movePosition(QtGui.QTextCursor.Up)
        # If there is no selection, just insert a new line and tab
        else:
            QMessageBox.about(self, "Message", "Please select one or more lines")

    def numbererlist(self):
        cursor = self.inputText.textCursor()
        # start = cursor.blockNumber()
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()
            # Move to the selection's last line
            cursor.setPosition(cursor.selectionEnd())
            # Calculate range of selection
            diff = cursor.blockNumber() - temp
            # Iterate over lines
            for n in range(diff + 1):
                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                # Insert tabbing
                cursor.insertText("1. ")
                # And move back up
                cursor.movePosition(QtGui.QTextCursor.Up)
        # If there is no selection, just insert a new line and tab
        else:
            QMessageBox.about(self, "Message", "Please select one or more lines")

    def indent(self):
        # Grab the cursor
        cursor = self.inputText.textCursor()
        # start = cursor.blockNumber()
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()
            # Move to the selection's last line
            cursor.setPosition(cursor.selectionEnd())
            # Calculate range of selection
            diff = cursor.blockNumber() - temp
            # Iterate over lines
            for n in range(diff + 1):
                # Move to start of each line
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                # Insert tabbing
                cursor.insertText("\t")
                # And move back up
                cursor.movePosition(QtGui.QTextCursor.Up)
        # If there is no selection, just insert a tab
        else:
            cursor.insertText("\t")
        # Add a line at the top of indent paragraph for mardown render
        cursor.insertText("\n")

    def link(self):
        cursor = self.inputText.textCursor()
        if cursor.hasSelection():
            alpha = cursor.selectedText()
            beta = '[' + alpha + ']' + '(' + alpha + ')'
            cursor.insertText(beta)
        else:
            QMessageBox.about(self, "Message", "Please select a link")


    def insertline(self):
        cursor = self.inputText.textCursor()
        cursor.insertBlock()
        cursor.insertText("\n --- \r")

    def insertblockquotes(self):
        cursor = self.inputText.textCursor()
        alpha = cursor.selectedText()
        beta = '\n >' + alpha
        cursor.insertText(beta)

    def image(self):
        # Grab the cursor
        cursor = self.inputText.textCursor()
        self.imgfilename = QFileDialog.getOpenFileName(self, 'Insert an image link', "/home", "*")[0]
        if self.imgfilename != "":
            file = open(self.imgfilename, "r")
            file.close()
        image_path = self.imgfilename
        url_image = "![alt text](" + image_path + ")"
        cursor.insertText(url_image)

    # Render from markdown to html
    def convert(self):
        raw_input = self.inputText.toPlainText()
        renderer = HighlightRenderer()
        markdown = mistune.Markdown(renderer=renderer)
        css_style = """<style type='text/css'>""" + css.css_string + """</style>"""
        mkd = markdown(raw_input)
        result = css_style + mkd
        self.outputText.setText(result)


    def parseFileName(self):
        filename = self.filename.split('/')
        self.fname = filename[-1]
        return self.fname


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TextEditor()
    ex.show()
    sys.exit(app.exec_())
