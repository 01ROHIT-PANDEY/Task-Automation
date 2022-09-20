import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(900, 591)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(-1, -11, 900, 600))
        self.widget.setStyleSheet("background-image:qlineargradient(spread:pad, x1:0.068, y1:0.664773, x2:1, y2:0.466, stop:0.232955 rgba(0, 0, 0, 255), stop:0.636364 rgba(255, 255, 255, 255));\n"
"background-color: qlineargradient(spread:pad, x1:0.108, y1:0.579545, x2:1, y2:0, stop:0 rgba(64, 64, 64, 255), stop:1 rgba(255, 255, 255, 255));\n"
"background-color:rgb(93, 128, 255)")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(290, 50, 291, 51))
        self.label.setStyleSheet("color: rgb(255, 162, 47);")
        self.label.setObjectName("label")

        self.imagetext = QtWidgets.QPushButton(self.widget)
        self.imagetext.setGeometry(QtCore.QRect(330, 260, 201, 51))
        self.imagetext.setStyleSheet("background-color:\n"
        "rgb(228, 255, 255);\n"
        "border-radius:25px;\n"
        "")
        self.imagetext.setObjectName("imagetext")
        self.imagetext.clicked.connect(self.open_dashboard)
        
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt; font-weight:600; color:#ffffff;\">Task Automation</span></p></body></html>"))
    
        self.imagetext.setText(_translate("Dialog", "DASHBOARD"))
        
    def open_dashboard(self):
        import Main_Window

        
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
