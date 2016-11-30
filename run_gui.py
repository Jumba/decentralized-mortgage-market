from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import os

from market.views import login


class ExampleApp(QMainWindow, login.Ui_Form): #QtWidgets.QMainWindow and login.Ui_Form are the superclasses
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.toolButton.clicked.connect(self.browse)
        #self.toolButton.clicked.connect(self.browse) kan ook
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

        tmp = ('Notepad: %s' % filename)
        self.setWindowTitle(tmp)
        self.lineEdit.setText(unistr)

    def login(self):
        print self.lineEdit.text()



def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    #form.toolButton.clicked.connect(form.browse())
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
