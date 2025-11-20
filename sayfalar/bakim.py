# sayfalar/bakim.py
# UI GÜNCELLEMESİ: Konsol yerine modern durum listesi.

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel,
                             QListWidget, QListWidgetItem, QApplication)
from PyQt6.QtGui import QColor, QIcon
import subprocess
import os


class BakimSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Sistem Bakımı ve Optimizasyon"))

        # Butonlar
        grid = QGridLayout()
        grid.setSpacing(15)

        def btn(txt, cmd, icon, r, c, col="#60A549"):
            b = QPushButton(f"{icon}  {txt}")
            b.setMinimumHeight(60)
            b.setStyleSheet(
                f"background-color:{col};color:white;font-weight:bold;border-radius:8px;text-align:left;padding-left:15px;")
            b.clicked.connect(lambda: self.islem_baslat(cmd, txt))
            grid.addWidget(b, r, c)

        # Buton Yerleşimi
        btn("Sistemi Güncelle", "apt update && apt upgrade -y", "🔄", 0, 0)
        btn("Gereksizleri Sil", "apt autoremove -y && apt autoclean", "🧹", 0, 1)
        btn("Paketleri Onar", "apt install --fix-broken -y", "🛠️", 1, 0)
        btn("Önbellek Temizle", "sh -c 'echo 3 > /proc/sys/vm/drop_caches'", "🚀", 1, 1, "#d35400")
        btn("Logları Temizle", "rm -rf /var/log/*.gz", "📄", 2, 0, "#c0392b")
        btn("Thumbnail Sil", "rm -rf ~/.cache/thumbnails/*", "🖼️", 2, 1, "#c0392b")

        layout.addLayout(grid)

        layout.addSpacing(20)
        layout.addWidget(QLabel("İşlem Durumu:"))

        # İşlem Listesi (Log Konsolu Yerine)
        self.status_list = QListWidget()
        self.status_list.setStyleSheet("""
            QListWidget { background: #222; border: 1px solid #444; border-radius: 6px; }
            QListWidget::item { padding: 8px; border-bottom: 1px solid #333; font-size: 10pt; }
        """)
        layout.addWidget(self.status_list)

    def islem_baslat(self, komut_str, baslik):
        # Listeye yeni işlem ekle
        item = QListWidgetItem(f"⏳ {baslik}: Yetki bekleniyor...")
        self.status_list.insertItem(0, item)
        QApplication.processEvents()

        # Yetki al ve çalıştır
        env = os.environ.copy()
        if "DISPLAY" not in env: env["DISPLAY"] = ":0"

        full_cmd = ["pkexec", "sh", "-c", komut_str]

        try:
            item.setText(f"⚙️ {baslik}: Çalışıyor...")
            QApplication.processEvents()

            # Komutu çalıştır
            process = subprocess.run(full_cmd, capture_output=True, text=True, env=env)

            if process.returncode == 0:
                item.setText(f"✅ {baslik}: Tamamlandı.")
                item.setForeground(QColor("#2ecc71"))  # Yeşil
            else:
                # Hata mesajını kısaca göster
                err = process.stderr.strip() if process.stderr else "Bilinmeyen Hata"
                item.setText(f"❌ {baslik}: Hata! ({err[:50]}...)")
                item.setForeground(QColor("#e74c3c"))  # Kırmızı

        except Exception as e:
            item.setText(f"⚠️ {baslik}: Kritik Hata ({str(e)})")
            item.setForeground(QColor("#f1c40f"))  # Sarı