import sys
import re
from spellchecker import SpellCheck
from PyQt5.Qt import Qt
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QAction, QApplication, QMenu, QPlainTextEdit
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QTextCursor, QMouseEvent, QFont
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon


class SpellTextEdit(QPlainTextEdit, QMainWindow):

    def __init__(self, *args):
        QPlainTextEdit.__init__(self, *args)

        # Default dictionary based on the current locale.
        self.dict = SpellCheck()
        self.checker = ErrorHighlighter(self.document())
        self.checker.setChecker(self.dict)
        self.title = "English Spell Checker"
        self.left = 500
        self.top = 200
        self.width = 400
        self.height = 350
        self.icon_title = "spell.png"
        self.WindowSetUp()

    def WindowSetUp(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(self.icon_title))
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFont(QFont('Arial', 13))

    def mouseClickEvent(self, ev):
        if ev.button() == Qt.RightButton:
            # Rewrite the mouse event to a left button event so the cursor is
            # moved to the location of the pointer.
            ev = QMouseEvent(QEvent.MouseButtonPress, ev.pos(),
                                Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
        QPlainTextEdit.mouseClickEvent(self, ev)

    def contextMenuEvent(self, event):
        popup_menu = self.createStandardContextMenu()

        # Select the word under the cursor.
        cursor = self.textCursor()
        cursor.select(QTextCursor.WordUnderCursor)
        self.setTextCursor(cursor)

        # Check if the selected word is misspelled and offer spelling
        # suggestions if it is.
        if self.textCursor().hasSelection():
            text = str(self.textCursor().selectedText())
            if self.dict.check(text):
                suggestion_menu = QMenu('Spelling Suggestions')
                for word in self.dict.get_best_candidate(text):
                    action = SpellAction(word, suggestion_menu)
                    action.correct.connect(self.correctWord)
                    suggestion_menu.addAction(action)
                # Only add the spelling suggests to the menu if there are
                # suggestions.
                if len(suggestion_menu.actions()) != 0:
                    popup_menu.insertSeparator(popup_menu.actions()[0])
                    popup_menu.insertMenu(popup_menu.actions()[0], suggestion_menu)

        popup_menu.exec_(event.globalPos())

    def correctWord(self, word):
        '''
        Replaces the selected text with word.
        '''
        point_cursor = self.textCursor()
        point_cursor.beginEditBlock()

        point_cursor.removeSelectedText()
        point_cursor.insertText(word)

        point_cursor.endEditBlock()

class ErrorHighlighter(QSyntaxHighlighter):

    WORDS = u'(?iu)[\w\']+'

    def __init__(self, *args):
        QSyntaxHighlighter.__init__(self, *args)

        self.dict = None

    def setChecker(self, dict):
        self.dict = dict

    def highlightBlock(self, text: str):
        if not self.dict:
            return

        format_ = QTextCharFormat()
        format_.setUnderlineColor(Qt.red)
        format_.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        word_iter = re.finditer(self.WORDS, text)
        for word in word_iter:
            if self.dict.check(word.group()):
                self.setFormat(word.start(),
                    word.end() - word.start(), format_)


class SpellAction(QAction):

    '''
    A special QAction that returns the text in a signal.
    '''

    correct = pyqtSignal(str)

    def __init__(self, *args):
        QAction.__init__(self, *args)

        self.triggered.connect(lambda x: self.correct.emit(
            str(self.text())))


def main(args=sys.argv):
    app = QApplication(args)


    spellEdit = SpellTextEdit()
    spellEdit.show()

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())