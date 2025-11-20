# sayfalar/diger_sayfalar.py
# DÜZELTME: Ağ tarama (Nmap) ayrıştırma mantığı iyileştirildi.

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QListWidget, QPushButton, QLineEdit, QMessageBox,
                             QGroupBox, QProgressBar, QApplication, QTableWidget,
                             QTableWidgetItem, QHeaderView, QListWidgetItem, QTabWidget,
                             QScrollArea)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QIcon
import psutil
import subprocess
import platform
import requests
import time


# --- HIZ TESTİ WORKER (AYNI) ---
class HizTestiWorker(QThread):
    sonuc_sinyali = pyqtSignal(str, str)

    def run(self):
        try:
            self.sonuc_sinyali.emit("Durum", "Ping Ölçülüyor...")
            p = subprocess.check_output(["ping", "-c", "1", "8.8.8.8"], text=True)
            ping = p.split("time=")[1].split(" ")[0]
            self.sonuc_sinyali.emit("Gecikme", f"{ping} ms")

            self.sonuc_sinyali.emit("Durum", "İndirme Testi Başladı...")
            url_dl = "http://speedtest.tele2.net/10MB.zip"
            start_time = time.time()
            r = requests.get(url_dl, stream=True, timeout=10)
            size = 0
            for chunk in r.iter_content(1024 * 10):
                size += len(chunk)
                if time.time() - start_time > 5: break
            duration = time.time() - start_time
            speed_mbps = (size * 8) / (duration * 1000000)
            self.sonuc_sinyali.emit("İndirme", f"{speed_mbps:.2f} Mbps")

            self.sonuc_sinyali.emit("Durum", "Yükleme Testi Başladı...")
            data = b'0' * (1024 * 1024 * 2)
            start_time = time.time()
            try:
                requests.post("https://postman-echo.com/post", data=data, timeout=10)
                duration = time.time() - start_time
                speed_up_mbps = (len(data) * 8) / (duration * 1000000)
                self.sonuc_sinyali.emit("Yükleme", f"{speed_up_mbps:.2f} Mbps")
            except:
                self.sonuc_sinyali.emit("Yükleme", "Hata")
            self.sonuc_sinyali.emit("Bitti", "Test Tamamlandı")
        except Exception as e:
            self.sonuc_sinyali.emit("Hata", f"Hata: {e}")


# --- 1. SÜREÇ YÖNETİMİ (AYNI) ---
class SurecYonetimiSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        header = QHBoxLayout();
        lbl = QLabel("Görev Yöneticisi");
        lbl.setStyleSheet("font-size: 16pt; color: #33AADD; font-weight: bold;");
        header.addWidget(lbl)
        self.lbl_count = QLabel("Toplam: 0");
        self.lbl_count.setStyleSheet("color: #888;");
        header.addStretch();
        header.addWidget(self.lbl_count);
        layout.addLayout(header)
        self.liste = QListWidget();
        self.liste.setStyleSheet(
            "QListWidget { background: #252526; border: 1px solid #333; border-radius: 6px; } QListWidget::item { padding: 5px; border-bottom: 1px solid #2d2d30; } QListWidget::item:selected { background: #33AADD; color: white; }");
        self.liste.setFont(QFont("Monospace"));
        layout.addWidget(self.liste)
        btn_kill = QPushButton("⛔ Seçili Süreci Sonlandır");
        btn_kill.setStyleSheet(
            "background-color: #c0392b; color: white; font-weight: bold; padding: 10px; border-radius: 6px;");
        btn_kill.clicked.connect(self.oldur);
        layout.addWidget(btn_kill)
        self.timer = QTimer(self);
        self.timer.timeout.connect(lambda: self.guncelle(None));
        self.timer.start(3000);
        self.guncelle(None)

    def guncelle(self, veri=None):
        current_row = self.liste.currentRow();
        scroll_val = self.liste.verticalScrollBar().value();
        self.liste.clear();
        count = 0
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                count += 1;
                cpu = p.info['cpu_percent'];
                cpu_str = f"%{cpu:.1f}";
                metin = f"PID: {str(p.info['pid']):<6} | {p.info['name']:<20} | CPU: {cpu_str:<8} | RAM: %{p.info['memory_percent']:.1f}"
                item = QListWidgetItem(metin);
                if cpu > 50:
                    item.setForeground(QColor("#e74c3c"))
                else:
                    item.setForeground(QColor("#ecf0f1"))
                self.liste.addItem(item)
            except:
                pass
        self.lbl_count.setText(f"İşlem Sayısı: {count}");
        self.liste.verticalScrollBar().setValue(scroll_val);
        if current_row >= 0: self.liste.setCurrentRow(current_row)

    def oldur(self):
        item = self.liste.currentItem()
        if item:
            try:
                pid = int(item.text().split('|')[0].replace("PID:", "").strip()); psutil.Process(
                    pid).kill(); QMessageBox.information(self, "Başarılı", f"PID {pid} sonlandırıldı."); self.guncelle(
                    None)
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Hata: {e}")


