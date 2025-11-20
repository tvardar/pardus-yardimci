# ana_pencere.py
# Sürüm 1.0 - GitHub Linki Güncellendi

import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QAction

from sayfalar.genel_bakis import GenelBakisSayfasi
from sayfalar.bakim import BakimSayfasi
from sayfalar.diger_sayfalar import SurecYonetimiSayfasi, AgAraclariSayfasi, DonanimSayfasi
from sayfalar.yonetim import YonetimSayfasi
from gorsel_araclar import BilgiIsleyicisi, SvgIkonOlusturucu
from stil_sayfasi import PYQT6_STIL


class AnaPencere(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pardus Yardımcı")  # Başlık Sadeleştirildi
        self.resize(1100, 700)
        self.setMinimumSize(950, 600)

        if getattr(sys, 'frozen', False):
            self.base_dir = sys._MEIPASS
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.icon_path = os.path.join(self.base_dir, "icons", "yardimci.ico")
        if os.path.exists(self.icon_path): self.setWindowIcon(QIcon(self.icon_path))

        self.arayuzu_kur();
        self.tray_kur();
        self.backend_baslat();
        self.setStyleSheet(PYQT6_STIL)

    def get_icon_path(self, filename):
        return os.path.join(self.base_dir, "icons", filename)

    def arayuzu_kur(self):
        ana_widget = QWidget();
        self.setCentralWidget(ana_widget)
        main_layout = QHBoxLayout(ana_widget);
        main_layout.setContentsMargins(0, 0, 0, 0);
        main_layout.setSpacing(0)

        self.menu_panel = QWidget();
        self.menu_panel.setFixedWidth(260);
        self.menu_panel.setObjectName("YanMenu")
        menu_layout = QVBoxLayout(self.menu_panel);
        menu_layout.setContentsMargins(10, 20, 10, 20)

        logo_path = None
        for f in ["yardimci-logo.png", "yardimci.png", "logo.png"]:
            p = self.get_icon_path(f)
            if os.path.exists(p): logo_path = p; break

        if logo_path:
            l = QLabel();
            l.setPixmap(QPixmap(logo_path).scaled(140, 140, Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation))
            l.setAlignment(Qt.AlignmentFlag.AlignCenter);
            l.setStyleSheet("background:transparent; border:none; margin-bottom:10px;");
            menu_layout.addWidget(l)
        else:
            l = QLabel("PARDUS\nYARDIMCI");
            l.setAlignment(Qt.AlignmentFlag.AlignCenter);
            l.setStyleSheet("color: #33AADD; font-weight: bold; font-size: 16pt;");
            menu_layout.addWidget(l)

        t = QLabel("Yönetim Paneli");
        t.setObjectName("UygulamaBaslik");
        t.setAlignment(Qt.AlignmentFlag.AlignCenter);
        t.setStyleSheet("font-size: 14pt; color: #AAAAAA;");
        menu_layout.addWidget(t);
        menu_layout.addSpacing(20)

        self.stack = QStackedWidget()
        self.sayfa_genel = GenelBakisSayfasi()
        self.sayfa_donanim = DonanimSayfasi()
        self.sayfa_surec = SurecYonetimiSayfasi()
        self.sayfa_ag = AgAraclariSayfasi()
        self.sayfa_yonetim = YonetimSayfasi()
        self.sayfa_bakim = BakimSayfasi()
        self.sayfa_hakkinda = self.hakkinda_sayfasi_olustur()

        self.menuler = [
            ("Genel Bakış", "icons/gauge.svg", self.sayfa_genel),
            ("Donanım & Güç", "icons/hardware.svg", self.sayfa_donanim),
            ("Süreç Yönetimi", "icons/process.svg", self.sayfa_surec),
            ("Ağ & Hız Testi", "icons/network.svg", self.sayfa_ag),
            ("Sistem Yönetimi", "icons/chip.svg", self.sayfa_yonetim),
            ("Bakım & Onarım", "icons/maintenance.svg", self.sayfa_bakim),
            ("Hakkında", "icons/info.svg", self.sayfa_hakkinda)
        ]

        for i, (ad, ico, w) in enumerate(self.menuler):
            b = QPushButton(ad);
            b.setObjectName("MenuDugmesi");
            b.setCheckable(True);
            b.setCursor(Qt.CursorShape.PointingHandCursor)

            ipath = self.get_icon_path(ico.split('/')[-1])
            if os.path.exists(ipath):
                b.setIcon(QIcon(ipath))
            elif "chip.svg" in ico:
                b.setIcon(QIcon(SvgIkonOlusturucu.ayarlar_ikonu()))

            b.setIconSize(QSize(22, 22))
            if i == 0: b.setChecked(True)
            b.clicked.connect(lambda c, idx=i: self.sayfa_degistir(idx))
            menu_layout.addWidget(b);
            self.stack.addWidget(w)

        menu_layout.addStretch();
        main_layout.addWidget(self.menu_panel);
        main_layout.addWidget(self.stack)

    def tray_kur(self):
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray = QSystemTrayIcon(self)
            if os.path.exists(self.icon_path):
                self.tray.setIcon(QIcon(self.icon_path))
            else:
                self.tray.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))

            menu = QMenu()
            show_act = QAction("Göster", self);
            show_act.triggered.connect(self.showNormal)
            quit_act = QAction("Çıkış", self);
            quit_act.triggered.connect(QApplication.instance().quit)
            menu.addAction(show_act);
            menu.addAction(quit_act)

            self.tray.setContextMenu(menu);
            self.tray.show();
            self.tray.setToolTip("Pardus Yardımcı Çalışıyor")

    def closeEvent(self, event):
        if self.tray.isVisible():
            self.hide();
            event.ignore()

    def hakkinda_sayfasi_olustur(self):
        w = QWidget();
        l = QVBoxLayout(w);
        l.setAlignment(Qt.AlignmentFlag.AlignCenter);
        l.setSpacing(15)
        logo_path = None
        for f in ["yardimci-logo.png", "yardimci.png", "logo.png"]:
            p = self.get_icon_path(f);
            if os.path.exists(p): logo_path = p; break
        if logo_path:
            img = QLabel();
            img.setPixmap(QPixmap(logo_path).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                                    Qt.TransformationMode.SmoothTransformation))
            img.setAlignment(Qt.AlignmentFlag.AlignCenter);
            l.addWidget(img)

        l.addWidget(QLabel("<h1 style='color:#33AADD; margin-bottom:0px;'>Pardus Yardımcı</h1>"))

        # --- SÜRÜM GÜNCELLEMESİ ---
        l.addWidget(QLabel("<h3 style='color:#AAAAAA; margin-top:0px;'>Sürüm 1.0</h3>"))
        # --------------------------

        desc = QLabel(
            "Linux sistem yönetimini kolaylaştıran, açık kaynaklı ve\nkullanıcı dostu bir sistem yönetim aracıdır.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter);
        desc.setStyleSheet("font-size: 11pt; color: #E0E0E0;")
        l.addWidget(desc)
        l.addSpacing(20)

        style = "color: #33AADD; text-decoration: none; font-size: 11pt; font-weight:bold;"
        l.addWidget(QLabel(f'<a href="mailto:tarikvardar@gmail.com" style="{style}">📧 tarikvardar@gmail.com</a>'))

        # --- GITHUB LİNKİ GÜNCELLEMESİ ---
        l.addWidget(QLabel(
            f'<a href="https://github.com/tvardar/pardus-yardimci" style="{style}">🐙 github.com/tvardar/pardus-yardimci</a>'))
        # ---------------------------------

        for i in range(l.count()):
            if l.itemAt(i).widget(): l.itemAt(i).widget().setOpenExternalLinks(True)

        l.addStretch()
        l.addWidget(QLabel("© 2025 Tarık Vardar - GPL v3 Lisansı"))
        l.addSpacing(20)
        return w

    def backend_baslat(self):
        self.thread = BilgiIsleyicisi();
        self.thread.bilgi_guncelle_sinyal.connect(self.veri_dagitici);
        self.thread.start()

    def veri_dagitici(self, veri):
        cw = self.stack.currentWidget()
        if hasattr(cw, 'guncelle'):
            try:
                cw.guncelle(veri)
            except:
                pass

    def sayfa_degistir(self, index):
        self.stack.setCurrentIndex(index);
        l = self.menu_panel.layout();
        idx = 0
        for i in range(l.count()):
            w = l.itemAt(i).widget()
            if isinstance(w, QPushButton): w.setChecked(idx == index); idx += 1