# sayfalar/genel_bakis.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QProgressBar, QGridLayout, QGroupBox, QApplication,
                             QPushButton, QLineEdit, QSizePolicy, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon
from gorsel_araclar import GostergeWidget, HaritaWidget, SvgIkonOlusturucu, SayfaBasligi
import socket
import psutil
import subprocess
import os


class GenelBakisSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_main = parent
        self.statik_veriler_yuklendi = False
        self.layout = QVBoxLayout(self)
        self.arayuz_kur()

    def arayuz_kur(self):
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)

        header_container = QWidget()
        hl = QHBoxLayout(header_container);
        hl.setContentsMargins(0, 0, 0, 0)
        baslik = SayfaBasligi("Genel Bakış", SvgIkonOlusturucu.dashboard_ikonu("#33AADD", 32))
        hl.addWidget(baslik, stretch=1)
        
        # --- HUD BUTONU (Matrix Yeşili Stil) ---
        btn_hud = QPushButton("HUD MODU")
        # İkon rengi de Matrix yeşili (#2ecc71)
        btn_hud.setIcon(QIcon(SvgIkonOlusturucu.hud_ikonu("#2ecc71", 24)))
        btn_hud.setFixedWidth(140)
        btn_hud.setCursor(Qt.CursorShape.PointingHandCursor)
        # CSS ile özelleştirilmiş stil
        btn_hud.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a; 
                border: 2px solid #2ecc71; 
                border-radius: 18px; 
                padding: 8px; 
                color: #2ecc71;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
                color: #1a1a1a;
            }
        """)
        btn_hud.clicked.connect(self.baslat_hud)
        hl.addWidget(btn_hud)
        self.layout.addWidget(header_container)

        ust = QWidget();
        ul = QHBoxLayout(ust);
        ul.setContentsMargins(0, 0, 0, 0)
        self.ram_gosterge = GostergeWidget(baslik="RAM")
        ul.addWidget(self.ram_gosterge)

        cg = QGroupBox("İşlemci (CPU)");
        cl = QVBoxLayout(cg)
        hl = QHBoxLayout();
        hl.addWidget(QLabel("Yük:"))
        self.cpu_text = QLabel("%0");
        self.cpu_text.setStyleSheet("font-weight:bold;")
        hl.addWidget(self.cpu_text);
        hl.addStretch()
        icon_temp = QLabel();
        icon_temp.setPixmap(SvgIkonOlusturucu.termometre_getir())
        hl.addWidget(icon_temp)
        self.temp_label = QLabel("--°C");
        self.temp_label.setStyleSheet("color:#ff5555;font-weight:bold;")
        hl.addWidget(self.temp_label);
        cl.addLayout(hl)
        self.cpu_bar = QProgressBar();
        self.cpu_bar.setFixedHeight(10);
        self.cpu_bar.setFormat("")
        cl.addWidget(self.cpu_bar)
        self.core_grid = QGridLayout()
        self.core_labels = []
        for i in range(psutil.cpu_count(logical=True)):
            l = QLabel(f"Çkrdk {i + 1}: %0");
            l.setStyleSheet("font-size:8pt; color: gray;")
            self.core_labels.append(l);
            self.core_grid.addWidget(l, i // 4, i % 4)
        cl.addLayout(self.core_grid)
        ul.addWidget(cg, stretch=1)
        self.layout.addWidget(ust)

        alt = QWidget();
        al = QHBoxLayout(alt);
        al.setContentsMargins(0, 0, 0, 0)
        ag = QGroupBox("Bağlantı Detayları");
        ag.setFixedWidth(340);
        al_v = QVBoxLayout(ag)

        w, self.lbl_ssid = self.etiket("SSID", "...")
        al_v.addWidget(w)
        w, self.lbl_ip = self.etiket("Yerel IP", "...", True);
        al_v.addWidget(w)
        w, self.lbl_genel_ip = self.etiket("Harici IP", "...", True);
        al_v.addWidget(w)
        w, self.lbl_iss = self.etiket("İSS", "...");
        al_v.addWidget(w)
        w, self.lbl_konum = self.etiket("Konum", "...");
        al_v.addWidget(w)
        al_v.addStretch()

        # WIFI ŞİFRE ALANI
        wifi_box = QWidget();
        wb_layout = QVBoxLayout(wifi_box);
        wb_layout.setContentsMargins(0, 5, 0, 5);
        wb_layout.setSpacing(5)
        h_wifi = QHBoxLayout();
        h_wifi.setSpacing(5)
        icon_key = QLabel();
        icon_key.setPixmap(SvgIkonOlusturucu.anahtar_ikonu())
        lbl_wifi_title = QLabel("Wi-Fi Parolası");
        lbl_wifi_title.setStyleSheet("font-weight:bold; color: gray;")
        h_wifi.addWidget(icon_key);
        h_wifi.addWidget(lbl_wifi_title);
        h_wifi.addStretch();
        wb_layout.addLayout(h_wifi)
        self.wifi_inp = QLineEdit();
        self.wifi_inp.setPlaceholderText("Gizli");
        self.wifi_inp.setEchoMode(QLineEdit.EchoMode.Password);
        self.wifi_inp.setReadOnly(True)
        self.wifi_inp.setStyleSheet("font-weight: bold; padding: 4px;")
        self.btn_show = QPushButton("Göster");
        self.btn_show.setFixedWidth(70);
        self.btn_show.clicked.connect(self.sifre_toggle)
        h_inp = QHBoxLayout();
        h_inp.setContentsMargins(0, 0, 0, 0);
        h_inp.addWidget(self.wifi_inp);
        h_inp.addWidget(self.btn_show);
        wb_layout.addLayout(h_inp)
        al_v.addWidget(wifi_box)

        # TRAFİK SAYACI
        trafik_box = QGroupBox();
        trafik_box.setStyleSheet("border:none; margin-top:0px; background: #222; border-radius: 6px;")
        tl = QHBoxLayout(trafik_box);
        tl.setContentsMargins(5, 5, 5, 5)
        i_down = QLabel();
        i_down.setPixmap(SvgIkonOlusturucu.indir_ikonu());
        tl.addWidget(i_down)
        self.lbl_indir = QLabel("0 MB");
        self.lbl_indir.setStyleSheet("font-weight:bold;color:#33AADD;font-size:10pt;");
        tl.addWidget(self.lbl_indir)
        tl.addStretch()
        i_up = QLabel();
        i_up.setPixmap(SvgIkonOlusturucu.yukle_ikonu());
        tl.addWidget(i_up)
        self.lbl_yukle = QLabel("0 MB");
        self.lbl_yukle.setStyleSheet("font-weight:bold;color:#e67e22;font-size:10pt;");
        tl.addWidget(self.lbl_yukle)
        al_v.addWidget(trafik_box)

        al.addWidget(ag)
        self.map = HaritaWidget()
        self.map.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        al.addWidget(self.map)
        self.layout.addWidget(alt)

    def etiket(self, t, v, c=False):
        w = QWidget();
        l = QVBoxLayout(w);
        l.setContentsMargins(0, 0, 0, 0);
        l.setSpacing(0)
        l.addWidget(QLabel(f"<small style='color:gray'>{t}</small>"))
        val = QLabel(v);
        val.setStyleSheet("color:#33AADD;font-weight:bold;font-size:11pt;")
        if c: val.setCursor(Qt.CursorShape.PointingHandCursor); val.mousePressEvent = lambda \
            e: QApplication.clipboard().setText(val.text())
        l.addWidget(val);
        return w, val

    def sifre_toggle(self):
        if self.wifi_inp.echoMode() == QLineEdit.EchoMode.Normal:
            self.wifi_inp.setEchoMode(QLineEdit.EchoMode.Password);
            self.btn_show.setText("Göster");
            return
        ssid = self.lbl_ssid.text()
        if "..." in ssid or "Bilinmiyor" in ssid: return
        env = os.environ.copy();
        env["DISPLAY"] = ":0"
        cmds = [["pkexec", "nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", ssid],
                ["pkexec", "nmcli", "device", "wifi", "show-password"]]
        sifre = None
        for cmd in cmds:
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, env=env)
                if res.returncode == 0 and res.stdout.strip():
                    out = res.stdout.strip()
                    if "Password:" in out: out = out.split("Password:")[1].strip()
                    sifre = out;
                    break
            except:
                pass
        if sifre:
            self.wifi_inp.setText(sifre); self.wifi_inp.setEchoMode(QLineEdit.EchoMode.Normal); self.btn_show.setText(
                "Gizle")
        else:
            QMessageBox.warning(self, "Hata", "Şifre alınamadı.")

    def guncelle(self, veri):
        cpu_val = int(veri.get("toplam_cpu_yuzde", 0))
        self.ram_gosterge.degeri_ayarla(veri.get("ram_yuzde", 0))
        self.cpu_bar.setValue(cpu_val)
        self.cpu_text.setText(f"%{cpu_val}")
        self.temp_label.setText(f"{veri.get('cpu_sicaklik', 0):.1f}°C")
        for i, v in enumerate(veri.get("cpu_yuzde", [])):
            if i < len(self.core_labels): self.core_labels[i].setText(f"Çekirdek {i + 1}: %{v:.0f}")
        self.lbl_ssid.setText(veri.get("ag_ssid", "..."))
        self.lbl_ip.setText(socket.gethostbyname(socket.gethostname()))
        self.lbl_indir.setText(f"{veri.get('ag_alinan', '0 MB')}")
        self.lbl_yukle.setText(f"{veri.get('ag_gonderilen', '0 MB')}")
        k = veri.get("konum_bilgisi", {})
        if k and k.get("ip") != "N/A":
            self.lbl_genel_ip.setText(k.get("ip"))
            self.lbl_iss.setText(k.get("org"))
            self.lbl_konum.setText(f"{k.get('sehir')}, {k.get('ulke')}")
            if not self.statik_veriler_yuklendi and k.get("lat"):
                self.map.konumu_guncelle(k.get("lat"), k.get("lon"))
                self.statik_veriler_yuklendi = True

    def baslat_hud(self):
        if hasattr(self.parent_main, 'hud_moduna_gec'):
            self.parent_main.hud_moduna_gec()