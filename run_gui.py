import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from market.views import login


class LoginController(QMainWindow, login.Ui_Form):
    def __init__(self, parent=None):
        super(LoginController, self).__init__(parent)
        self.setupUi(self)
        self.browseButton.clicked.connect(self.browse)
        self.loginButton.clicked.connect(self.login)
        self.generateButton.clicked.connect(self.generate)
        if os.path.exists('remembered'):
            f = open('remembered', 'r')
            self.keyField.setText(f.readline())

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

        self.keyField.setText(unistr)

    def login(self):
        #if remember me == true
        if not self.rememberMeCheckBox.checkState():
            if os.path.exists('remembered'):
                os.remove('remembered')
        #do the user check
        else:
            f = open('remembered', 'w+');
            f.write(self.keyField.text())
            f.close()

    def generate(self):
        #generate new user
        return NotImplemented


def main():
    app = QApplication(sys.argv)
    form = LoginController()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
