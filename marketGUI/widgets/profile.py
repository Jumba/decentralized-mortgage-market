# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/profile.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

import base64
import math
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle, QToolButton


class EllipseButton(QToolButton):
    """
    Represents an ellipsoid button in the GUI.
    """
    pass


class ProfileWidget(QWidget):
    def __init__(self, parent=None):
        super(ProfileWidget, self).__init__(parent)

    def setupUi(self, Form):
        Form.setObjectName("Form")

        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(20, 130, 141, 17))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(230, 130, 171, 17))
        self.label_6.setObjectName("label_6")
        self.documentsTable = QtWidgets.QTableWidget(Form)
        self.documentsTable.setEnabled(False)
        self.documentsTable.setGeometry(QtCore.QRect(20, 390, 541, 101))
        self.documentsTable.setObjectName("documentsTable")
        self.documentsTable.setColumnCount(0)
        self.documentsTable.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.documentsTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.documentsTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.documentsTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.documentsTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.documentsTable.setVerticalHeaderItem(4, item)
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(230, 250, 141, 17))
        self.label_8.setObjectName("label_8")
        self.lastNameField = QtWidgets.QLineEdit(Form)
        self.lastNameField.setGeometry(QtCore.QRect(230, 90, 191, 27))
        self.lastNameField.setObjectName("lastNameField")
        self.saveButton = QtWidgets.QPushButton(Form)
        self.saveButton.setGeometry(QtCore.QRect(430, 520, 121, 27))
        self.saveButton.setObjectName("saveButton")
        self.telNumberField = QtWidgets.QLineEdit(Form)
        self.telNumberField.setEnabled(True)
        self.telNumberField.setGeometry(QtCore.QRect(230, 270, 191, 27))
        self.telNumberField.setObjectName("telNumberField")
        self.lbl_iban = QtWidgets.QLabel(Form)
        self.lbl_iban.setGeometry(QtCore.QRect(20, 310, 57, 17))
        self.lbl_iban.setObjectName("lbl_iban")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(20, 190, 141, 17))
        self.label_7.setObjectName("label_7")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 57, 21))
        self.label_2.setObjectName("label_2")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(20, 250, 141, 17))
        self.label_9.setObjectName("label_9")
        self.lbl_document = QtWidgets.QLabel(Form)
        self.lbl_document.setGeometry(QtCore.QRect(20, 370, 181, 17))
        self.lbl_document.setObjectName("lbl_document")
        self.titleLabel = QtWidgets.QLabel(Form)
        self.titleLabel.setGeometry(QtCore.QRect(10, 10, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)
        self.titleLabel.setObjectName("titleLabel")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(230, 70, 211, 17))
        self.label_4.setObjectName("label_4")
        self.curPostalCodeField = QtWidgets.QLineEdit(Form)
        self.curPostalCodeField.setEnabled(False)
        self.curPostalCodeField.setGeometry(QtCore.QRect(20, 150, 191, 27))
        self.curPostalCodeField.setObjectName("curPostalCodeField")
        self.radioButtonBorrower = QtWidgets.QRadioButton(Form)
        self.radioButtonBorrower.setGeometry(QtCore.QRect(70, 40, 104, 22))
        self.radioButtonBorrower.setObjectName("radioButtonBorrower")
        self.curAddressField = QtWidgets.QLineEdit(Form)
        self.curAddressField.setEnabled(False)
        self.curAddressField.setGeometry(QtCore.QRect(20, 210, 401, 31))
        self.curAddressField.setObjectName("curAddressField")
        self.radioButtonInvestor = QtWidgets.QRadioButton(Form)
        self.radioButtonInvestor.setGeometry(QtCore.QRect(180, 40, 104, 22))
        self.radioButtonInvestor.setChecked(True)
        self.radioButtonInvestor.setObjectName("radioButtonInvestor")
        self.curHouseNumberField = QtWidgets.QLineEdit(Form)
        self.curHouseNumberField.setEnabled(False)
        self.curHouseNumberField.setGeometry(QtCore.QRect(230, 150, 191, 27))
        self.curHouseNumberField.setObjectName("curHouseNumberField")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 131, 17))
        self.label_3.setObjectName("label_3")
        self.emailAddressField = QtWidgets.QLineEdit(Form)
        self.emailAddressField.setGeometry(QtCore.QRect(20, 270, 191, 27))
        self.emailAddressField.setObjectName("emailAddressField")
        self.firstNameField = QtWidgets.QLineEdit(Form)
        self.firstNameField.setGeometry(QtCore.QRect(20, 90, 191, 27))
        self.firstNameField.setObjectName("firstNameField")
        self.IBANField = QtWidgets.QLineEdit(Form)
        self.IBANField.setGeometry(QtCore.QRect(20, 330, 401, 27))
        self.IBANField.setObjectName("IBANField")

        self.retranslateUi(Form)
        # QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label_5.setText(_translate("Form", "Current Post Code"))
        self.label_6.setText(_translate("Form", "Current House Number"))
        item = self.documentsTable.verticalHeaderItem(0)
        item.setText(_translate("Form", "Example Document 1"))
        item = self.documentsTable.verticalHeaderItem(1)
        item.setText(_translate("Form", "Example Document 2"))
        item = self.documentsTable.verticalHeaderItem(2)
        item.setText(_translate("Form", "Example Document 3"))
        item = self.documentsTable.verticalHeaderItem(3)
        item.setText(_translate("Form", "Example Document 4"))
        item = self.documentsTable.verticalHeaderItem(4)
        item.setText(_translate("Form", "Example Document 5"))
        self.label_8.setText(_translate("Form", "Telephone Number"))
        self.saveButton.setText(_translate("Form", "Save Changes"))
        self.lbl_iban.setText(_translate("Form", "IBAN"))
        self.label_7.setText(_translate("Form", "Current Address"))
        self.label_2.setText(_translate("Form", "I am a:"))
        self.label_9.setText(_translate("Form", "Email Address"))
        self.lbl_document.setText(_translate("Form", "Documents"))
        self.titleLabel.setText(_translate("Form", "Profile"))
        self.label_4.setText(_translate("Form", "Last Name"))
        self.radioButtonBorrower.setText(_translate("Form", "Borrower"))
        self.radioButtonInvestor.setText(_translate("Form", "Investor"))
        self.label_3.setText(_translate("Form", "First Name"))


