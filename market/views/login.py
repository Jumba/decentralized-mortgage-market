# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/tmp/loginxD1774.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(650, 273)
        self.titleLabel = QtWidgets.QLabel(Form)
        self.titleLabel.setGeometry(QtCore.QRect(0, 0, 651, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.titleLabel.setFont(font)
        self.titleLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.keyFieldLabel = QtWidgets.QLabel(Form)
        self.keyFieldLabel.setGeometry(QtCore.QRect(30, 50, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.keyFieldLabel.setFont(font)
        self.keyFieldLabel.setObjectName("keyFieldLabel")
        self.keyField = QtWidgets.QLineEdit(Form)
        self.keyField.setGeometry(QtCore.QRect(30, 70, 481, 23))
        self.keyField.setObjectName("keyField")
        self.browseButton = QtWidgets.QToolButton(Form)
        self.browseButton.setGeometry(QtCore.QRect(530, 70, 71, 22))
        self.browseButton.setObjectName("browseButton")
        self.loginButton = QtWidgets.QPushButton(Form)
        self.loginButton.setGeometry(QtCore.QRect(430, 100, 80, 23))
        self.loginButton.setObjectName("loginButton")
        self.rememberMeCheckBox = QtWidgets.QCheckBox(Form)
        self.rememberMeCheckBox.setGeometry(QtCore.QRect(304, 100, 111, 21))
        self.rememberMeCheckBox.setAutoFillBackground(False)
        self.rememberMeCheckBox.setChecked(True)
        self.rememberMeCheckBox.setObjectName("rememberMeCheckBox")
        self.generateLabel = QtWidgets.QLabel(Form)
        self.generateLabel.setGeometry(QtCore.QRect(30, 140, 651, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.generateLabel.setFont(font)
        self.generateLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.generateLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.generateLabel.setObjectName("generateLabel")
        self.generateButton = QtWidgets.QPushButton(Form)
        self.generateButton.setGeometry(QtCore.QRect(30, 180, 80, 23))
        self.generateButton.setObjectName("generateButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.titleLabel.setText(_translate("Form", "Login"))
        self.keyFieldLabel.setText(_translate("Form", "Private key"))
        self.browseButton.setToolTip(_translate("Form", "<html><head/><body><p><br/></p></body></html>"))
        self.browseButton.setText(_translate("Form", "Browse"))
        self.loginButton.setText(_translate("Form", "Login"))
        self.rememberMeCheckBox.setText(_translate("Form", "Remember Me"))
        self.generateLabel.setText(_translate("Form", "Don\'t have a private key?"))
        self.generateButton.setText(_translate("Form", "Generate "))

