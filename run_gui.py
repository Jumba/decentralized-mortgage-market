import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from market.views import login


class LoginController(QMainWindow, login.Ui_Form):
    def __init__(self, parent=None):
        super(LoginController, self).__init__(parent)
        self.setupUi(self)
        self.toolButton.clicked.connect(self.browse)
        self.pushButton.clicked.connect(self.login)

    def browse(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
        fh = ''

        if QFile.exists(filename):
            fh = QFile(filename)

        if not fh.open(QFile.ReadOnly):
            qApp.quit()

        data = fh.readAll()
        codec = QTextCodec.codecForUtfText(data)
        unistr = codec.toUnicode(data)

        self.lineEdit.setText(unistr)

    def login(self):
        #if remember me == true
        print self.lineEdit.text()


def main():
    app = QApplication(sys.argv)
    form = LoginController()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
