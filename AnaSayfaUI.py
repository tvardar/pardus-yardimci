# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AnaSayfaUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(955, 490)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(955, 490))
        MainWindow.setMaximumSize(QtCore.QSize(955, 490))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Pardus.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 80, 931, 361))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(410, 75, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_17 = QtWidgets.QLabel(self.tab)
        self.label_17.setGeometry(QtCore.QRect(410, 125, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.lblServissagla = QtWidgets.QLabel(self.tab)
        self.lblServissagla.setGeometry(QtCore.QRect(590, 125, 341, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblServissagla.setFont(font)
        self.lblServissagla.setObjectName("lblServissagla")
        self.lblYerelip = QtWidgets.QLabel(self.tab)
        self.lblYerelip.setGeometry(QtCore.QRect(590, 175, 261, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblYerelip.setFont(font)
        self.lblYerelip.setObjectName("lblYerelip")
        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setGeometry(QtCore.QRect(410, 26, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.lblSistem = QtWidgets.QLabel(self.tab)
        self.lblSistem.setGeometry(QtCore.QRect(189, 27, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblSistem.setFont(font)
        self.lblSistem.setObjectName("lblSistem")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(9, 125, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(11, 290, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.lblDagitim = QtWidgets.QLabel(self.tab)
        self.lblDagitim.setGeometry(QtCore.QRect(189, 175, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblDagitim.setFont(font)
        self.lblDagitim.setObjectName("lblDagitim")
        self.lblKernel = QtWidgets.QLabel(self.tab)
        self.lblKernel.setGeometry(QtCore.QRect(189, 125, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblKernel.setFont(font)
        self.lblKernel.setObjectName("lblKernel")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(9, 175, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lblLocalhost = QtWidgets.QLabel(self.tab)
        self.lblLocalhost.setGeometry(QtCore.QRect(590, 225, 261, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblLocalhost.setFont(font)
        self.lblLocalhost.setObjectName("lblLocalhost")
        self.lblUlke = QtWidgets.QLabel(self.tab)
        self.lblUlke.setGeometry(QtCore.QRect(590, 26, 261, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblUlke.setFont(font)
        self.lblUlke.setObjectName("lblUlke")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(410, 225, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.lblSehir = QtWidgets.QLabel(self.tab)
        self.lblSehir.setGeometry(QtCore.QRect(590, 75, 221, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblSehir.setFont(font)
        self.lblSehir.setObjectName("lblSehir")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(9, 27, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(410, 175, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.lineip = QtWidgets.QLineEdit(self.tab)
        self.lineip.setGeometry(QtCore.QRect(190, 288, 121, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lineip.setFont(font)
        self.lineip.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.lineip.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineip.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineip.setAlignment(QtCore.Qt.AlignCenter)
        self.lineip.setObjectName("lineip")
        self.btngoster = QtWidgets.QPushButton(self.tab)
        self.btngoster.setGeometry(QtCore.QRect(320, 288, 51, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btngoster.setFont(font)
        self.btngoster.setIconSize(QtCore.QSize(25, 25))
        self.btngoster.setAutoDefault(False)
        self.btngoster.setFlat(False)
        self.btngoster.setObjectName("btngoster")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(411, 290, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.linewifi = QtWidgets.QLineEdit(self.tab)
        self.linewifi.setGeometry(QtCore.QRect(590, 288, 121, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.linewifi.setFont(font)
        self.linewifi.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.linewifi.setEchoMode(QtWidgets.QLineEdit.Password)
        self.linewifi.setAlignment(QtCore.Qt.AlignCenter)
        self.linewifi.setObjectName("linewifi")
        self.btngoster2 = QtWidgets.QPushButton(self.tab)
        self.btngoster2.setGeometry(QtCore.QRect(720, 288, 51, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btngoster2.setFont(font)
        self.btngoster2.setIconSize(QtCore.QSize(25, 25))
        self.btngoster2.setObjectName("btngoster2")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(10, 75, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.lblPcadi = QtWidgets.QLabel(self.tab)
        self.lblPcadi.setGeometry(QtCore.QRect(190, 76, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblPcadi.setFont(font)
        self.lblPcadi.setObjectName("lblPcadi")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setGeometry(QtCore.QRect(10, 225, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.lblKullanici = QtWidgets.QLabel(self.tab)
        self.lblKullanici.setGeometry(QtCore.QRect(190, 225, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblKullanici.setFont(font)
        self.lblKullanici.setObjectName("lblKullanici")
        self.line = QtWidgets.QFrame(self.tab)
        self.line.setGeometry(QtCore.QRect(380, 20, 16, 291))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.lblIslemci = QtWidgets.QLabel(self.tab_2)
        self.lblIslemci.setGeometry(QtCore.QRect(190, 27, 791, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblIslemci.setFont(font)
        self.lblIslemci.setObjectName("lblIslemci")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(10, 27, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lblekrankart = QtWidgets.QLabel(self.tab_2)
        self.lblekrankart.setGeometry(QtCore.QRect(190, 77, 791, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblekrankart.setFont(font)
        self.lblekrankart.setObjectName("lblekrankart")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(10, 77, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lblseskart = QtWidgets.QLabel(self.tab_2)
        self.lblseskart.setGeometry(QtCore.QRect(190, 127, 791, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblseskart.setFont(font)
        self.lblseskart.setObjectName("lblseskart")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(10, 127, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_18 = QtWidgets.QLabel(self.tab_2)
        self.label_18.setGeometry(QtCore.QRect(10, 177, 161, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.tab_2)
        self.label_19.setGeometry(QtCore.QRect(192, 178, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.tab_2)
        self.label_20.setGeometry(QtCore.QRect(333, 178, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.lblRamtoplam = QtWidgets.QLabel(self.tab_2)
        self.lblRamtoplam.setGeometry(QtCore.QRect(262, 180, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblRamtoplam.setFont(font)
        self.lblRamtoplam.setObjectName("lblRamtoplam")
        self.lblRamkullanilan = QtWidgets.QLabel(self.tab_2)
        self.lblRamkullanilan.setGeometry(QtCore.QRect(423, 180, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblRamkullanilan.setFont(font)
        self.lblRamkullanilan.setObjectName("lblRamkullanilan")
        self.lblhdd1kullan = QtWidgets.QLabel(self.tab_2)
        self.lblhdd1kullan.setGeometry(QtCore.QRect(423, 240, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblhdd1kullan.setFont(font)
        self.lblhdd1kullan.setObjectName("lblhdd1kullan")
        self.label_21 = QtWidgets.QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(333, 238, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.label_22 = QtWidgets.QLabel(self.tab_2)
        self.label_22.setGeometry(QtCore.QRect(11, 238, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.lblhdd1toplam = QtWidgets.QLabel(self.tab_2)
        self.lblhdd1toplam.setGeometry(QtCore.QRect(262, 240, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblhdd1toplam.setFont(font)
        self.lblhdd1toplam.setObjectName("lblhdd1toplam")
        self.label_23 = QtWidgets.QLabel(self.tab_2)
        self.label_23.setGeometry(QtCore.QRect(192, 238, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setObjectName("label_23")
        self.lblRambos = QtWidgets.QLabel(self.tab_2)
        self.lblRambos.setGeometry(QtCore.QRect(543, 180, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblRambos.setFont(font)
        self.lblRambos.setObjectName("lblRambos")
        self.lblhdd1bos = QtWidgets.QLabel(self.tab_2)
        self.lblhdd1bos.setGeometry(QtCore.QRect(543, 240, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.lblhdd1bos.setFont(font)
        self.lblhdd1bos.setObjectName("lblhdd1bos")
        self.label_33 = QtWidgets.QLabel(self.tab_2)
        self.label_33.setGeometry(QtCore.QRect(483, 238, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.label_34 = QtWidgets.QLabel(self.tab_2)
        self.label_34.setGeometry(QtCore.QRect(483, 178, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_34.setFont(font)
        self.label_34.setObjectName("label_34")
        self.line_2 = QtWidgets.QFrame(self.tab_2)
        self.line_2.setGeometry(QtCore.QRect(10, 210, 901, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_13 = QtWidgets.QLabel(self.tab_3)
        self.label_13.setGeometry(QtCore.QRect(13, 30, 251, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.btnupdate = QtWidgets.QPushButton(self.tab_3)
        self.btnupdate.setGeometry(QtCore.QRect(223, 25, 171, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btnupdate.setFont(font)
        self.btnupdate.setObjectName("btnupdate")
        self.label_24 = QtWidgets.QLabel(self.tab_3)
        self.label_24.setGeometry(QtCore.QRect(13, 77, 251, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.btnremove = QtWidgets.QPushButton(self.tab_3)
        self.btnremove.setGeometry(QtCore.QRect(223, 74, 171, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btnremove.setFont(font)
        self.btnremove.setObjectName("btnremove")
        self.btnbagimlilik = QtWidgets.QPushButton(self.tab_3)
        self.btnbagimlilik.setGeometry(QtCore.QRect(223, 173, 171, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btnbagimlilik.setFont(font)
        self.btnbagimlilik.setObjectName("btnbagimlilik")
        self.label_30 = QtWidgets.QLabel(self.tab_3)
        self.label_30.setGeometry(QtCore.QRect(13, 127, 181, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.label_31 = QtWidgets.QLabel(self.tab_3)
        self.label_31.setGeometry(QtCore.QRect(13, 177, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.tab_3)
        self.label_32.setGeometry(QtCore.QRect(471, 29, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.btngrubguncelle = QtWidgets.QPushButton(self.tab_3)
        self.btngrubguncelle.setGeometry(QtCore.QRect(710, 27, 171, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btngrubguncelle.setFont(font)
        self.btngrubguncelle.setObjectName("btngrubguncelle")
        self.btnpaketduzelt = QtWidgets.QPushButton(self.tab_3)
        self.btnpaketduzelt.setGeometry(QtCore.QRect(223, 125, 171, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btnpaketduzelt.setFont(font)
        self.btnpaketduzelt.setObjectName("btnpaketduzelt")
        self.line_3 = QtWidgets.QFrame(self.tab_3)
        self.line_3.setGeometry(QtCore.QRect(430, 20, 20, 271))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 955, 22))
        self.menubar.setObjectName("menubar")
        self.menuMEN = QtWidgets.QMenu(self.menubar)
        self.menuMEN.setTearOffEnabled(True)
        self.menuMEN.setObjectName("menuMEN")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuhakkinda = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("hakkinda.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuhakkinda.setIcon(icon1)
        self.menuhakkinda.setObjectName("menuhakkinda")
        self.menucikis = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("cikis.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menucikis.setIcon(icon2)
        self.menucikis.setShortcutVisibleInContextMenu(True)
        self.menucikis.setObjectName("menucikis")
        self.menuMEN.addAction(self.menuhakkinda)
        self.menuMEN.addSeparator()
        self.menuMEN.addAction(self.menucikis)
        self.menubar.addAction(self.menuMEN.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.menucikis.triggered.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pardus Yardımcı"))
        self.label_15.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Şehir : </span></p></body></html>"))
        self.label_17.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Servis Sağlayıcı : </span></p></body></html>"))
        self.lblServissagla.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.lblYerelip.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:400;\"><br/></span></p></body></html>"))
        self.label_14.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Ülke : </span></p></body></html>"))
        self.lblSistem.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:400;\"><br/></span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Kernel Versiyonu  : </span></p></body></html>"))
        self.label_11.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Harici İp </span><span style=\" font-size:9pt; font-weight:600; color:#1a5fb4;\">(</span><span style=\" font-size:9pt; font-weight:600; color:#cc0000;\">Paylaşmayın !!</span><span style=\" font-size:9pt; font-weight:600; color:#1a5fb4;\">)</span><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\"> : </span></p></body></html>"))
        self.lblDagitim.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:400;\"><br/></span></p></body></html>"))
        self.lblKernel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:400;\"><br/></span></p></body></html>"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Dağıtım : </span></p></body></html>"))
        self.lblLocalhost.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:400;\"><br/></span></p></body></html>"))
        self.lblUlke.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">LocalHost : </span></p></body></html>"))
        self.lblSehir.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Sistem : </span></p></body></html>"))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Yerel İp : </span></p></body></html>"))
        self.lineip.setPlaceholderText(_translate("MainWindow", "İnternete Bağlan"))
        self.btngoster.setText(_translate("MainWindow", "Göster"))
        self.label_12.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#1a5fb4;\">Wi-Fi Şifresi </span><span style=\" font-size:9pt; color:#1a5fb4;\">(</span><span style=\" font-size:9pt; color:#cc0000;\">Dikkat !!</span><span style=\" font-size:9pt; color:#1a5fb4;\">)</span><span style=\" color:#1a5fb4;\"> : </span></p></body></html>"))
        self.linewifi.setPlaceholderText(_translate("MainWindow", "Wifi Şifresi"))
        self.btngoster2.setText(_translate("MainWindow", "Göster"))
        self.label_10.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Pc Adı : </span></p></body></html>"))
        self.lblPcadi.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:400;\"><br/></span></p></body></html>"))
        self.label_16.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Kullanıcı Adı : </span></p></body></html>"))
        self.lblKullanici.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:400;\"><br/></span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Sistem ve Ağ Bilgileri"))
        self.lblIslemci.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:400;\"><br/></span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">İşlemci : </span></p></body></html>"))
        self.lblekrankart.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Ekran Kartı : </span></p></body></html>"))
        self.lblseskart.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Ses Kartı : </span></p></body></html>"))
        self.label_18.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Ram Bilgileri : </span></p></body></html>"))
        self.label_19.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#e66100;\">Toplam :</span></p></body></html>"))
        self.label_20.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#e66100;\">Kullanılan :</span></p></body></html>"))
        self.lblRamtoplam.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.lblRamkullanilan.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.lblhdd1kullan.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label_21.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#e66100;\">Kullanılan :</span></p></body></html>"))
        self.label_22.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#1a5fb4;\">HDD Bilgileri : </span></p></body></html>"))
        self.lblhdd1toplam.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label_23.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#e66100;\">Toplam :</span></p></body></html>"))
        self.lblRambos.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.lblhdd1bos.setText(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label_33.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#e66100;\">Boşta :</span></p></body></html>"))
        self.label_34.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#e66100;\">Boşta :</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Donanım Bilgileri"))
        self.label_13.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Sistemi Güncelle : </span></p></body></html>"))
        self.btnupdate.setText(_translate("MainWindow", "Güncelle"))
        self.label_24.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#1a5fb4;\">Sistemi Temizle : </span></p></body></html>"))
        self.btnremove.setText(_translate("MainWindow", "Temizle"))
        self.btnbagimlilik.setText(_translate("MainWindow", "Bağımlılıkları Tamamla"))
        self.label_30.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#1a5fb4;\">Bozuk Paketleri Düzelt :</span></p></body></html>"))
        self.label_31.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#1a5fb4;\">Eksik Bağımlılıkları Gider :</span></p></body></html>"))
        self.label_32.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; color:#1a5fb4;\">Grub Güncelle :</span></p></body></html>"))
        self.btngrubguncelle.setText(_translate("MainWindow", "Grub Güncelle"))
        self.btnpaketduzelt.setText(_translate("MainWindow", "Paketleri Düzelt"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Terminal İşlemleri"))
        self.menuMEN.setTitle(_translate("MainWindow", "MENÜ"))
        self.menuhakkinda.setText(_translate("MainWindow", "Hakkinda"))
        self.menucikis.setText(_translate("MainWindow", "Çıkış"))
        self.menucikis.setShortcut(_translate("MainWindow", "Ctrl+X"))
