# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error.ui'
#
# Created: Mon Jun 16 09:59:43 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form2(object):
    def setupUi(self, Form2):
        Form2.setObjectName(_fromUtf8("Form2"))
        Form2.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Form2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listWidget = QtGui.QListWidget(Form2)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(288, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(Form2)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)

        self.retranslateUi(Form2)
        QtCore.QMetaObject.connectSlotsByName(Form2)

    def retranslateUi(self, Form2):
        Form2.setWindowTitle(_translate("Form2", "MYRaf Error", None))
        self.pushButton.setText(_translate("Form2", "Save Log", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form2 = QtGui.QDialog()
    ui = Ui_Form2()
    ui.setupUi(Form2)
    Form2.show()
    sys.exit(app.exec_())

