#!/usr/bin/env python3

""" GUI for gcp_find and other utilities
"""
import os
import sys
import re
import cv2
import glob
import numpy as np
from PIL import Image
from time import sleep
from PIL.ExifTags import TAGS
from aruco_type import ARUCO_TYPE
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, QObject, QThread
from PyQt5.QtGui import QPixmap
from process_raw import DngFile

class ParameterWin(QtWidgets.QWidget, QtWidgets.QApplication):
    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle('Parameters')
        self.resize(705,407)
        self.setWindowIcon(QtGui.QIcon('fgcp_logo.png'))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.validator = QRegExpValidator(QRegExp(r'[+-]?[0-9]+\.[0-9]+'))
        self.params = cv2.aruco.DetectorParameters_create()
        self.ipath = ''
        self.combomt = QtWidgets.QComboBox(self.centralwidget)
        self.combomt.setGeometry(QtCore.QRect(10, 30, 171, 22))
        self.combomt.setObjectName("combomt")
        self.pmarkertype = QtWidgets.QLabel(self.centralwidget)
        self.pmarkertype.setGeometry(QtCore.QRect(10, 10, 171, 16))
        self.pmarkertype.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pmarkertype.setTextFormat(QtCore.Qt.AutoText)
        self.pmarkertype.setObjectName("pmarkertype")
        self.boxminrate = QtWidgets.QLineEdit(self.centralwidget)
        self.boxminrate.setGeometry(QtCore.QRect(200, 30, 113, 20))
        self.boxminrate.setObjectName("boxminrate")
        self.boxminrate.setValidator(self.validator)
        self.pmin = QtWidgets.QLabel(self.centralwidget)
        self.pmin.setGeometry(QtCore.QRect(200, 10, 111, 16))
        self.pmin.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pmin.setTextFormat(QtCore.Qt.AutoText)
        self.pmin.setObjectName("pmin")
        self.boxignore = QtWidgets.QLineEdit(self.centralwidget)
        self.boxignore.setGeometry(QtCore.QRect(330, 30, 113, 20))
        self.boxignore.setObjectName("boxignore")
        self.boxignore.setValidator(self.validator)
        self.pignore = QtWidgets.QLabel(self.centralwidget)
        self.pignore.setGeometry(QtCore.QRect(330, 10, 111, 16))
        self.pignore.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pignore.setTextFormat(QtCore.Qt.AutoText)
        self.pignore.setObjectName("pignore")
        self.combosoft = QtWidgets.QComboBox(self.centralwidget)
        self.combosoft.setGeometry(QtCore.QRect(10, 90, 171, 22))
        self.combosoft.setObjectName("combosoft")
        self.psoft = QtWidgets.QLabel(self.centralwidget)
        self.psoft.setGeometry(QtCore.QRect(10, 70, 171, 16))
        self.psoft.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.psoft.setTextFormat(QtCore.Qt.AutoText)
        self.psoft.setObjectName("psoft")
        self.boxlimit = QtWidgets.QLineEdit(self.centralwidget)
        self.boxlimit.setGeometry(QtCore.QRect(570, 30, 113, 20))
        self.boxlimit.setObjectName("boxlimit")
        self.boxlimit.setValidator(self.validator)
        self.boxlimit.setText(f'{99}')
        self.pespg = QtWidgets.QLabel(self.centralwidget)
        self.pespg.setGeometry(QtCore.QRect(450, 10, 111, 16))
        self.pespg.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pespg.setTextFormat(QtCore.Qt.AutoText)
        self.pespg.setObjectName("pespg")
        self.boxseperator = QtWidgets.QLineEdit(self.centralwidget)
        self.boxseperator.setGeometry(QtCore.QRect(200, 90, 113, 20))
        self.boxseperator.setObjectName("boxseperator")
        self.boxwinmax = QtWidgets.QLineEdit(self.centralwidget)
        self.boxwinmax.setGeometry(QtCore.QRect(450, 90, 113, 20))
        self.boxwinmax.setObjectName("boxwinmax")
        self.boxwinmax.setValidator(self.validator)
        self.boxwinstep = QtWidgets.QLineEdit(self.centralwidget)
        self.boxwinstep.setGeometry(QtCore.QRect(570, 90, 113, 20))
        self.boxwinstep.setObjectName("boxwinstep")
        self.boxwinstep.setValidator(self.validator)
        self.plimit = QtWidgets.QLabel(self.centralwidget)
        self.plimit.setGeometry(QtCore.QRect(570, 10, 111, 16))
        self.plimit.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.plimit.setTextFormat(QtCore.Qt.AutoText)
        self.plimit.setObjectName("plimit")
        self.pseperator = QtWidgets.QLabel(self.centralwidget)
        self.pseperator.setGeometry(QtCore.QRect(200, 70, 111, 16))
        self.pseperator.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pseperator.setTextFormat(QtCore.Qt.AutoText)
        self.pseperator.setObjectName("pseperator")
        self.pwinmin = QtWidgets.QLabel(self.centralwidget)
        self.pwinmin.setGeometry(QtCore.QRect(330, 70, 111, 16))
        self.pwinmin.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pwinmin.setTextFormat(QtCore.Qt.AutoText)
        self.pwinmin.setObjectName("pwinmin")
        self.boxmaxrate = QtWidgets.QLineEdit(self.centralwidget)
        self.boxmaxrate.setGeometry(QtCore.QRect(330, 150, 113, 20))
        self.boxmaxrate.setObjectName("boxmaxrate")
        self.boxmaxrate.setValidator(self.validator)
        self.boxpoly = QtWidgets.QLineEdit(self.centralwidget)
        self.boxpoly.setGeometry(QtCore.QRect(450, 150, 113, 20))
        self.boxpoly.setObjectName("boxpoly")
        self.boxpoly.setValidator(self.validator)
        self.boxespg = QtWidgets.QLineEdit(self.centralwidget)
        self.boxespg.setGeometry(QtCore.QRect(450, 30, 113, 20))
        self.boxespg.setObjectName("boxespg")
        self.boxespg.setValidator(self.validator)
        self.boxwinmin = QtWidgets.QLineEdit(self.centralwidget)
        self.boxwinmin.setGeometry(QtCore.QRect(330, 90, 113, 20))
        self.boxwinmin.setObjectName("boxwinmin")
        self.boxwinmin.setValidator(self.validator)
        self.boxthres = QtWidgets.QLineEdit(self.centralwidget)
        self.boxthres.setGeometry(QtCore.QRect(200, 150, 113, 20))
        self.boxthres.setObjectName("boxthres")
        self.boxthres.setValidator(self.validator)
        self.boxcorner = QtWidgets.QLineEdit(self.centralwidget)
        self.boxcorner.setGeometry(QtCore.QRect(570, 150, 113, 20))
        self.boxcorner.setObjectName("boxcorner")
        self.boxcorner.setValidator(self.validator)
        self.boxmarkerdist = QtWidgets.QLineEdit(self.centralwidget)
        self.boxmarkerdist.setGeometry(QtCore.QRect(200, 210, 113, 20))
        self.boxmarkerdist.setObjectName("boxmarkerdist")
        self.boxmarkerdist.setValidator(self.validator)
        self.boxborderdist = QtWidgets.QLineEdit(self.centralwidget)
        self.boxborderdist.setGeometry(QtCore.QRect(330, 210, 113, 20))
        self.boxborderdist.setObjectName("boxborderdist")
        self.boxborderdist.setValidator(self.validator)
        self.boxborderbits = QtWidgets.QLineEdit(self.centralwidget)
        self.boxborderbits.setGeometry(QtCore.QRect(450, 210, 113, 20))
        self.boxborderbits.setObjectName("boxborderbits")
        self.boxborderbits.setValidator(self.validator)
        self.boxotsu = QtWidgets.QLineEdit(self.centralwidget)
        self.boxotsu.setGeometry(QtCore.QRect(570, 210, 113, 20))
        self.boxotsu.setObjectName("boxotsu")
        self.boxotsu.setValidator(self.validator)
        self.boxpersp = QtWidgets.QLineEdit(self.centralwidget)
        self.boxpersp.setGeometry(QtCore.QRect(200, 270, 113, 20))
        self.boxpersp.setObjectName("boxpersp")
        self.boxpersp.setValidator(self.validator)
        self.boxerror = QtWidgets.QLineEdit(self.centralwidget)
        self.boxerror.setGeometry(QtCore.QRect(330, 270, 113, 20))
        self.boxerror.setObjectName("boxerror")
        self.boxerror.setValidator(self.validator)
        self.pwinmax = QtWidgets.QLabel(self.centralwidget)
        self.pwinmax.setGeometry(QtCore.QRect(450, 70, 111, 16))
        self.pwinmax.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pwinmax.setTextFormat(QtCore.Qt.AutoText)
        self.pwinmax.setObjectName("pwinmax")
        self.pwinstep = QtWidgets.QLabel(self.centralwidget)
        self.pwinstep.setGeometry(QtCore.QRect(570, 70, 111, 16))
        self.pwinstep.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pwinstep.setTextFormat(QtCore.Qt.AutoText)
        self.pwinstep.setObjectName("pwinstep")
        self.pthres = QtWidgets.QLabel(self.centralwidget)
        self.pthres.setGeometry(QtCore.QRect(200, 130, 111, 16))
        self.pthres.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pthres.setTextFormat(QtCore.Qt.AutoText)
        self.pthres.setObjectName("pthres")
        self.pmaxrate = QtWidgets.QLabel(self.centralwidget)
        self.pmaxrate.setGeometry(QtCore.QRect(330, 130, 111, 16))
        self.pmaxrate.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pmaxrate.setTextFormat(QtCore.Qt.AutoText)
        self.pmaxrate.setObjectName("pmaxrate")
        self.ppoly = QtWidgets.QLabel(self.centralwidget)
        self.ppoly.setGeometry(QtCore.QRect(450, 130, 111, 16))
        self.ppoly.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.ppoly.setTextFormat(QtCore.Qt.AutoText)
        self.ppoly.setObjectName("ppoly")
        self.pcorner = QtWidgets.QLabel(self.centralwidget)
        self.pcorner.setGeometry(QtCore.QRect(570, 130, 111, 16))
        self.pcorner.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pcorner.setTextFormat(QtCore.Qt.AutoText)
        self.pcorner.setObjectName("pcorner")
        self.pmakerdist = QtWidgets.QLabel(self.centralwidget)
        self.pmakerdist.setGeometry(QtCore.QRect(200, 190, 111, 16))
        self.pmakerdist.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pmakerdist.setTextFormat(QtCore.Qt.AutoText)
        self.pmakerdist.setObjectName("pmakerdist")
        self.pborderdist = QtWidgets.QLabel(self.centralwidget)
        self.pborderdist.setGeometry(QtCore.QRect(330, 190, 111, 16))
        self.pborderdist.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pborderdist.setTextFormat(QtCore.Qt.AutoText)
        self.pborderdist.setObjectName("pborderdist")
        self.pborderbits = QtWidgets.QLabel(self.centralwidget)
        self.pborderbits.setGeometry(QtCore.QRect(450, 190, 111, 16))
        self.pborderbits.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pborderbits.setTextFormat(QtCore.Qt.AutoText)
        self.pborderbits.setObjectName("pborderbits")
        self.potsu = QtWidgets.QLabel(self.centralwidget)
        self.potsu.setGeometry(QtCore.QRect(570, 190, 111, 16))
        self.potsu.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.potsu.setTextFormat(QtCore.Qt.AutoText)
        self.potsu.setObjectName("potsu")
        self.ppersp = QtWidgets.QLabel(self.centralwidget)
        self.ppersp.setGeometry(QtCore.QRect(200, 250, 111, 16))
        self.ppersp.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.ppersp.setTextFormat(QtCore.Qt.AutoText)
        self.ppersp.setObjectName("ppersp")
        self.perror = QtWidgets.QLabel(self.centralwidget)
        self.perror.setGeometry(QtCore.QRect(330, 250, 111, 16))
        self.perror.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.perror.setTextFormat(QtCore.Qt.AutoText)
        self.perror.setObjectName("perror")
        self.pcorrect = QtWidgets.QLabel(self.centralwidget)
        self.pcorrect.setGeometry(QtCore.QRect(450, 250, 111, 16))
        self.pcorrect.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pcorrect.setTextFormat(QtCore.Qt.AutoText)
        self.pcorrect.setObjectName("pcorrect")
        self.boxcorrect = QtWidgets.QLineEdit(self.centralwidget)
        self.boxcorrect.setGeometry(QtCore.QRect(450, 270, 113, 20))
        self.boxcorrect.setObjectName("boxcorrect")
        self.boxcorrect.setValidator(self.validator)
        self.boxrefinement = QtWidgets.QLineEdit(self.centralwidget)
        self.boxrefinement.setGeometry(QtCore.QRect(570, 270, 113, 20))
        self.boxrefinement.setObjectName("boxrefinement")
        self.boxrefinement.setValidator(self.validator)
        self.boxrefwin = QtWidgets.QLineEdit(self.centralwidget)
        self.boxrefwin.setGeometry(QtCore.QRect(200, 330, 113, 20))
        self.boxrefwin.setObjectName("boxrefwin")
        self.boxrefwin.setValidator(self.validator)
        self.boxmaxiter = QtWidgets.QLineEdit(self.centralwidget)
        self.boxmaxiter.setGeometry(QtCore.QRect(330, 330, 113, 20))
        self.boxmaxiter.setObjectName("boxmaxiter")
        self.boxmaxiter.setValidator(self.validator)
        self.boxminacc = QtWidgets.QLineEdit(self.centralwidget)
        self.boxminacc.setGeometry(QtCore.QRect(450, 330, 113, 20))
        self.boxminacc.setObjectName("boxminacc")
        self.boxminacc.setValidator(self.validator)
        self.prefinement = QtWidgets.QLabel(self.centralwidget)
        self.prefinement.setGeometry(QtCore.QRect(570, 250, 111, 16))
        self.prefinement.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.prefinement.setTextFormat(QtCore.Qt.AutoText)
        self.prefinement.setObjectName("prefinement")
        self.prefwin = QtWidgets.QLabel(self.centralwidget)
        self.prefwin.setGeometry(QtCore.QRect(200, 310, 111, 16))
        self.prefwin.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.prefwin.setTextFormat(QtCore.Qt.AutoText)
        self.prefwin.setObjectName("prefwin")
        self.pmaxiter = QtWidgets.QLabel(self.centralwidget)
        self.pmaxiter.setGeometry(QtCore.QRect(330, 310, 111, 16))
        self.pmaxiter.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pmaxiter.setTextFormat(QtCore.Qt.AutoText)
        self.pmaxiter.setObjectName("pmaxiter")
        self.pminacc = QtWidgets.QLabel(self.centralwidget)
        self.pminacc.setGeometry(QtCore.QRect(450, 310, 111, 16))
        self.pminacc.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pminacc.setTextFormat(QtCore.Qt.AutoText)
        self.pminacc.setObjectName("pminacc")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(70)
        self.pinputfile = QtWidgets.QLabel(self.centralwidget)
        self.pinputfile.setGeometry(QtCore.QRect(10, 190, 171, 16))
        self.pinputfile.setFont(font)
        self.pinputfile.setTextFormat(QtCore.Qt.AutoText)
        self.pinputfile.setObjectName("pinputfile")
        self.inputfile = QtWidgets.QRadioButton(self.centralwidget)
        self.inputfile.setGeometry(QtCore.QRect(10, 210, 121, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.inputfile.setFont(font)
        self.inputfile.setObjectName("inputfile")
        self.poutput = QtWidgets.QLabel(self.centralwidget)
        self.poutput.setGeometry(QtCore.QRect(10, 250, 111, 16))
        self.poutput.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.poutput.setTextFormat(QtCore.Qt.AutoText)
        self.poutput.setObjectName("poutput")
        self.outputfile = QtWidgets.QLineEdit(self.centralwidget)
        self.outputfile.setGeometry(QtCore.QRect(10, 270, 161, 20))
        self.outputfile.setStyleSheet("")
        self.outputfile.setText("")
        self.outputfile.setObjectName("outputfile")
        self.fixparameter = QtWidgets.QPushButton(self.centralwidget, clicked=lambda:self.fixparams())
        self.fixparameter.setGeometry(QtCore.QRect(10, 330, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fixparameter.setFont(font)
        self.fixparameter.setObjectName("fixparameter")
        self.fixparameter.setStyleSheet("QPushButton{color:white;\n"
                                    "background-color: rgb(0, 120, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;}\n"
                                    "QPushButton:hover{border:2px solid;\n"
                                    "background-color: rgb(0, 120, 200);}\n")

        self.pinverted = QtWidgets.QLabel(self.centralwidget)
        self.pinverted.setGeometry(QtCore.QRect(570, 310, 111, 16))
        self.pinverted.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";")
        self.pinverted.setTextFormat(QtCore.Qt.AutoText)
        self.pinverted.setObjectName("pinverted")
        self.comboInverted = QtWidgets.QComboBox(self.centralwidget)
        self.comboInverted.setGeometry(QtCore.QRect(570, 330, 111, 22))
        self.comboInverted.setObjectName("comboInverted")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.combomt.addItems(ARUCO_TYPE)
        self.combosoft.addItems(['Select','ODM','VisualSfM'])
        self.comboInverted.addItems(['False', 'True'])
        self.inputfile.toggled.connect(lambda:self.inputFileName(self.inputfile))

    def retranslateUi(self, parameter):
        _translate = QtCore.QCoreApplication.translate
        parameter.setWindowTitle(_translate("Parameter", "Parameters"))
        self.pmarkertype.setText(_translate("Parameter", "Select Marker Type"))
        self.pmin.setText(_translate("Parameter", "MinRate"))
        self.pignore.setText(_translate("Parameter", "Ignore"))
        self.psoft.setText(_translate("Parameter", "Software"))
        self.pespg.setText(_translate("Parameter", "EPSG"))
        self.plimit.setText(_translate("parameter", "Limit"))
        self.pseperator.setText(_translate("parameter", "Seperator"))
        self.pwinmin.setText(_translate("parameter", "WinMin"))
        self.pwinmax.setText(_translate("parameter", "WinMax"))
        self.pwinstep.setText(_translate("parameter", "WinStep"))
        self.pthres.setText(_translate("parameter", "Thres"))
        self.pmaxrate.setText(_translate("parameter", "MaxRate"))
        self.ppoly.setText(_translate("parameter", "Poly"))
        self.pcorner.setText(_translate("parameter", "Corner"))
        self.pmakerdist.setText(_translate("parameter", "MarkerDist"))
        self.pborderdist.setText(_translate("parameter", "BorderDist"))
        self.pborderbits.setText(_translate("parameter", "BorderBits"))
        self.potsu.setText(_translate("parameter", "Otsu"))
        self.ppersp.setText(_translate("parameter", "Persp"))
        self.perror.setText(_translate("parameter", "Error"))
        self.pcorrect.setText(_translate("parameter", "Correct"))
        self.prefinement.setText(_translate("parameter", "Refinement"))
        self.prefwin.setText(_translate("parameter", "RefWin"))
        self.pmaxiter.setText(_translate("parameter", "Maxiter"))
        self.pminacc.setText(_translate("parameter", "Minacc"))
        self.pinputfile.setText(_translate("parameter", "Input File"))
        self.inputfile.setText(_translate("parameter", "Select Input File"))
        self.poutput.setText(_translate("parameter", "Output File Name"))
        self.fixparameter.setText(_translate("parameter", "Fix Parameters"))
        self.pinverted.setText(_translate("parameter", "Inverted"))


    def display(self):
        self.show()

    def inputFileName(self, i):
        if i.isChecked():
            self.ipath, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Select Input File",os.getcwd(),
            "Text documents (*.txt);;")
            self.pinputfile.setText(self.ipath.split('/')[-1])

    def fixparams(self):
        if self.boxminrate.text() !='':
            self.minrate = float(self.boxminrate.text())
            self.params.minMarkerPerimeterRate = self.minrate
        else:
            self.params.minMarkerPerimeterRate = 0.3

        if self.boxmaxrate.text() !='':
            self.maxrate = float(self.boxmaxrate.text())
            self.params.maxMarkerPerimeterRate = self.maxrate
        else:
            self.params.maxMarkerPerimeterRate = self.params.maxMarkerPerimeterRate

        if self.boxignore.text() !='':
            self.ignore = float(self.boxignore.text())
            self.params.perspectiveRemoveIgnoredMarginPerCell = self.ignore
        else:
            self.params.perspectiveRemoveIgnoredMarginPerCell = self.params.perspectiveRemoveIgnoredMarginPerCell

        if self.boxespg.text() !='':
            self.epsg = int(self.boxespg.text())
        else:
            pass

        if self.boxlimit.text() !='':
            self.limit = int(self.boxlimit.text())
        else:
            self.boxlimit.setText(f'{99}')

        if self.boxseperator.text() !='':
            self.seperator = self.boxseperator.text()
            self.boxseperator.setText(self.seperator)
        else:
            self.boxseperator.setText(" ")

        if self.boxwinmin.text() !='':
            self.winmin = int(self.boxwinmin.text())
            self.params.adaptiveThreshWinSizeMin = self.winmin
        else:
            self.params.adaptiveThreshWinSizeMin = self.params.adaptiveThreshWinSizeMin

        if self.boxwinmax.text() !='':
            self.winmax = int(self.boxwinmax.text())
            self.params.adaptiveThreshWinSizeMax = self.winmax
        else:
            self.params.adaptiveThreshWinSizeMax = self.params.adaptiveThreshWinSizeMax

        if self.boxwinstep.text() !='':
            self.winstep = int(self.boxwinstep.text())
            self.params.adaptiveThreshWinSizeStep = self.winstep
        else:
            self.params.adaptiveThreshWinSizeStep = self.params.adaptiveThreshWinSizeStep

        if self.boxthres.text() !='':
            self.thres = float(self.boxthres.text())
            self.params.adaptiveThreshConstant = self.thres
        else:
            self.params.adaptiveThreshConstant = self.params.adaptiveThreshConstant

        if self.boxpoly.text() !='':
            self.poly = float(self.boxpoly.text())
            self.params.polygonalApproxAccuracyRate = self.poly
        else:
            self.params.polygonalApproxAccuracyRate = self.params.polygonalApproxAccuracyRate

        if self.boxcorner.text() !='':
            self.corner = float(self.boxcorner.text())
            self.params.minCornerDistanceRate = self.corner
        else:
            self.params.minCornerDistanceRate = self.params.minCornerDistanceRate

        if self.boxmarkerdist.text() !='':
            self.markerdist = float(self.boxmarkerdist.text())
            self.params.minMarkerDistanceRate = self.markerdist
        else:
            self.params.minMarkerDistanceRate = self.params.minMarkerDistanceRate

        if self.boxborderdist.text() !='':
            self.borderdist = int(self.boxborderbits.text())
            self.params.minDistanceToBorder = self.borderdist
        else:
            self.params.minDistanceToBorder = self.params.minDistanceToBorder

        if self.boxborderbits.text() !='':
            self.borderbits = int(self.boxborderbits.text())
            self.params.markerBorderBits = self.borderbits
        else:
            self.params.markerBorderBits = self.params.markerBorderBits

        if self.boxotsu.text() !='':
            self.otsu = float(self.boxotsu.text())
            self.params.minOtsuStdDev = self.otsu
        else:
            self.params.minOtsuStdDev = self.params.minOtsuStdDev

        if self.boxpersp.text() !='':
            self.persp = int(self.boxpersp.text())
            self.params.perspectiveRemovePixelPerCell = self.persp
        else:
            self.params.perspectiveRemovePixelPerCell = self.params.perspectiveRemovePixelPerCell

        if self.boxerror.text() !='':
            self.error = float(self.boxerror.text())
            self.params.maxErroneousBitsInBorderRate = self.error
        else:
            self.params.maxErroneousBitsInBorderRate = self.params.maxErroneousBitsInBorderRate

        if self.boxcorrect.text() !='':
            self.correct = float(self.boxcorrect.text())
            self.params.errorCorrectionRate = self.correct
        else:
            self.params.errorCorrectionRate = self.params.errorCorrectionRate

        if self.boxrefinement.text() !='':
            self.refinement = int(self.boxrefinement.text())
            self.params.cornerRefinementMethod = self.refinement
        else:
            self.params.cornerRefinementMethod = self.params.cornerRefinementMethod

        if self.boxrefwin.text() !='':
            self.refwin = int(self.boxrefwin.text())
            self.params.cornerRefinementWinSize = self.refwin
        else:
            self.params.cornerRefinementWinSize = self.params.cornerRefinementWinSize

        if self.boxmaxiter.text() !='':
            self.maxiter = int(self.boxmaxiter.text())
            self.params.cornerRefinementMaxIterations = self.maxiter
        else:
            self.params.cornerRefinementMaxIterations = self.params.cornerRefinementMaxIterations

        if self.boxminacc.text() !='':
            self.minacc = float(self.boxminacc.text())
            self.params.cornerRefinementMinAccuracy = self.minacc
        else:
            self.params.cornerRefinementMinAccuracy = self.params.cornerRefinementMinAccuracy

        if self.comboInverted.currentText() == 'False':
            self.params.detectInvertedMarker = False
        else:
            self.params.detectInvertedMarker = True

        self.close()

class Ui_MainWindow(QtWidgets.QGraphicsView,QtWidgets.QWidget):
    """ Class for main window
    """
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent=None):
        super().__init__(parent)

        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1377, 760)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setWindowIcon(QtGui.QIcon('fgcp_logo.png'))
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.ParameterWindow = ParameterWin()
        self.index = 0
        self.path_ = None
        self.img_name = None
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1361, 721))
        self.tabWidget.setMaximumSize(QtCore.QSize(1800, 1800))
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
        self.label.setGeometry(QtCore.QRect(30, 10, 351, 31))
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
        self.GMcomboBox.setObjectName("GMcomboBox")
        self.GMpushButton = QtWidgets.QPushButton(self.tab, clicked=lambda:self.generate())
        self.GMpushButton.setGeometry(QtCore.QRect(310, 70, 131, 31))
        self.GMpushButton.setObjectName("GMpushButton")
        self.GMpushButton.setStyleSheet("QPushButton{color:white;\n"
                                    "background-color: rgb(0, 120, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;}\n"
                                    "QPushButton:hover{border:2px solid;\n"
                                    "background-color: rgb(0, 120, 210);}\n")
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
        self.EDpathButton_3.setObjectName("EDpathButton_3")
        self.EDpathButton_3.setStyleSheet("QPushButton{color:white;\n"
                                    "background-color: rgb(0, 120, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;}\n"
                                    "QPushButton:hover{border:2px solid;\n"
                                    "background-color: rgb(0, 120, 210);}\n")
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
        self.EDsubmitButton_2.setStyleSheet("QPushButton{color:white;\n"
                                    "background-color: rgb(0, 70, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;}\n"
                                    "QPushButton:hover{border:2px solid;\n"
                                    "background-color: rgb(0, 70, 200);}\n")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.EDsubmitButton_2.setFont(font)
        self.EDsubmitButton_2.setObjectName("EDsubmitButton_2")
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
        self.EDClrBtn.setStyleSheet("QPushButton{color:white;\n"
                                    "background-color: rgb(0, 120, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;}\n"
                                    "QPushButton:hover{border:2px solid;\n"
                                    "background-color: rgb(0, 120, 200);}\n")
        self.EDClrBtn.setObjectName("EDClrBtn")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.next = QtWidgets.QPushButton(self.tab_3, clicked=lambda:self.nxt())
        self.next.setGeometry(QtCore.QRect(380, 580, 31, 31))
        self.next.setObjectName("next")
        self.previous = QtWidgets.QPushButton(self.tab_3, clicked=lambda:self.prvs())
        self.previous.setGeometry(QtCore.QRect(349, 580, 31, 31))
        self.previous.setObjectName("previous")
        self.selectimage = QtWidgets.QRadioButton(self.tab_3)
        self.selectimage.setGeometry(QtCore.QRect(180, 590, 111, 17))
        self.selectimage.setChecked(False)
        self.selectimage.setObjectName("selectimage")
        self.selectdir = QtWidgets.QRadioButton(self.tab_3)
        self.selectdir.setGeometry(QtCore.QRect(450, 590, 121, 17))
        self.selectdir.setChecked(False)
        self.selectdir.setObjectName("selectdir")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.run = QtWidgets.QPushButton(self.tab_3, clicked=lambda:self.runn())
        self.run.setGeometry(QtCore.QRect(180, 620, 391, 31))
        self.run.setObjectName("run")
        self.run.setFont(font)
        self.run.setStyleSheet("QPushButton{color:white;\n"
                                "background-color: rgb(0, 70, 255);\n"
                                "border-style:outset;\n"
                                "border-width: 2px;\n"
                                "border-radius:10px;\n"
                                "border-color:black;\n"
                                "padding:4px;\n"
                                "min-width:10px;}\n"
                                "QPushButton:hover{border:2px solid;\n"
                                "background-color: rgb(0, 70, 200);}\n")
        self.outputs = QtWidgets.QListWidget(self.tab_3)
        self.outputs.setGeometry(QtCore.QRect(890, 30, 471, 621))
        self.outputs.setObjectName("outputs")
        self.outputs.setStyleSheet("color:white;\n"
                                   "background-color:rgb(99,102,106);\n"
                                   "font:bold 12px;")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.clrresult = QtWidgets.QPushButton(self.tab_3, clicked=lambda:self.clrOutput())
        self.clrresult.setGeometry(QtCore.QRect(1270, 0, 91, 31))
        self.clrresult.setObjectName("clrresult")
        self.clrresult.setFont(font)
        self.clrresult.setStyleSheet("QPushButton{color:white;\n"
                                    "background-color: rgb(0, 120, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;}\n"
                                    "QPushButton:hover{border:2px solid;\n"
                                    "background-color: rgb(0, 120, 200);}\n")

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.selectpath = QtWidgets.QPushButton(self.tab_3, clicked=lambda:self.imPath())
        self.selectpath.setGeometry(QtCore.QRect(600, 590, 111, 21))
        self.selectpath.setObjectName("selectpath")
        self.selectpath.setFont(font)
        self.selectpath.setStyleSheet("QPushButton{color:white;\n"
                                    "background-color: rgb(0, 120, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;}\n"
                                    "QPushButton:hover{border:2px solid;\n"
                                    "background-color: rgb(0, 120, 200);}\n")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.imgname = QtWidgets.QLabel(self.tab_3)
        self.imgname.setGeometry(QtCore.QRect(10, 590, 131, 16))
        self.imgname.setFont(font)
        self.imgname.setObjectName("imgname")
        self.checkmark = QtWidgets.QCheckBox(self.tab_3)
        self.checkmark.setGeometry(QtCore.QRect(730, 590, 131, 20))
        self.checkmark.setFont(font)
        self.checkmark.setObjectName("checkmark")
        self.checkmark.toggled.connect(lambda:self.markMarker())
        self.photoClicked.connect(self.clickMarker)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pbar = QtWidgets.QProgressBar(self.tab_3)
        self.pbar.setGeometry(QtCore.QRect(890, 0, 160, 31))
        self.pbar.setFont(font)
        self.pbar.setObjectName("resultbar")
        self.pbar.setTextVisible(True)
        self.pbar.setValue(0)
        self.pbar.setFormat("Results")
        self.pbar.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.openparm = QtWidgets.QPushButton(self.tab_3, clicked=lambda:self.paramWindow())
        self.openparm.setGeometry(QtCore.QRect(600, 620, 111, 31))
        self.openparm.setObjectName("openparm")
        self.openparm.setFont(font)
        self.openparm.setStyleSheet("QPushButton{color:white;\n"
                                    "background-color: rgb(0, 120, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;}\n"
                                    "QPushButton:hover{border:2px solid;\n"
                                    "background-color: rgb(0, 120, 200);}\n")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.delresult = QtWidgets.QPushButton(self.tab_3, clicked=lambda:self.delResults())
        self.delresult.setGeometry(QtCore.QRect(1160, 0, 101, 31))
        self.delresult.setObjectName("delresult")
        self.delresult.setFont(font)
        self.delresult.setStyleSheet("QPushButton{color:white;\n"
                                    "background-color: rgb(0, 120, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;}\n"
                                    "QPushButton:hover{border:2px solid;\n"
                                    "background-color: rgb(0, 120, 200);}\n")
        self.createfile = QtWidgets.QPushButton(self.tab_3, clicked=lambda:self.createFile())
        self.createfile.setGeometry(QtCore.QRect(1050, 0, 101, 31))
        self.createfile.setObjectName("createfile")
        self.createfile.setFont(font)
        self.createfile.setStyleSheet("QPushButton{color:white;\n"
                                    "background-color: rgb(0, 120, 255);\n"
                                    "border-style:outset;\n"
                                    "border-width: 2px;\n"
                                    "border-radius:10px;\n"
                                    "border-color:black;\n"
                                    "padding:4px;\n"
                                    "min-width:10px;}\n"
                                    "QPushButton:hover{border:2px solid;\n"
                                    "background-color: rgb(0, 120, 200);}\n")
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_3)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 841, 571))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.addWidget(self)
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1377, 21))
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
        self.selectimage.setChecked(True)
        self.updating_btn(False, False)
        self.checkmark.setChecked(False)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Find-GCP"))
        self.label.setText(_translate("MainWindow", "Select Marker Type"))
        self.GMpushButton.setText(_translate("MainWindow", "Generate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Generate Marker"))
        self.ED1radioButton.setText(_translate("MainWindow", "Select Image"))
        self.EDradioButton_2.setText(_translate("MainWindow", "Select Directory"))
        self.EDpathButton_3.setText(_translate("MainWindow", "Path"))
        self.EDlabel_2.setText(_translate("MainWindow", "Image Preview Will Appear Here"))
        self.EDsubmitButton_2.setText(_translate("MainWindow", "Submit"))
        self.EDlabel_3.setText(_translate("MainWindow", "Results"))
        self.EDClrBtn.setText(_translate("MainWindow", "Clear Results"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Exif Data"))
        self.next.setText(_translate("MainWindow", ">"))
        self.previous.setText(_translate("MainWindow", "<"))
        self.selectimage.setText(_translate("MainWindow", "Select Image"))
        self.selectdir.setText(_translate("MainWindow", "Select Directory"))
        self.run.setText(_translate("MainWindow", "Submit"))
        self.clrresult.setText(_translate("MainWindow", "Clear Results"))
        self.selectpath.setText(_translate("MainWindow", "Select Path"))
        self.openparm.setText(_translate("MainWindow", "Set Parameters"))
        self.delresult.setText(_translate("MainWindow", "Delete Result"))
        self.createfile.setText(_translate("MainWindow", "Create File"))
        self.imgname.setText(_translate("MainWindow", ""))
        self.checkmark.setText(_translate("MainWindow", "Mark Undetected"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Find GCP"))

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
            "JPG File (*.jpg);; PNG File (*.png);;")
            self.pixmap = QPixmap(self.path_)
            self.EDlabel_2.setPixmap(self.pixmap)
        elif self.EDradioButton_2.isChecked():
            self.path_ = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory", os.getcwd())
            self.path_ = self.path_ +'/*.[jJ][pP][gG]'

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
            if exif !=None:
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

    def paramWindow(self):
        self.ParameterWindow.display()

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(Ui_MainWindow, self).mousePressEvent(event)

    def markMarker(self):
        if self.checkmark.isChecked() == True:
            self.toggleDragMode()
        elif self.checkmark.isChecked() == False:
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def clickMarker(self, pos):
        if self.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
            self.outputs.addItem('%d %d %s' % (pos.x(), pos.y(),
            re.split(r' |/|\\',self.img_name[self.index_])[-1]))


    def imPath(self):
        if self.selectimage.isChecked():
            self.path_, _ = QtWidgets.QFileDialog.getOpenFileNames(None, "Select Image",os.getcwd(),
            "JPG File (*.jpg);; PNG File (*.png);;")
            self.img_name = [img for img in self.path_]
            self.current_index = 0
        elif self.selectdir.isChecked():
            self.path_ = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory", os.getcwd())
            self.path_ = self.path_ +'/*.[jJ][pP][gG]'
            self.img_name = [img for img in glob.iglob(self.path_)]
            self.current_index = 0

    def nxt(self):
        self.current_index += 1

    def prvs(self):
        self.current_index -= 1

    @property
    def current_index(self):
        return self.index_

    @current_index.setter
    def current_index(self, img_index):
        if img_index <= 0 and len(self.img_name) <= 0:
            self.updating_btn(False, False)
        elif img_index < 0:
            self.updating_btn(False, True)
        elif img_index >= (len(self.img_name) -1):
            self.updating_btn(True, False)
        else:
            self.updating_btn(True, True)

        if 0 <= img_index < len(self.img_name):
            self.index_= img_index
            filename = self.img_name[self.index_]
            self.imgname.setText(re.split(r' |/|\\',filename)[-1])
            pixmap = QPixmap(filename)
            self.setPhoto(pixmap)
        self.markMarker()

    def updating_btn(self, previous, next):
        if self.checkmark.isChecked() == True:
            self.toggleDragMode()
        self.previous.setEnabled(previous)
        self.next.setEnabled(next)

    def runn(self):
        def getImage(img):
            gcp_found = {}
            coords = {}
            gcps = []

            if 'dng' in img.lower():
                dng = DngFile.read(img)
                image = dng.postprocess()  # demosaicing by rawpy
            else :
                image = cv2.imread(img)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if f'{self.ParameterWindow.combomt.currentText()}' != 'DICT_3X3':
                arucoDict = cv2.aruco.Dictionary_get(ARUCO_TYPE.get(self.ParameterWindow.combomt.currentText()))
            else:
                arucoDict = ARUCO_TYPE['DICT_3X3']
            (corners, ids, rejected) = cv2.aruco.detectMarkers(gray,arucoDict,
             parameters=self.ParameterWindow.params)

            if self.ParameterWindow.ipath.endswith('.txt'):
                if not os.path.isfile(self.ParameterWindow.ipath) or \
                    not os.access(self.ParameterWindow.ipath, os.R_OK):
                    self.outputs.addItem('cannot open input file {}'.format(self.ParameterWindow.ipath))
                else:
                    with open(self.ParameterWindow.ipath, 'r') as finput:
                        for line in finput:
                            co_list = line.strip().split(self.ParameterWindow.boxseperator.text())
                            if len(co_list) < 4:
                                self.outputs.addItem("Illegal input: {}".format(line))
                                continue
                            coords[int(co_list[0])] = [float(x) for x in co_list[1:4]]

            def gcp_f(gcp_found):
                if self.ParameterWindow.ipath.endswith('.txt'):
                    print("processing {}".format(img))
                    for j in gcp_found:

                        print('GCP{}: on {} images {}'.format(j, len(gcp_found[j]),
                                                            gcp_found[j]))
                    print('{} GCP markers found'.format(ids.size))

            def verbose(verb):
                if self.ParameterWindow.ipath.endswith('.txt'):
                    for j in verb:
                        print('GCP{}: on {} images {}'.format(j, len(verb[j]),
                                                        verb[j]))
            if len(corners) > 0:
                for i in range(ids.size):
                    j = ids[i][0]
                    if j not in gcp_found:
                        gcp_found[j] = []
                    gcp_found[j].append(img)
                    x = int(round(np.average(corners[i][0][:, 0])))
                    y = int(round(np.average(corners[i][0][:, 1])))
                    gcps.append((x, y, os.path.basename(img), j))
                gcp_f(gcp_found)
                verbose(gcp_found)

            for gcp in gcps:
                j = gcp[3]
                if f'{self.ParameterWindow.combosoft.currentText()}' != 'Select' and \
                    f'{self.ParameterWindow.combosoft.currentText()}' == 'ODM':
                    if j in coords and self.ParameterWindow.boxlimit.text() != "":
                        if len(gcp_found[j]) <= int(self.ParameterWindow.boxlimit.text()):
                            self.outputs.addItem(('{:.3f} {:.3f} {:.3f} {} {} {} {}'.format(
                                coords[j][0], coords[j][1], coords[j][2],
                                gcp[0], gcp[1], gcp[2], j)))
                        else:
                            self.outputs.addItem("GCP {} over limit it is dropped on image {}".format(
                                j, gcp[2]))
                    else:
                        self.outputs.addItem("No coordinates for {}".format(j))
                elif f'{self.ParameterWindow.combosoft.currentText()}' == 'VisualSfM':
                    if j in coords and self.ParameterWindow.boxlimit.text() != "":
                        if len(gcp_found[j]) <= int(self.ParameterWindow.boxlimit.text()):
                            self.outputs.addItem('{} {} {} {:.3f} {:.3f} {:.3f} {}'.format(
                                gcp[2], gcp[0], gcp[1],
                                coords[j][0], coords[j][1], coords[j][2], j))
                        else:
                            self.outputs.addItem("GCP {} over limit it is dropped on image {}".format(
                                j, gcp[2]))
                    else:
                        self.outputs("No coordinates for {}".format(j))

                else:
                    if j in coords and self.ParameterWindow.boxlimit.text() != "":
                        if len(gcp_found[j]) <= int(self.ParameterWindow.boxlimit.text()):
                            self.outputs.addItem('{:.3f} {:.3f} {:.3f} {} {} {} {}'.format(
                                coords[j][0], coords[j][1], coords[j][2],
                                gcp[0], gcp[1], gcp[2], j))
                        else:
                            self.outputs.addItem("GCP {} over limit it is dropped on image {}".format(
                                j, gcp[2]))
                    else:
                        if len(gcp_found[j]) <= int(self.ParameterWindow.boxlimit.text()):
                            self.outputs.addItem('{} {} {} {}'.format(
                                gcp[0], gcp[1], gcp[2], j))
                        else:
                            self.outputs.addItem("GCP {} over limit it is dropped on image {}".format(
                                j, gcp[2]))

        checkProgress = 0
        if self.img_name:
            self.pbar.setRange(0,len(self.img_name))
            self.pbar.setFormat("Progress")

        if type(self.path_) == list:
            for img in self.path_:
                checkProgress +=1
                getImage(img)
                self.pbar.setValue(checkProgress)
        else:
            for img in glob.iglob(f"{self.path_}"):
                checkProgress +=1
                getImage(img)
                QtWidgets.QApplication.processEvents()
                self.pbar.setValue(checkProgress)
        sleep(0.05)
        self.pbar.setValue(0)
        self.pbar.setFormat("Results")

    def clrOutput(self):
        self.outputs.clear()

    def createFile(self):
        listresults = [self.outputs.item(i).text() for i in range(self.outputs.count())]
        if self.ParameterWindow.outputfile.text() != '':
            try:
                with open(f'{self.ParameterWindow.outputfile.text()}.txt', 'w') as finput:
                    if self.ParameterWindow.boxespg.text() != '':
                        finput.write('EPSG:{}'.format(self.ParameterWindow.boxespg.text()+'\n'))

                    for r in listresults:
                        finput.writelines(r+'\n')
                    finput.close()
            except Exception:
                self.outputs.addItem('Cannot Open')

    def delResults(self):
        delete = self.outputs.currentRow()
        self.outputs.takeItem(delete)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