class DownloadProgressBar(QWidget):
    """
    The DownloadProgressBar is visible in the download details pane and displays the completed pieces (or the progress
    of various actions such as file checking).
    """

    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.show_pieces = False
        self.pieces = []
        self.fraction = 0
        self.download = None

    def update_with_download(self, download):
        self.download = download
        if download["status"] in ("DLSTATUS_SEEDING", "DLSTATUS_STOPPED", "DLSTATUS_STOPPED_ON_ERROR",
                                  "DLSTATUS_CIRCUITS"):
            self.set_fraction(download["progress"])
        elif download["status"] in ("DLSTATUS_HASHCHECKING", "DLSTATUS_DOWNLOADING"):
            self.set_pieces()
        else:
            self.set_fraction(0.0)

    def set_fraction(self, fraction):
        self.show_pieces = False
        self.fraction = fraction
        self.repaint()

    def set_pieces(self):
        self.show_pieces = True
        self.fraction = 0.0
        self.pieces = self.decode_pieces(self.download["pieces"])[:self.download["total_pieces"]]
        self.repaint()

    def decode_pieces(self, pieces):
        byte_array = map(ord, base64.b64decode(pieces))
        byte_string = ''.join(bin(num)[2:].zfill(8) for num in byte_array)
        return [i == '1' for i in byte_string]

    def paintEvent(self, _):
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

        if self.show_pieces:
            piece_width = self.width() / float(len(self.pieces))
            for i in xrange(len(self.pieces)):
                if self.pieces[i]:
                    painter.fillRect(QRect(float(i) * piece_width, 0, math.ceil(piece_width), self.height()),
                                     QColor(230, 115, 0))
        else:
            painter.fillRect(QRect(0, 0, self.width() * self.fraction, self.height()), QColor(230, 115, 0))
