# sayfalar/yonetim.py
# DÜZELTME: 'inactive' kelimesi yanlışlıkla 'active' olarak algılanıyordu, düzeltildi.

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QListWidget, QListWidgetItem, QMessageBox, QGroupBox, QTabWidget, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import subprocess
import os
import shutil
import sys


class YonetimSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ufw_bin = self.ufw_yolu_bul()

        layout = QVBoxLayout(self)
        tabs = QTabWidget();
        layout.addWidget(tabs)

        # --- TAB 1: GENEL AYARLAR ---
        tab_gen = QWidget();
        l_gen = QVBoxLayout(tab_gen)
        l_gen.setAlignment(Qt.AlignmentFlag.AlignTop)

        grp_auto = QGroupBox("Otomatik Başlatma")
        l_auto = QVBoxLayout(grp_auto)
        self.chk_autostart = QCheckBox("Uygulamayı bilgisayar açıldığında başlat")
        self.chk_autostart.setStyleSheet("font-size: 11pt; padding: 5px;")
        self.autostart_path = os.path.expanduser("~/.config/autostart/pardus-yardimci.desktop")
        self.chk_autostart.setChecked(os.path.exists(self.autostart_path))
        self.chk_autostart.toggled.connect(self.toggle_autostart)
        l_auto.addWidget(self.chk_autostart);
        l_gen.addWidget(grp_auto)

        grp_apps = QGroupBox("Diğer Başlangıç Uygulamaları")
        l_apps = QVBoxLayout(grp_apps)
        self.list_start = QListWidget();
        l_apps.addWidget(self.list_start)
        btn_del = QPushButton("🗑️ Seçili Uygulamayı Kaldır");
        btn_del.clicked.connect(self.del_autostart)
        l_apps.addWidget(btn_del);
        l_gen.addWidget(grp_apps)
        tabs.addTab(tab_gen, "Genel Ayarlar")

        # --- TAB 2: GÜVENLİK DUVARI ---
        tab_sec = QWidget();
        l_sec = QVBoxLayout(tab_sec)
        self.header_ufw = QHBoxLayout()
        self.lbl_ufw = QLabel("Durum: Bilinmiyor (Yenile'ye Basın)")
        self.lbl_ufw.setStyleSheet("font-size: 12pt; font-weight: bold; color: #888;")
        self.header_ufw.addWidget(self.lbl_ufw)
        self.btn_install_ufw = QPushButton("📥 UFW Kur")
        self.btn_install_ufw.setStyleSheet("background-color: #33AADD; color: white; font-weight: bold;")
        self.btn_install_ufw.clicked.connect(self.install_ufw)
        self.btn_install_ufw.hide()
        self.header_ufw.addWidget(self.btn_install_ufw);
        l_sec.addLayout(self.header_ufw)

        h_btn = QHBoxLayout()
        # Tek şifre için komutlar birleştirildi
        btn_on = QPushButton("✅ Aç");
        btn_on.clicked.connect(lambda: self.ufw_cmd("enable"))
        btn_off = QPushButton("⛔ Kapat");
        btn_off.clicked.connect(lambda: self.ufw_cmd("disable"))
        h_btn.addWidget(btn_on);
        h_btn.addWidget(btn_off);
        l_sec.addLayout(h_btn)

        l_sec.addWidget(QLabel("Kurallar:"))
        self.list_rules = QListWidget();
        l_sec.addWidget(self.list_rules)
        btn_ref = QPushButton("Durumu Yenile");
        btn_ref.clicked.connect(self.check_ufw)
        l_sec.addWidget(btn_ref)
        tabs.addTab(tab_sec, "Güvenlik Duvarı")

        # --- TAB 3: SERVİSLER ---
        tab_serv = QWidget();
        l_serv = QVBoxLayout(tab_serv)
        l_serv.addWidget(QLabel("Çalışan Kritik Servisler"))
        self.list_serv = QListWidget();
        l_serv.addWidget(self.list_serv)
        btn_stop = QPushButton("⛔ Durdur");
        btn_stop.clicked.connect(self.stop_service)
        l_serv.addWidget(btn_stop)
        tabs.addTab(tab_serv, "Servisler")

        self.load_autostart();
        self.load_services()

    # --- UFW ---
    def ufw_yolu_bul(self):
        for p in ["/usr/sbin/ufw", "/sbin/ufw", "/usr/bin/ufw"]:
            if os.path.exists(p): return p
        return shutil.which("ufw") or "ufw"

    def check_ufw(self):
        if self.ufw_bin == "ufw" and not shutil.which("ufw"):
            self.lbl_ufw.setText("Durum: UFW Bulunamadı");
            self.btn_install_ufw.show();
            return
        self.btn_install_ufw.hide()
        try:
            out = subprocess.check_output(["pkexec", self.ufw_bin, "status"], text=True)
            self.list_rules.clear();
            self.parse_ufw_output(out)
        except:
            self.lbl_ufw.setText("Durum: Yetki Verilmedi / Bilinmiyor"); self.lbl_ufw.setStyleSheet("color: orange;")

    def ufw_cmd(self, action):
        try:
            # Komut: /usr/sbin/ufw enable && /usr/sbin/ufw status
            full_cmd = f"{self.ufw_bin} {action} && {self.ufw_bin} status"

            # Komutu çalıştır ve çıktıyı al
            res = subprocess.run(["pkexec", "sh", "-c", full_cmd], capture_output=True, text=True)

            if res.returncode == 0:
                self.list_rules.clear()
                self.parse_ufw_output(res.stdout)
            else:
                # Kullanıcı iptal ederse veya hata olursa
                if "dismissed" not in res.stderr:
                    QMessageBox.warning(self, "Hata", f"İşlem başarısız:\n{res.stderr}")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Komut hatası: {e}")

    def parse_ufw_output(self, out):
        # Çıktıyı küçük harfe çevirip kontrol et
        out_lower = out.lower()

        # Önce "inactive" (pasif) kontrolü yap! Çünkü "inactive" kelimesi "active"i de içerir.
        if "inactive" in out_lower or "etkin değil" in out_lower or "stopped" in out_lower:
            self.lbl_ufw.setText("Durum: KAPALI (Riskli)")
            self.lbl_ufw.setStyleSheet("color: #e74c3c; font-weight:bold; font-size:12pt")
            # Kapalıyken kural listesi boş kalsın

        elif "active" in out_lower or "etkin" in out_lower:
            self.lbl_ufw.setText("Durum: AÇIK (Güvenli)")
            self.lbl_ufw.setStyleSheet("color: #2ecc71; font-weight:bold; font-size:12pt")

            capture = False
            for l in out.split('\n'):
                if "To" in l and "Action" in l: capture = True; continue
                if capture and l.strip(): self.list_rules.addItem(l)

        else:
            # Ne açık ne kapalı anlaşılamadıysa
            self.lbl_ufw.setText("Durum: Bilinmiyor")
            self.lbl_ufw.setStyleSheet("color: orange; font-weight:bold;")

    def install_ufw(self):
        subprocess.run(["pkexec", "apt", "install", "ufw", "-y"]); self.ufw_bin = self.ufw_yolu_bul(); self.check_ufw()

    # --- BAŞLANGIÇ ---
    def toggle_autostart(self, checked):
        if checked:
            try:
                os.makedirs(os.path.dirname(self.autostart_path), exist_ok=True)
                if getattr(sys, 'frozen', False):
                    exec_cmd = sys.executable
                else:
                    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                                               "yardimci_app.py")); exec_cmd = f"{sys.executable} {script_path}"
                content = f"[Desktop Entry]\nType=Application\nName=Pardus Yardımcı\nExec={exec_cmd}\nIcon=utilities-terminal\nComment=Pardus Sistem Yöneticisi\nX-GNOME-Autostart-enabled=true\n"
                with open(self.autostart_path, "w") as f:
                    f.write(content)
                self.load_autostart()
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Eklenemedi: {e}"); self.chk_autostart.setChecked(False)
        else:
            if os.path.exists(self.autostart_path): os.remove(self.autostart_path); self.load_autostart()

    def load_autostart(self):
        self.list_start.clear();
        p = os.path.expanduser("~/.config/autostart")
        if os.path.exists(p):
            for f in os.listdir(p):
                if f.endswith(".desktop"): self.list_start.addItem(f)

    def del_autostart(self):
        i = self.list_start.currentItem()
        if i:
            try:
                os.remove(os.path.expanduser(f"~/.config/autostart/{i.text()}")); self.load_autostart()
            except:
                pass

    # --- SERVİSLER ---
    def load_services(self):
        self.list_serv.clear()
        try:
            o = subprocess.check_output("systemctl list-units --type=service --state=running --no-pager", shell=True,
                                        text=True)
            for l in o.split('\n')[1:-7]:
                if l.split(): self.list_serv.addItem(l.split()[0])
        except:
            pass

    def stop_service(self):
        i = self.list_serv.currentItem()
        if i: subprocess.run(["pkexec", "systemctl", "stop", i.text()]); self.load_services()