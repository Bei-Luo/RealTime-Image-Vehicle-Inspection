# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(740, 774)
        Form.setWindowTitle("")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 720, 576))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 670, 261, 31))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(40, 720, 271, 31))
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(300, 670, 421, 31))
        self.label_6.setObjectName("label_6")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(300, 720, 381, 31))
        self.label_9.setObjectName("label_9")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 721, 41))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("Form", "TextLabel"))
        self.label.setText(_translate("Form", "累计小型车："))
        self.label_3.setText(_translate("Form", "累计大型车："))
        self.label_6.setText(_translate("Form", "车辆密度（辆/每分钟）"))
        self.label_9.setText(_translate("Form", "车辆密度（辆/每分钟）"))
        self.label_4.setText(_translate("Form", "第二十小组作品 - 澳门友谊大桥实时车型检测与流量监测"))
