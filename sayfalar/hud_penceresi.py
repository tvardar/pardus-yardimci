# sayfalar/hud_penceresi.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QProgressBar, QApplication, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen


class HUDPenceresi(QWidget):
    def __init__(self, ana_pencere_ref):
        super().__init__()
        self.ana_pencere = ana_pencere_ref

        # Pencere Ayarları
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.Tool)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.resize(320, 240)
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 340, 50)

        self.arayuzu_kur()

    def arayuzu_kur(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        # Ana Başlık
        header = QHBoxLayout()
        self.lbl_title = QLabel("SİSTEM MONİTÖRÜ")
        self.lbl_title.setStyleSheet("color: #888; font-weight: bold; font-size: 9pt; letter-spacing: 2px;")
        header.addWidget(self.lbl_title)
        header.addStretch()

        # Kapatma İpucu (Artık Tıklanabilir)
        self.lbl_close = QLabel("✕")
        self.lbl_close.setStyleSheet("color: #555; font-weight: bold; font-size: 14pt; padding: 2px;")
        self.lbl_close.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lbl_close.mousePressEvent = self.kapat_tiklandi
        header.addWidget(self.lbl_close)
        layout.addLayout(header)

        # Izgara Düzeni (Grid)
        grid = QGridLayout()
        grid.setSpacing(15)

        # --- BİLEŞEN OLUŞTURUCU ---
        def create_stat(title, color):
            lbl_t = QLabel(title)
            lbl_t.setStyleSheet("color: #aaa; font-size: 8pt;")
            lbl_v = QLabel("-")
            lbl_v.setStyleSheet("color: white; font-size: 14pt; font-weight: bold; font-family: Monospace;")
            bar = QProgressBar()
            bar.setFixedHeight(6)
            bar.setTextVisible(False)
            bar.setStyleSheet(f"""
                QProgressBar {{ background: #333; border-radius: 3px; border: none; }}
                QProgressBar::chunk {{ background: {color}; border-radius: 3px; }}
            """)
            return lbl_t, lbl_v, bar

        # 1. CPU
        self.l_cpu_t, self.l_cpu_v, self.bar_cpu = create_stat("İŞLEMCİ", "#33AADD")
        grid.addWidget(self.l_cpu_t, 0, 0)
        grid.addWidget(self.l_cpu_v, 1, 0)
        grid.addWidget(self.bar_cpu, 2, 0)

        # 2. RAM
        self.l_ram_t, self.l_ram_v, self.bar_ram = create_stat("BELLEK", "#9b59b6")
        grid.addWidget(self.l_ram_t, 0, 1)
        grid.addWidget(self.l_ram_v, 1, 1)
        grid.addWidget(self.bar_ram, 2, 1)

        # 3. ISI
        self.l_temp_t, self.l_temp_v, self.bar_temp = create_stat("SICAKLIK", "#e67e22")
        self.bar_temp.setRange(0, 100)
        grid.addWidget(self.l_temp_t, 3, 0)
        grid.addWidget(self.l_temp_v, 4, 0)
        grid.addWidget(self.bar_temp, 5, 0)

        # 4. AĞ
        vbox_net = QVBoxLayout()
        vbox_net.setSpacing(2)
        lbl_net_t = QLabel("AĞ TRAFİĞİ")
        lbl_net_t.setStyleSheet("color: #aaa; font-size: 8pt;")
        vbox_net.addWidget(lbl_net_t)
        self.lbl_dl = QLabel("▼ 0 MB")
        self.lbl_dl.setStyleSheet("color: #2ecc71; font-size: 11pt; font-weight: bold;")
        vbox_net.addWidget(self.lbl_dl)
        self.lbl_ul = QLabel("▲ 0 MB")
        self.lbl_ul.setStyleSheet("color: #f1c40f; font-size: 11pt; font-weight: bold;")
        vbox_net.addWidget(self.lbl_ul)
        grid.addLayout(vbox_net, 3, 1, 3, 1)

        layout.addLayout(grid)
        layout.addStretch()

        lbl_info = QLabel("Çift Tıkla: Kapat | Sürükle: Taşı")
        lbl_info.setStyleSheet("color: #444; font-size: 7pt;")
        lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_info)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(20, 20, 20, 210)))
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 15, 15)
        painter.setBrush(QBrush(QColor(255, 255, 255, 5)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(1, 1, self.width() - 2, 40, 15, 15)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        self.close()

    def kapat_tiklandi(self, event):
        """X butonuna tıklandığında çalışır"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.close()

    def closeEvent(self, event):
        """Pencere kapanırken ana pencereyi geri çağır ve ortala"""
        if self.ana_pencere:
            self.ana_pencere.showNormal()
            self.ana_pencere.ekran_ortala() # Burası kritik
            self.ana_pencere.activateWindow()
        event.accept()

    def guncelle(self, veri):
        cpu = int(veri.get("toplam_cpu_yuzde", 0))
        self.l_cpu_v.setText(f"%{cpu}")
        self.bar_cpu.setValue(cpu)
        color = "#e74c3c" if cpu > 80 else "#33AADD"
        self.bar_cpu.setStyleSheet(
            f"QProgressBar {{ background: #333; border-radius: 3px; border: none; }} QProgressBar::chunk {{ background: {color}; border-radius: 3px; }}")

        ram = int(veri.get("ram_yuzde", 0))
        self.l_ram_v.setText(f"%{ram}")
        self.bar_ram.setValue(ram)

        temp = veri.get("cpu_sicaklik", 0)
        self.l_temp_v.setText(f"{temp:.0f}°C")
        self.bar_temp.setValue(int(temp))

        dl = veri.get("ag_alinan", "0 MB")
        ul = veri.get("ag_gonderilen", "0 MB")
        self.lbl_dl.setText(f"▼ {dl}")
        self.lbl_ul.setText(f"▲ {ul}")