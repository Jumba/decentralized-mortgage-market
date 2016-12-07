import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.views import login
from marketGUI.market_app import MarketApplication


class LoginController(QMainWindow, login.Ui_Form):
    def __init__(self, parent=None, app=None):
        super(LoginController, self).__init__(parent)
        self.app = app
        self.setupUi(self)
        self.browseButton.clicked.connect(self.browse)

#        self.loginButton.clicked.connect(self.login)
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
        private_key = codec.toUnicode(data)

        self.keyField.setText(filename)

    def login(self):
        key_file = open(self.keyField.text(), 'r').read()
        # if remember me == true
        if not self.rememberMeCheckBox.checkState():
            if os.path.exists('remembered'):
                os.remove('remembered')
        # do the user check
        else:
            f = open('remembered', 'w+');
            f.write(self.keyField.text())
            f.close()

        # Login
        user = self.app.api.login_user(key_file)
        if user:
            self.app.user = user
        else:
            print "Login failed"


    def generate(self):
        user, public, private = self.app.api.create_user()

        if not os.path.isfile('market_public.key') and not os.path.isfile('market_private.key'):
            with open('market_public.key', 'w+') as f:
                f.write(public)

            with open('market_private.key', 'w+') as f:
                f.write(private)

            path = os.path.dirname(os.path.abspath(__file__))
            key_path = os.path.join(path, 'market_private.key')
            self.keyField.setText(key_path)
        else:
            print "Keyfile found. Not overwriting."



def main():
    app = MarketApplication(sys.argv)

    form = LoginController(app=app)
    form.show()

    app.exec_()


if __name__ == '__main__':
    main()
