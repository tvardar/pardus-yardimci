# ana_pencere.py

import sys
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtNetwork import QLocalServer, QLocalSocket

from sayfalar.genel_bakis import GenelBakisSayfasi
from sayfalar.bakim import BakimSayfasi
from sayfalar.diger_sayfalar import SurecYonetimiSayfasi, AgAraclariSayfasi, DonanimSayfasi
from sayfalar.yonetim import YonetimSayfasi
from sayfalar.hud_penceresi import HUDPenceresi
from gorsel_araclar import BilgiIsleyicisi, SvgIkonOlusturucu, SayfaBasligi, AyarlarYoneticisi
from stil_sayfasi import get_stil


class AnaPencere(QMainWindow):
    def __init__(self, socket_name="PardusYardimciInstance"):
        super().__init__()
        self.setWindowTitle("Pardus Yardımcı")
        self.resize(1100, 700)
        self.setMinimumSize(950, 600)
        self.ayarlar = AyarlarYoneticisi()

        # --- YOL BULMA MANTIĞI (GÜNCELLENDİ) ---
        if getattr(sys, 'frozen', False):
            # PyInstaller (one-dir) modunda sys.executable, /opt/pardus-yardimci/PardusYardimci'yı gösterir.
            # Bizim icons klasörümüz bu dosyanın yanındadır (yani basedir).
            self.base_dir = os.path.dirname(sys.executable)
            
            # Bazen PyInstaller _internal klasörü oluşturur, ikonlar orada olabilir.
            # İki ihtimali de kontrol edelim:
            if not os.path.exists(os.path.join(self.base_dir, "icons")):
                self.base_dir = os.path.join(self.base_dir, "_internal")
        else:
            # Geliştirme (Python) modu
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # --- İKON SEÇİMİ (Sadece PNG) ---
        self.icon_path = os.path.join(self.base_dir, "icons", "yardimci-logo.png")
        
        # Pencere ve Uygulama İkonunu Ata
        if os.path.exists(self.icon_path):
            self.app_icon = QIcon(self.icon_path)
            self.setWindowIcon(self.app_icon)
            # Linux'ta pencere sınıfı için de ikon ayarla
            QApplication.setWindowIcon(self.app_icon)
        else:
            # İkon bulunamazsa terminale bas (debug için)
            print(f"UYARI: İkon bulunamadı: {self.icon_path}")
            self.app_icon = QIcon()

        # --- TEK ÖRNEK SUNUCUSU ---
        self.socket_name = socket_name
        self.server = QLocalServer()
        try:
            if sys.platform != "win32":
                import socket
                if os.path.exists(f"/tmp/{self.socket_name}") or os.path.exists(self.socket_name):
                     QLocalServer.removeServer(self.socket_name)
        except:
            pass
            
        self.server.listen(self.socket_name)
        self.server.newConnection.connect(self.yeni_baglanti_geldi)
        # --------------------------

        self.hud_window = None
        self.arayuzu_kur();
        self.tray_kur();
        self.backend_baslat();
        self.tema_uygula()
        self.ekran_ortala()

    def ekran_ortala(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def yeni_baglanti_geldi(self):
        socket = self.server.nextPendingConnection()
        socket.readyRead.connect(lambda: self.pencereyi_one_getir(socket))

    def pencereyi_one_getir(self, socket):
        _ = socket.readAll()
        if self.hud_window and self.hud_window.isVisible():
            self.hud_window.close() 
        self.showNormal()
        self.ekran_ortala()
        self.activateWindow()
        self.raise_()

    def get_icon_path(self, filename):
        # Diğer sayfalardan çağrılan ikonlar için
        return os.path.join(self.base_dir, "icons", filename)

    def tema_uygula(self):
        self.ayarlar.ayarlar = self.ayarlar.yukle()
        secim = self.ayarlar.ayarlar.get("tema", "Otomatik")
        tema = AyarlarYoneticisi.sistem_temasini_algila() if secim == "Otomatik" else secim
        self.setStyleSheet(get_stil(tema))

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

        # Logo Gösterimi (Yan Menü)
        if os.path.exists(self.icon_path):
            l = QLabel();
            l.setPixmap(QPixmap(self.icon_path).scaled(140, 140, Qt.AspectRatioMode.KeepAspectRatio,
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
        self.sayfa_genel = GenelBakisSayfasi(parent=self)
        self.sayfa_donanim = DonanimSayfasi()
        self.sayfa_surec = SurecYonetimiSayfasi()
        self.sayfa_ag = AgAraclariSayfasi()
        self.sayfa_yonetim = YonetimSayfasi(parent=self)
        self.sayfa_bakim = BakimSayfasi()
        self.sayfa_hakkinda = self.hakkinda_sayfasi_olustur()

        self.menuler = [
            ("Genel Bakış", SvgIkonOlusturucu.dashboard_ikonu, self.sayfa_genel),
            ("Donanım & Güç", SvgIkonOlusturucu.hardware_ikonu, self.sayfa_donanim),
            ("Süreç Yönetimi", SvgIkonOlusturucu.process_ikonu, self.sayfa_surec),
            ("Ağ & Hız Testi", SvgIkonOlusturucu.network_ikonu, self.sayfa_ag),
            ("Sistem Yönetimi", SvgIkonOlusturucu.ayarlar_ikonu, self.sayfa_yonetim),
            ("Bakım & Onarım", SvgIkonOlusturucu.maintenance_ikonu, self.sayfa_bakim),
            ("Hakkında", SvgIkonOlusturucu.info_ikonu, self.sayfa_hakkinda)
        ]

        for i, (ad, ikon_func, w) in enumerate(self.menuler):
            b = QPushButton(ad);
            b.setObjectName("MenuDugmesi");
            b.setCheckable(True);
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setIcon(QIcon(ikon_func("#AAAAAA", 24)))
            b.setIconSize(QSize(22, 22));
            if i == 0: b.setChecked(True)
            b.clicked.connect(lambda c, idx=i: self.sayfa_degistir(idx))
            menu_layout.addWidget(b);
            self.stack.addWidget(w)

        menu_layout.addStretch();
        main_layout.addWidget(self.menu_panel);
        main_layout.addWidget(self.stack)

    def hud_moduna_gec(self):
        self.hide();
        if not self.hud_window: self.hud_window = HUDPenceresi(self)
        self.hud_window.show()

    def backend_baslat(self):
        self.thread = BilgiIsleyicisi();
        self.thread.bilgi_guncelle_sinyal.connect(self.veri_dagitici);
        self.thread.start()

    def veri_dagitici(self, veri):
        if self.hud_window and self.hud_window.isVisible():
            self.hud_window.guncelle(veri)
        elif self.isVisible():
            cw = self.stack.currentWidget()
            if hasattr(cw, 'guncelle'):
                try:
                    cw.guncelle(veri)
                except:
                    pass

    def tray_kur(self):
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray = QSystemTrayIcon(self)
            
            # --- TRAY İKONU (Ana pencereden al) ---
            if not self.app_icon.isNull():
                self.tray.setIcon(self.app_icon)
            else:
                self.tray.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
                
            menu = QMenu()
            show_act = QAction("Göster", self);
            show_act.triggered.connect(self.showNormal)
            quit_act = QAction("Çıkış", self);
            quit_act.triggered.connect(self.uygulamayi_kapat)
            menu.addAction(show_act);
            menu.addAction(quit_act)
            self.tray.setContextMenu(menu);
            self.tray.show();
            self.tray.setToolTip("Pardus Yardımcı")
            self.tray.activated.connect(self.tray_tiklandi)

    def tray_tiklandi(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showNormal()
            self.activateWindow()

    def closeEvent(self, event):
        if self.tray.isVisible():
            self.hide(); event.ignore()
        else:
            self.uygulamayi_kapat()

    def uygulamayi_kapat(self):
        if self.thread and self.thread.isRunning():
            self.thread.requestInterruption();
            self.thread.quit();
            self.thread.wait(2000)
        self.server.close()
        QLocalServer.removeServer(self.socket_name)
        QApplication.instance().quit()

    def hakkinda_sayfasi_olustur(self):
        w = QWidget();
        l = QVBoxLayout(w);
        l.setAlignment(Qt.AlignmentFlag.AlignCenter);
        l.setSpacing(15)
        
        # Logo
        if os.path.exists(self.icon_path):
            img = QLabel();
            img.setPixmap(QPixmap(self.icon_path).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                                    Qt.TransformationMode.SmoothTransformation))
            img.setAlignment(Qt.AlignmentFlag.AlignCenter);
            l.addWidget(img)
            
        l.addWidget(QLabel("<h1 style='color:#33AADD; margin-bottom:0px;'>Pardus Yardımcı</h1>"))
        l.addWidget(QLabel("<h3 style='color:#AAAAAA; margin-top:0px;'>Sürüm 1.0</h3>"))
        desc = QLabel(
            "Linux sistem yönetimini kolaylaştıran, açık kaynaklı ve\nkullanıcı dostu bir sistem yönetim aracıdır.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter);
        desc.setStyleSheet("font-size: 11pt; color: #E0E0E0;")
        l.addWidget(desc);
        l.addSpacing(20)
        style = "color: #33AADD; text-decoration: none; font-size: 11pt; font-weight:bold;"
        l.addWidget(QLabel(f'<a href="mailto:tarikvardar@gmail.com" style="{style}">📧 tarikvardar@gmail.com</a>'))
        l.addWidget(QLabel(
            f'<a href="https://github.com/tvardar/pardus-yardimci" style="{style}">🐙 github.com/tvardar/pardus-yardimci</a>'))
        for i in range(l.count()):
            if l.itemAt(i).widget(): l.itemAt(i).widget().setOpenExternalLinks(True)
        l.addStretch();
        l.addWidget(QLabel("© 2025 Tarık Vardar - GPL v3 Lisansı"));
        l.addSpacing(20)
        return w

    def sayfa_degistir(self, index):
        self.stack.setCurrentIndex(index);
        l = self.menu_panel.layout();
        idx = 0
        for i in range(l.count()):
            w = l.itemAt(i).widget()
            if isinstance(w, QPushButton): w.setChecked(idx == index); idx += 1