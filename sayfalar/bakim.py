# sayfalar/bakim.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel,
                             QListWidget, QListWidgetItem, QApplication)
from PyQt6.QtGui import QColor, QIcon
from gorsel_araclar import SayfaBasligi, SvgIkonOlusturucu
import subprocess
import os


class BakimSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        icon = SvgIkonOlusturucu.maintenance_ikonu("#33AADD", 32)
        layout.addWidget(SayfaBasligi("Bakım & Onarım", icon))

        grid = QGridLayout()
        grid.setSpacing(15)

        def btn(txt, cmd, icon_pixmap, r, c):
            b = QPushButton(f"  {txt}")
            b.setIcon(QIcon(icon_pixmap))
            b.setIconSize(icon_pixmap.size())
            b.setMinimumHeight(60)
            b.setStyleSheet("text-align:left; padding-left:15px; font-weight:bold;")
            b.clicked.connect(lambda: self.islem_baslat(cmd, txt))
            grid.addWidget(b, r, c)

        blue = "#33AADD";
        orange = "#e67e22";
        red = "#e74c3c"

        cmd_prefix = "DEBIAN_FRONTEND=noninteractive"
        
        btn("Sistemi Güncelle", f"{cmd_prefix} apt-get update && {cmd_prefix} apt-get upgrade -y", SvgIkonOlusturucu.refresh_ikonu(blue), 0, 0)
        btn("Gereksizleri Sil", f"{cmd_prefix} apt-get autoremove -y && {cmd_prefix} apt-get autoclean", SvgIkonOlusturucu.clean_ikonu(blue), 0, 1)
        btn("Paketleri Onar", f"{cmd_prefix} apt-get install --fix-broken -y", SvgIkonOlusturucu.fix_ikonu(blue), 1, 0)
        btn("Önbellek Temizle", "sh -c 'echo 3 > /proc/sys/vm/drop_caches'", SvgIkonOlusturucu.ram_ikonu(orange), 1, 1)
        btn("Logları Temizle", "rm -rf /var/log/*.gz", SvgIkonOlusturucu.log_ikonu(red), 2, 0)
        btn("GRUB Güncelle", "update-grub", SvgIkonOlusturucu.grub_ikonu(blue), 2, 1)

        layout.addLayout(grid)
        layout.addSpacing(20)
        layout.addWidget(QLabel("İşlem Durumu:"))

        self.status_list = QListWidget()
        self.status_list.setStyleSheet("""
            QListWidget { background: #1e1e1e; color: #ccc; font-family: Monospace; font-size: 9pt; }
            QListWidget::item { padding: 2px; }
        """)
        layout.addWidget(self.status_list)

    def islem_baslat(self, komut_str, baslik):
        # Başlangıç mesajı
        header = QListWidgetItem(f"⏳ {baslik}: İşlem Başlatılıyor...")
        header.setForeground(QColor("#f1c40f")) # Sarı
        self.status_list.addItem(header)
        self.status_list.scrollToBottom()
        QApplication.processEvents()

        env = os.environ.copy();
        env["DISPLAY"] = ":0"
        # sh -c ile komutu çalıştırıyoruz
        full_cmd = ["pkexec", "sh", "-c", komut_str]

        try:
            # Komutu çalıştır ve çıktıyı yakala
            process = subprocess.run(full_cmd, capture_output=True, text=True, env=env)
            
            # STDOUT (Normal Çıktı) Yazdır
            if process.stdout:
                for line in process.stdout.splitlines():
                    if line.strip():
                        item = QListWidgetItem(f"  > {line.strip()}")
                        item.setForeground(QColor("#aaaaaa")) # Gri detay
                        self.status_list.addItem(item)
            
            # STDERR (Hata Çıktısı) Yazdır
            if process.stderr:
                for line in process.stderr.splitlines():
                    if line.strip():
                        # apt-get uyarılarını filtrele (CLI interface uyarısı gelmez ama diğerleri gelebilir)
                        if "WARNING: apt" in line: continue
                        
                        item = QListWidgetItem(f"  ! {line.strip()}")
                        item.setForeground(QColor("#e74c3c")) # Kırmızı detay
                        self.status_list.addItem(item)

            if process.returncode == 0:
                fin = QListWidgetItem(f"✅ {baslik}: Başarıyla Tamamlandı.")
                fin.setForeground(QColor("#2ecc71")) # Yeşil
                self.status_list.addItem(fin)
            else:
                err = QListWidgetItem(f"❌ {baslik}: Hata ile Sonlandı (Kod: {process.returncode})")
                err.setForeground(QColor("#e74c3c")) # Kırmızı
                self.status_list.addItem(err)

        except Exception as e:
            item = QListWidgetItem(f"⚠️ {baslik}: Kritik Sistem Hatası ({str(e)})")
            item.setForeground(QColor("#e74c3c"))
            self.status_list.addItem(item)
        
        self.status_list.addItem(QListWidgetItem("-" * 40))
        self.status_list.scrollToBottom()