import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import main_view_controller
from market.views.main_view import Ui_MainWindow

USER = 1


class LoginController:
    def __init__(self, mainwindow):
        # assert(mainwindow, Ui_MainWindow)
        # self.mainwindow = Ui_MainWindow
        self.mainwindow = mainwindow
        self.app = mainwindow.app

        self.setup_signals()
        if os.path.exists('remembered'):
            f = open('remembered', 'r')
            self.mainwindow.login_private_key_lineedit.setText(f.readline())
            self.mainwindow.login_remember_me_checkbox.setChecked(True)

    def setup_signals(self):
        self.mainwindow.login_generate_pushbutton.clicked.connect(self.generate)
        self.mainwindow.login_browse_pushbutton.clicked.connect(self.browse)
        self.mainwindow.login_login_pushbutton.clicked.connect(self.login)

    def browse(self):
        filename, _ = QFileDialog.getOpenFileName(self.mainwindow, 'Open File', os.getenv('HOME'))
        fh = ''

        if QFile.exists(filename):
            fh = QFile(filename)

        if not fh.open(QFile.ReadOnly):
            qApp.quit()
        #
        # data = fh.readAll()
        # codec = QTextCodec.codecForUtfText(data)
        # private_key = codec.toUnicode(data)

        self.mainwindow.login_private_key_lineedit.setText(filename)

    def generate(self):
        user, public, private = self.app.api.create_user()

        if not os.path.isfile('market_public.key') and not os.path.isfile('market_private.key'):
            with open('market_public.key', 'w+') as f:
                f.write(public)

            with open('market_private.key', 'w+') as f:
                f.write(private)

            path = os.path.dirname(os.path.abspath(__file__))
            key_path = os.path.join(path, 'market_private.key')
            self.mainwindow.login_private_key_lineedit.setText(key_path)
        else:
            print "Keyfile found. Not overwriting."

    def login(self):
        if self.mainwindow.login_private_key_lineedit.text():
            key_file = open(self.mainwindow.login_private_key_lineedit.text(), 'r').read()
            # if remember me == true
            if not self.mainwindow.login_remember_me_checkbox.checkState():
                if os.path.exists('remembered'):
                    os.remove('remembered')
            # do the user check
            else:
                f = open('remembered', 'w+');
                f.write(self.mainwindow.login_private_key_lineedit.text())
                f.close()

            # Login
            user = self.app.api.login_user(key_file.encode('HEX'))
            if user:
                self.app.user = user
                print 'Login successful.'
                self.mainwindow.navigation.prepare_views_for_user()
            else:
                print 'Login failed.'
        else:
            print 'Key field is empty'

