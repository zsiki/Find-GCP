#!/usr/bin/env python3

""" GUI for gcp_find and other utilities
"""
import os
import sys
import cv2
import glob
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS
from aruco_type import ARUCO_TYPE
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap


class Ui_MainWindow():
    """ Class for main window
    """
    def setupUi(self, MainWindow, path_):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1040, 583)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setWindowIcon(QtGui.QIcon('fgcp_logo.png'))
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.path_ = path_
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1031, 561))
        self.tabWidget.setMaximumSize(QtCore.QSize(1100, 1100))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(30, 10, 500, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.GMcomboBox = QtWidgets.QComboBox(self.tab)
        self.GMcomboBox.setGeometry(QtCore.QRect(30, 70, 271, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        # font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.GMcomboBox.setFont(font)

        self.GMcomboBox.setObjectName("GMcomboBox")
        self.GMpushButton = QtWidgets.QPushButton(self.tab, clicked=lambda:self.generate())
        self.GMpushButton.setGeometry(QtCore.QRect(310, 70, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.GMpushButton.setFont(font)

        self.GMpushButton.setObjectName("GMpushButton")
        self.GMpushButton.setStyleSheet("color:white;\n"
                                    "background-color: rgb(0, 120, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;")

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.ED1radioButton = QtWidgets.QRadioButton(self.tab_2)
        self.ED1radioButton.setGeometry(QtCore.QRect(20, 430, 121, 31))
        self.ED1radioButton.setObjectName("ED1radioButton")
        self.EDradioButton_2 = QtWidgets.QRadioButton(self.tab_2)
        self.EDradioButton_2.setGeometry(QtCore.QRect(210, 430, 121, 31))
        self.EDradioButton_2.setObjectName("EDradioButton_2")
        self.EDpathButton_3 = QtWidgets.QPushButton(self.tab_2, clicked=lambda:self.path())
        self.EDpathButton_3.setGeometry(QtCore.QRect(370, 430, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.EDpathButton_3.setFont(font)
        self.EDpathButton_3.setObjectName("EDpathButton_3")
        self.EDpathButton_3.setStyleSheet("color:white;\n"
                                    "background-color: rgb(0, 120, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;")

        self.EDlabel_2 = QtWidgets.QLabel(self.tab_2)
        self.EDlabel_2.setGeometry(QtCore.QRect(10, 10, 581, 401))
        self.EDlabel_2.setTextFormat(QtCore.Qt.RichText)
        self.EDlabel_2.setPixmap(QtGui.QPixmap())
        self.EDlabel_2.setScaledContents(True)
        self.EDlabel_2.setWordWrap(False)
        self.EDlabel_2.setIndent(180)
        self.EDlabel_2.setObjectName("EDlabel_2")
        self.EDsubmitButton_2 = QtWidgets.QPushButton(self.tab_2, clicked=lambda:self.exif())
        self.EDsubmitButton_2.setGeometry(QtCore.QRect(0, 470, 581, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.EDsubmitButton_2.setFont(font)
        self.EDsubmitButton_2.setObjectName("EDsubmitButton_2")
        self.EDsubmitButton_2.setStyleSheet("color:white;\n"
                                    "background-color: rgb(0, 70, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;")

        self.listWidget = QtWidgets.QListWidget(self.tab_2)
        self.listWidget.setGeometry(QtCore.QRect(600, 30, 421, 481))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setStyleSheet("color:white;\n"
                                    "background-color:rgb(99,102,106);\n"
                                    "font:bold 12px;")
        self.EDlabel_3 = QtWidgets.QLabel(self.tab_2)
        self.EDlabel_3.setGeometry(QtCore.QRect(600, 10, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.EDlabel_3.setFont(font)
        self.EDlabel_3.setObjectName("EDlabel_3")
        self.EDClrBtn = QtWidgets.QPushButton(self.tab_2, clicked=lambda:self.clear())
        self.EDClrBtn.setGeometry(QtCore.QRect(920, 0, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.EDClrBtn.setFont(font)
        self.EDClrBtn.setAutoFillBackground(False)
        self.EDClrBtn.setStyleSheet("color:white;\n"
                                    "background-color: rgb(255, 0, 0);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;")
        self.EDClrBtn.setObjectName("EDClrBtn")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1040, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.GMcomboBox.addItem('Select Type')
        self.GMcomboBox.addItems(ARUCO_TYPE)
        self.ED1radioButton.setChecked(True)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Find-GCP"))
        self.label.setText(_translate("MainWindow", "Select Marker Type"))
        self.GMpushButton.setText(_translate("MainWindow", "Generate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                  _translate("MainWindow", "Generate Marker"))
        self.ED1radioButton.setText(_translate("MainWindow", "Select Image"))
        self.EDradioButton_2.setText(_translate("MainWindow", "Select Directory"))
        self.EDpathButton_3.setText(_translate("MainWindow", "Path"))
        self.EDlabel_2.setText(_translate("MainWindow", "Image Preview Will Appear Here"))
        self.EDsubmitButton_2.setText(_translate("MainWindow", "Submit"))
        self.EDlabel_3.setText(_translate("MainWindow", "Results"))
        self.EDClrBtn.setText(_translate("MainWindow", "Clear Results"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  _translate("MainWindow", "Exif Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3),
                                  _translate("MainWindow", "Find GCP"))

    def generate(self):
        if self.GMcomboBox.currentText() == 'Select Type':
            self.label.setText('Select a valid type')

        if os.path.exists(f'{self.GMcomboBox.currentText()}'):
            if not os.path.isdir(f'{self.GMcomboBox.currentText()}'):
                self.label.setText(f'{self.GMcomboBox.currentText()} is not a folder')
                exit(1)
        else:
            try:
                if f'{self.GMcomboBox.currentText()}' != 'Select Type':
                    os.mkdir(self.GMcomboBox.currentText())
            except:
                print('[INFO] Cannot Create')
                exit(2)

        if f"{self.GMcomboBox.currentText()}" != 'Select Type':
            if f"{self.GMcomboBox.currentText()}" == 'DICT_3X3':
                arucoDict = ARUCO_TYPE.get(self.GMcomboBox.currentText())
                for i in range(32):
                    tag = np.zeros((300, 300, 1), dtype="uint8")
                    marker = cv2.aruco.drawMarker(arucoDict, i, 300, tag, 1)
                    cv2.imwrite('{}/{}_{}.png'.format(self.GMcomboBox.currentText(),self.GMcomboBox.currentText(),i), marker)
                self.label.setText(f'Successfully Generated {self.GMcomboBox.currentText()}')
            else:
                arucoDict = cv2.aruco.Dictionary_get(ARUCO_TYPE.get(self.GMcomboBox.currentText()))
                for i in range(32):
                    tag = np.zeros((300, 300, 1), dtype="uint8")
                    marker = cv2.aruco.drawMarker(arucoDict, i, 300, tag, 1)
                    cv2.imwrite('{}/{}_{}.png'.format(self.GMcomboBox.currentText(),
                    self.GMcomboBox.currentText(), i), marker)
                self.label.setText(f'Successfully Generated {self.GMcomboBox.currentText()}')

    def path(self):
        if self.ED1radioButton.isChecked():
            self.path_, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open Image",os.getcwd(),
            "JPG Files (*.jpg *.JPG);; PNG Files (*.png *.PNG);; JPG & PNG Files (*.jpg *.JPG *.png *.PNG);;")
            self.pixmap = QPixmap(self.path_)
            self.EDlabel_2.setPixmap(self.pixmap)
        elif self.EDradioButton_2.isChecked():
            self.path_ = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory", os.getcwd())
            self.path_ = self.path_ +'/*.[jJ][pP][gG]'
        self.clear()

    def exif(self):
        if self.path_ == '':
            self.EDlabel_2.setText('No Image or Directory')
        else:
            pass
        def to_degrees(direction, value):
            """
            convert the GPS coordinates stored in the EXIF to degress in float format
            :param value: tuples of DMS
            :param dir: direction E/N/W/S
            :returns: decimal degree
            """
            try:
                angle_deg = float(value[0][0]) / float(value[0][1])
                angle_min = float(value[1][0]) / float(value[1][1])
                angle_sec = float(value[2][0]) / float(value[2][1])
            except:
                angle_deg, angle_min, angle_sec = value
            angle_dir = 1 if direction in ('E', 'N') else -1
            return angle_dir * (angle_deg + (angle_min / 60.0) + (angle_sec / 3600.0))

        def to_num(value):
            """
            convert elevation stored in the EXIF to metric data
            :param value: tuple (int, int)
            :returns: float value
            """
            try:
                ret = value[0] / value[1]
            except:
                ret = float(value)
            return ret
        for i in glob.iglob(self.path_):
            img_name = os.path.basename(i)
            try:
                img = Image.open(i)
                exif = img._getexif()
            except AttributeError:
                exif = None
            ret = []
            if exif is not None:
                exif_data = {TAGS[k]: v for k, v in exif.items() if k in TAGS}
                # print(exif_data)
                if 'GPSInfo' in exif_data and len(exif_data['GPSInfo']) > 6:
                    ret = [to_degrees(exif_data['GPSInfo'][3], exif_data['GPSInfo'][4]),
                        to_degrees(exif_data['GPSInfo'][1], exif_data['GPSInfo'][2]),
                        to_num(exif_data['GPSInfo'][6])]
                if 'DateTime' in exif_data:
                    ret.append(exif_data['DateTime'])

            if len(ret) > 3:
                item = "{},{:.6f},{:.6f},{:.2f},{}".format(img_name, ret[0], ret[1], ret[2], ret[3])
                self.listWidget.addItem(item)
            elif len(ret) == 3:
                item = "{},{:.6f},{:.6f},{:.2f}".format(img_name, ret[0], ret[1], ret[2])
                self.listWidget.addItem(item)
            elif len(ret) == 1:
                item = "{},,,,{}".format(img_name, ret[0])
                self.listWidget.addItem(item)
            else:
                item = "{},,,,,No EXIF".format(img_name)
                self.listWidget.addItem(item)

    def clear(self):
        self.listWidget.clear()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, path_='')
    MainWindow.show()
    sys.exit(app.exec_())