# --- 2. AĞ ARAÇLARI (DÜZELTİLDİ: TARAMA PARSING) ---
class AgAraclariSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget();
        layout.addWidget(self.tabs)

        # TAB 1: Tanılama
        tab1 = QWidget();
        l1 = QVBoxLayout(tab1)
        grp_ping = QGroupBox("Ping Testi");
        l_ping = QVBoxLayout(grp_ping)
        h_ping = QHBoxLayout();
        self.txt_hedef = QLineEdit("google.com");
        btn_ping = QPushButton("Ping");
        btn_ping.clicked.connect(self.ping_at)
        h_ping.addWidget(self.txt_hedef);
        h_ping.addWidget(btn_ping);
        l_ping.addLayout(h_ping)
        self.ping_list = QListWidget();
        self.ping_list.setMaximumHeight(80);
        self.ping_list.setStyleSheet("background: #222; border-radius: 4px;")
        l_ping.addWidget(self.ping_list);
        l1.addWidget(grp_ping)

        grp_scan = QGroupBox("Ağ Tarama");
        l_scan = QVBoxLayout(grp_scan)
        h_scan = QHBoxLayout();
        btn_scan = QPushButton("🔍 Ağı Tara");
        btn_scan.clicked.connect(self.agi_tara)
        self.lbl_durum = QLabel("Hazır");
        self.lbl_durum.setStyleSheet("color: #aaa;")
        h_scan.addWidget(btn_scan);
        h_scan.addWidget(self.lbl_durum);
        h_scan.addStretch();
        l_scan.addLayout(h_scan)
        self.table = QTableWidget();
        self.table.setColumnCount(3);
        self.table.setHorizontalHeaderLabels(["IP", "Cihaz", "Marka"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch);
        self.table.setStyleSheet(
            "QTableWidget { background-color: #252526; gridline-color: #444; color: #eee; } QHeaderView::section { background-color: #333; padding: 4px; border: 1px solid #444; color: #33AADD; font-weight: bold; }")
        l_scan.addWidget(self.table);
        l1.addWidget(grp_scan);
        self.tabs.addTab(tab1, "Tanılama")

        # TAB 2: Hız Testi
        tab2 = QWidget();
        l2 = QVBoxLayout(tab2);
        l2.setSpacing(20);
        l2.setContentsMargins(50, 50, 50, 50)
        l2.addWidget(QLabel("<h2 style='color:#33AADD; text-align:center'>İnternet Hız Testi</h2>"))
        grid_speed = QHBoxLayout()

        def create_speed_box(title):
            box = QGroupBox(title);
            lb = QVBoxLayout(box);
            lbl = QLabel("-");
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter);
            lbl.setStyleSheet("font-size: 24pt; font-weight: bold; color: white;");
            lb.addWidget(lbl);
            return box, lbl

        box_ping, self.lbl_ping = create_speed_box("Gecikme (Ping)")
        box_dl, self.lbl_dl = create_speed_box("İndirme (Download)")
        box_ul, self.lbl_ul = create_speed_box("Yükleme (Upload)")
        grid_speed.addWidget(box_ping);
        grid_speed.addWidget(box_dl);
        grid_speed.addWidget(box_ul);
        l2.addLayout(grid_speed)
        self.btn_speed = QPushButton("🚀 Testi Başlat");
        self.btn_speed.setFixedSize(200, 60);
        self.btn_speed.setStyleSheet(
            "background-color: #e67e22; color: white; font-size: 14pt; border-radius: 30px; font-weight:bold;");
        self.btn_speed.clicked.connect(self.hiz_testi_baslat)
        l2.addStretch();
        l2.addWidget(self.btn_speed, alignment=Qt.AlignmentFlag.AlignCenter);
        l2.addStretch();
        self.tabs.addTab(tab2, "Hız Testi")

    def guncelle(self, veri=None):
        pass

    def ping_at(self):
        hedef = self.txt_hedef.text();
        item = QListWidgetItem(f"⏳ {hedef}...");
        self.ping_list.insertItem(0, item);
        QApplication.processEvents()
        try:
            subprocess.check_output(['ping', '-c', '1', '-W', '2', hedef]); item.setText(
                f"✅ {hedef} - OK"); item.setForeground(QColor("#2ecc71"))
        except:
            item.setText(f"❌ {hedef} - Yok"); item.setForeground(QColor("#e74c3c"))

    def agi_tara(self):
        self.lbl_durum.setText("Taranıyor... (Lütfen Bekleyin)")
        self.table.setRowCount(0)
        QApplication.processEvents()

        try:
            # Nmap çıktısı analizi
            process = subprocess.Popen(["pkexec", "nmap", "-sn", "192.168.1.0/24"], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                self.lbl_durum.setText("Hata / Yetki Yok")
                return

            # Ham çıktıyı satır satır işle
            # Nmap çıktısı her cihaz için bloklar halinde gelir
            raw_blocks = stdout.split("Nmap scan report for")

            count = 0
            for block in raw_blocks[1:]:  # İlk eleman boştur
                # IP ve Hostname
                first_line = block.split('\n')[0].strip()
                ip = "Bilinmiyor"
                host = "-"

                if "(" in first_line:
                    # Örn: android-xx (192.168.1.5)
                    host = first_line.split("(")[0].strip()
                    ip = first_line.split("(")[1].replace(")", "").strip()
                else:
                    # Örn: 192.168.1.5
                    ip = first_line

                # Marka (Vendor)
                vendor = "-"
                if "MAC Address:" in block:
                    # Örn: MAC Address: AA:BB:CC... (Apple)
                    mac_line = [l for l in block.split('\n') if "MAC Address:" in l][0]
                    parts = mac_line.split("MAC Address:")[1].strip()
                    if "(" in parts:
                        vendor = parts.split("(")[1].replace(")", "").strip()
                    else:
                        vendor = "Bilinmiyor"
                else:
                    # Kendi cihazımızda MAC adresi görünmez
                    vendor = "Bu Cihaz (Localhost)"

                # Tabloya Ekle
                r = self.table.rowCount()
                self.table.insertRow(r)
                self.table.setItem(r, 0, QTableWidgetItem(ip))
                self.table.setItem(r, 1, QTableWidgetItem(host))
                self.table.setItem(r, 2, QTableWidgetItem(vendor))
                count += 1

            self.lbl_durum.setText(f"Tamamlandı. {count} cihaz bulundu.")

        except Exception as e:
            self.lbl_durum.setText("Hata")
            QMessageBox.critical(self, "Hata", f"Tarama hatası: {e}")

    def hiz_testi_baslat(self):
        self.btn_speed.setText("Ölçülüyor...");
        self.btn_speed.setEnabled(False)
        self.lbl_ping.setText("...");
        self.lbl_dl.setText("...");
        self.lbl_ul.setText("...")
        self.worker = HizTestiWorker();
        self.worker.sonuc_sinyali.connect(self.hiz_sonuc);
        self.worker.start()

    def hiz_sonuc(self, tur, deger):
        if tur == "Bitti":
            self.btn_speed.setText("🚀 Testi Başlat"); self.btn_speed.setEnabled(True)
        elif tur == "Hata":
            QMessageBox.critical(self, "Hata", deger); self.btn_speed.setEnabled(True); self.btn_speed.setText(
                "Tekrar Dene")
        elif tur == "Gecikme":
            self.lbl_ping.setText(deger)
        elif tur == "İndirme":
            self.lbl_dl.setText(deger)
        elif tur == "Yükleme":
            self.lbl_ul.setText(deger)
        elif tur == "Durum":
            self.btn_speed.setText(deger)


# --- 3. DONANIM SAYFASI (AYNI) ---
class DonanimSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(QLabel("Donanım & Güç"))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        self.icerik_widget = QWidget()
        self.icerik_layout = QVBoxLayout(self.icerik_widget)
        self.icerik_layout.setSpacing(20)

        self.grp_guc = QGroupBox("Güç & Batarya")
        l_guc = QVBoxLayout(self.grp_guc)
        self.lbl_durum = QLabel("Durum: Yükleniyor...")
        self.lbl_kalan = QLabel("Kalan: -")
        self.lbl_sure = QLabel("Tahmini Süre: -")
        l_guc.addWidget(self.lbl_durum);
        l_guc.addWidget(self.lbl_kalan);
        l_guc.addWidget(self.lbl_sure)
        self.icerik_layout.addWidget(self.grp_guc)

        self.grp_sis = QGroupBox("Sistem & Donanım")
        l_sis = QVBoxLayout(self.grp_sis)
        self.lbl_gpu = QLabel("GPU: -")
        self.lbl_cpu = QLabel("CPU: -")
        self.lbl_ram = QLabel("RAM: -")
        self.lbl_distro = QLabel("Dağıtım: -")
        self.lbl_kernel = QLabel("Kernel: -")
        l_sis.addWidget(self.lbl_gpu);
        l_sis.addWidget(self.lbl_cpu);
        l_sis.addWidget(self.lbl_ram)
        l_sis.addWidget(self.lbl_distro);
        l_sis.addWidget(self.lbl_kernel)
        self.icerik_layout.addWidget(self.grp_sis)

        self.grp_disk = QGroupBox("Depolama")
        self.layout_disk = QVBoxLayout(self.grp_disk)
        self.icerik_layout.addWidget(self.grp_disk)

        self.icerik_layout.addStretch()
        scroll.setWidget(self.icerik_widget)
        layout.addWidget(scroll)

    def guncelle(self, veri=None):
        if not veri: return

        bat = veri.get('batarya', {})
        if bat.get("status_yok"):
            self.lbl_durum.setText("Kaynak: AC / Masaüstü")
            self.lbl_kalan.setText("Batarya: Bulunamadı")
            self.lbl_sure.setText("Süre: -")
        else:
            durum_txt = "Şarj Oluyor ⚡" if bat.get('plugged') else "Pilde 🔋"
            self.lbl_durum.setText(f"Durum: {durum_txt}")
            self.lbl_kalan.setText(f"Kalan: %{bat.get('percent', 0)}")
            secs = bat.get('secsleft', -1)
            sure_txt = f"{secs / 60:.0f} dk" if secs > 0 else "Hesaplanıyor..."
            self.lbl_sure.setText(f"Tahmini Süre: {sure_txt}")

        self.lbl_gpu.setText(f"<b>GPU:</b> {veri.get('ekran_karti_model', '-')}")
        self.lbl_cpu.setText(f"<b>CPU:</b> {veri.get('islemci_model', '-')}")
        self.lbl_ram.setText(f"<b>RAM:</b> {veri.get('ram_toplam', '-')}")
        self.lbl_distro.setText(f"<b>Dağıtım:</b> {veri.get('dagitim_detay', '-')}")
        self.lbl_kernel.setText(f"<b>Kernel:</b> {platform.release()}")

        while self.layout_disk.count():
            item = self.layout_disk.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        for d in veri.get("disk_bolumleri", []):
            row = QWidget()
            h = QHBoxLayout(row)
            h.setContentsMargins(0, 5, 0, 5)

            model_str = d.get("model", "Disk")
            lbl = QLabel(f"💾 {model_str} ({d['aygit']})")
            lbl.setFixedWidth(200)
            lbl.setStyleSheet("font-weight:bold; color:#33AADD")

            bar = QProgressBar()
            bar.setValue(int(d['yuzde']))
            bar.setFormat(f"%p% Dolu ({d['kullanilan']} / {d['toplam']})")
            bar.setFixedHeight(18)

            h.addWidget(lbl)
            h.addWidget(bar)
            self.layout_disk.addWidget(row)