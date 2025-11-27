# sayfalar/diger_sayfalar.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QListWidget, QPushButton, QLineEdit, QMessageBox,
                             QGroupBox, QProgressBar, QApplication, QTableWidget,
                             QTableWidgetItem, QHeaderView, QListWidgetItem, QTabWidget,
                             QScrollArea, QFrame, QFileDialog)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QIcon
from gorsel_araclar import SayfaBasligi, SvgIkonOlusturucu
import psutil
import subprocess
import platform
import requests
import time
import re
import threading
from datetime import datetime


class HizTestiWorker(QThread):
    sonuc_sinyali = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.is_running = True
        self.total_downloaded = 0
        self.total_uploaded = 0
        self.io_lock = threading.Lock()

    def download_thread_func(self, url, duration):
        try:
            with requests.get(url, stream=True, timeout=5) as r:
                r.raise_for_status()
                start_t = time.time()
                for chunk in r.iter_content(chunk_size=40960):
                    if not self.is_running: break
                    with self.io_lock:
                        self.total_downloaded += len(chunk)
                    if time.time() - start_t > duration:
                        break
        except:
            pass

    def upload_thread_func(self, url, data, duration):
        start_t = time.time()
        while self.is_running and (time.time() - start_t < duration):
            try:
                r = requests.post(url, data=data, timeout=5)
                if r.status_code == 200:
                    with self.io_lock:
                        self.total_uploaded += len(data)
            except:
                pass

    def run(self):
        try:
            self.sonuc_sinyali.emit("Durum", "Ping Ölçülüyor...")
            try:
                p = subprocess.check_output(["ping", "-c", "3", "-W", "1", "8.8.8.8"], text=True)
                if "min/avg/max" in p:
                    val = p.split("min/avg/max")[1].split("=")[1].split("/")[1].strip()
                    self.sonuc_sinyali.emit("Gecikme", f"{val} ms")
                else:
                    self.sonuc_sinyali.emit("Gecikme", "~ ms")
            except:
                self.sonuc_sinyali.emit("Gecikme", "Hata")

            self.sonuc_sinyali.emit("Durum", "İndirme Başlatılıyor (Multi-Thread)...")
            
            url_dl = "https://speed.cloudflare.com/__down?bytes=50000000"
            self.total_downloaded = 0
            self.is_running = True
            
            threads = []
            test_duration = 10 
            start_time = time.time()
            
            for _ in range(4):
                t = threading.Thread(target=self.download_thread_func, args=(url_dl, test_duration))
                t.daemon = True
                t.start()
                threads.append(t)
            
            for t in threads:
                t.join()
                
            actual_duration = time.time() - start_time
            if actual_duration <= 0: actual_duration = 1
            
            dl_mbps = (self.total_downloaded * 8) / (actual_duration * 1000000)
            self.sonuc_sinyali.emit("İndirme", f"{dl_mbps:.2f} Mbps")

            self.sonuc_sinyali.emit("Durum", "Yükleme Başlatılıyor (Multi-Thread)...")
            
            url_ul = "https://speed.cloudflare.com/__up"
            self.total_uploaded = 0
            chunk_size = 512 * 1024 
            dummy_data = b'0' * chunk_size 
            
            threads = []
            start_time = time.time()
            
            for _ in range(4):
                t = threading.Thread(target=self.upload_thread_func, args=(url_ul, dummy_data, test_duration))
                t.daemon = True
                t.start()
                threads.append(t)
                
            for t in threads:
                t.join()
                
            actual_duration = time.time() - start_time
            if actual_duration <= 0: actual_duration = 1
            
            ul_mbps = (self.total_uploaded * 8) / (actual_duration * 1000000)
            self.sonuc_sinyali.emit("Yükleme", f"{ul_mbps:.2f} Mbps")

            self.sonuc_sinyali.emit("Durum", "Test Tamamlandı")
            self.sonuc_sinyali.emit("Bitti", "Bitti")

        except Exception as e:
            self.sonuc_sinyali.emit("Hata", str(e))
            
    def stop(self):
        self.is_running = False


class SurecYonetimiSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        icon = SvgIkonOlusturucu.process_ikonu("#33AADD", 32)
        layout.addWidget(SayfaBasligi("Görev Yöneticisi", icon))
        header = QHBoxLayout();
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


class AgAraclariSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        icon = SvgIkonOlusturucu.network_ikonu("#33AADD", 32)
        layout.addWidget(SayfaBasligi("Ağ & Hız Testi", icon))
        self.tabs = QTabWidget();
        layout.addWidget(self.tabs)
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
        
        icon_scan = QIcon(SvgIkonOlusturucu.info_ikonu("#33AADD"))
        self.tabs.addTab(tab1, icon_scan, "Tanılama")
        
        tab2 = QWidget();
        l2 = QVBoxLayout(tab2);
        l2.setSpacing(20);
        l2.setContentsMargins(50, 50, 50, 50)
        l2.addWidget(QLabel("<h2 style='color:#33AADD; text-align:center'>İnternet Hız Testi</h2>"))
        self.lbl_test_durum = QLabel("Başlamaya Hazır");
        self.lbl_test_durum.setAlignment(Qt.AlignmentFlag.AlignCenter);
        l2.addWidget(self.lbl_test_durum)
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
        box_dl, self.lbl_dl = create_speed_box("İndirme (Mbps)")
        box_ul, self.lbl_ul = create_speed_box("Yükleme (Mbps)")
        grid_speed.addWidget(box_ping);
        grid_speed.addWidget(box_dl);
        grid_speed.addWidget(box_ul);
        l2.addLayout(grid_speed)
        self.btn_speed = QPushButton("🚀 TESTİ BAŞLAT");
        self.btn_speed.setFixedSize(220, 60);
        self.btn_speed.setStyleSheet(
            "background-color: #e67e22; color: white; font-size: 14pt; border-radius: 30px; font-weight:bold;");
        self.btn_speed.clicked.connect(self.hiz_testi_baslat)
        l2.addStretch();
        l2.addWidget(self.btn_speed, alignment=Qt.AlignmentFlag.AlignCenter);
        l2.addStretch();
        
        icon_speed = QIcon(SvgIkonOlusturucu.dashboard_ikonu("#e67e22"))
        self.tabs.addTab(tab2, icon_speed, "Hız Testi")

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
        self.lbl_durum.setText("Taranıyor... (Bekleyin)");
        self.table.setRowCount(0);
        QApplication.processEvents()
        try:
            out = subprocess.check_output(["pkexec", "nmap", "-sn", "192.168.1.0/24"], text=True)
            for block in out.split("Nmap scan report for")[1:]:
                lines = block.split('\n');
                ip = "Bilinmiyor";
                host = "-";
                vendor = "-"
                h = lines[0].strip()
                if "(" in h:
                    host = h.split("(")[0].strip(); ip = h.split("(")[1].replace(")", "").strip()
                else:
                    ip = h
                for l in lines:
                    if "MAC Address:" in l:
                        v = l.split("MAC Address:")[1].strip()
                        if "(" in v:
                            vendor = v.split("(")[1].replace(")", "").strip()
                        else:
                            vendor = v
                r = self.table.rowCount();
                self.table.insertRow(r);
                self.table.setItem(r, 0, QTableWidgetItem(ip));
                self.table.setItem(r, 1, QTableWidgetItem(host));
                self.table.setItem(r, 2, QTableWidgetItem(vendor))
            self.lbl_durum.setText(f"Tamamlandı: {self.table.rowCount()} cihaz")
        except Exception as e:
            self.lbl_durum.setText("Hata"); QMessageBox.critical(self, "Hata", str(e))

    def hiz_testi_baslat(self):
        self.btn_speed.setText("Ölçülüyor...");
        self.btn_speed.setEnabled(False);
        self.lbl_ping.setText("...");
        self.lbl_dl.setText("...");
        self.lbl_ul.setText("...");
        self.worker = HizTestiWorker();
        self.worker.sonuc_sinyali.connect(self.hiz_sonuc);
        self.worker.start()

    def hiz_sonuc(self, tur, deger):
        if tur == "Bitti":
            self.btn_speed.setText("Testi Tekrarla"); self.btn_speed.setEnabled(True)
        elif tur == "Hata":
            QMessageBox.critical(self, "Hata", deger); self.btn_speed.setEnabled(True); self.btn_speed.setText(
                "Tekrar Dene")
        elif tur == "Gecikme":
            self.lbl_ping.setText(deger); self.lbl_ping.setStyleSheet(
                "color: #f1c40f; font-size: 24pt; font-weight: bold;")
        elif tur == "İndirme":
            self.lbl_dl.setText(deger); self.lbl_dl.setStyleSheet("color: #2ecc71; font-size: 24pt; font-weight: bold;")
        elif tur == "Yükleme":
            self.lbl_ul.setText(deger); self.lbl_ul.setStyleSheet("color: #3498db; font-size: 24pt; font-weight: bold;")
        elif tur == "Durum":
            self.lbl_test_durum.setText(deger)


class DonanimSayfasi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self);
        layout.setContentsMargins(20, 20, 20, 20)
        from gorsel_araclar import SayfaBasligi, SvgIkonOlusturucu
        icon = SvgIkonOlusturucu.hardware_ikonu("#33AADD", 32)
        layout.addWidget(SayfaBasligi("Donanım & Güç", icon))

        # BUTONLAR GRUBU
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_yenile = QPushButton("🔄 Yenile")
        self.btn_yenile.setStyleSheet("background-color: #33AADD; color: white; font-weight: bold; padding: 8px;")
        self.btn_yenile.clicked.connect(self.manuel_yenile)
        btn_layout.addWidget(self.btn_yenile)
        
        btn_txt = QPushButton("📄 Raporu Kaydet (TXT)")
        btn_txt.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; padding: 8px;")
        btn_txt.clicked.connect(self.txt_kaydet)
        btn_layout.addWidget(btn_txt)

        layout.addLayout(btn_layout)

        scroll = QScrollArea();
        scroll.setWidgetResizable(True);
        scroll.setStyleSheet("background: transparent; border: none;")
        self.icerik_widget = QWidget();
        self.icerik_layout = QVBoxLayout(self.icerik_widget);
        self.icerik_layout.setSpacing(20)

        self.grp_guc = QGroupBox("Güç & Batarya");
        l_guc = QVBoxLayout(self.grp_guc)
        self.lbl_durum = QLabel("Durum: Yükleniyor...");
        self.lbl_kalan = QLabel("Kalan: -");
        self.lbl_sure = QLabel("Tahmini Süre: -")
        l_guc.addWidget(self.lbl_durum);
        l_guc.addWidget(self.lbl_kalan);
        l_guc.addWidget(self.lbl_sure);
        self.icerik_layout.addWidget(self.grp_guc)

        self.grp_sis = QGroupBox("Sistem & Donanım");
        l_sis = QVBoxLayout(self.grp_sis)
        self.lbl_gpu = QLabel("GPU: -");
        self.lbl_cpu = QLabel("CPU: -");
        self.lbl_ram = QLabel("RAM: -");
        self.lbl_distro = QLabel("Dağıtım: -");
        self.lbl_kernel = QLabel("Kernel: -")
        l_sis.addWidget(self.lbl_gpu);
        l_sis.addWidget(self.lbl_cpu);
        l_sis.addWidget(self.lbl_ram);
        l_sis.addWidget(self.lbl_distro);
        l_sis.addWidget(self.lbl_kernel);
        self.icerik_layout.addWidget(self.grp_sis)

        # Tüm Diskler Toplamı (Fiziksel/Sanal Dahil, % ile)
        self.grp_tum_disk = QGroupBox("Tüm Diskler Toplamı");
        l_tum = QHBoxLayout(self.grp_tum_disk)
        self.lbl_tum_kullanim = QLabel("Kullanılan: 0 GB (%0)");
        self.lbl_tum_toplam = QLabel("Toplam: 0 GB");
        l_tum.addWidget(self.lbl_tum_kullanim);
        l_tum.addStretch();
        l_tum.addWidget(self.lbl_tum_toplam);
        self.icerik_layout.addWidget(self.grp_tum_disk)

        # Fiziksel HDD Toplamı (% ile)
        self.grp_hdd_toplam = QGroupBox("Fiziksel HDD Toplamı (/dev/sd*)");
        l_hdd = QHBoxLayout(self.grp_hdd_toplam)
        self.lbl_hdd_kullanim = QLabel("Kullanılan: 0 GB");
        self.lbl_hdd_yuzde = QLabel("(%0)");
        self.lbl_hdd_toplam = QLabel("Toplam: 0 GB");
        l_hdd.addWidget(self.lbl_hdd_kullanim);
        l_hdd.addWidget(self.lbl_hdd_yuzde);
        l_hdd.addStretch();
        l_hdd.addWidget(self.lbl_hdd_toplam);
        self.icerik_layout.addWidget(self.grp_hdd_toplam)

        self.grp_disk = QGroupBox("Depolama Birimleri (Tümü)");
        self.layout_disk = QVBoxLayout(self.grp_disk);
        self.layout_disk.setSpacing(15);
        self.icerik_layout.addWidget(self.grp_disk)
        self.icerik_layout.addStretch();
        scroll.setWidget(self.icerik_widget);
        layout.addWidget(scroll)
        self.son_veri = {}

    def manuel_yenile(self):
        """Disk listesini temizler, böylece 1sn sonraki otomatik döngüde yenileri eklenir."""
        while self.layout_disk.count():
             item = self.layout_disk.takeAt(0)
             if item.widget():
                 item.widget().deleteLater()
        
        lbl_info = QLabel("Yenileniyor... Lütfen bekleyin.");
        lbl_info.setStyleSheet("color: orange; font-style: italic;")
        self.layout_disk.addWidget(lbl_info)

    def txt_kaydet(self):
        if not self.son_veri: return
        path, _ = QFileDialog.getSaveFileName(self, "Rapor Kaydet", f"sistem_raporu_{int(time.time())}.txt",
                                              "Text Files (*.txt)")
        if path:
            try:
                # Veriyi düzgün bir formata dönüştür
                lines = []
                lines.append(f"--- PARDUS YARDIMCI SİSTEM RAPORU ---")
                lines.append(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                lines.append("-" * 40)
                
                lines.append(f"[SİSTEM ÖZETİ]")
                lines.append(f"Dağıtım: {self.son_veri.get('dagitim_detay', 'Bilinmiyor')}")
                lines.append(f"Kernel: {platform.release()}")
                lines.append(f"CPU Modeli: {self.son_veri.get('islemci_model', 'Bilinmiyor')}")
                lines.append(f"GPU Modeli: {self.son_veri.get('ekran_karti_model', 'Bilinmiyor')}")
                lines.append(f"CPU Sıcaklık: {self.son_veri.get('cpu_sicaklik', 0)}°C")
                lines.append(f"RAM: {self.son_veri.get('ram_toplam', '0 GB')} (Kullanım: %{self.son_veri.get('ram_yuzde', 0)})")
                lines.append("")
                
                lines.append(f"[AĞ BİLGİLERİ]")
                k = self.son_veri.get('konum_bilgisi', {})
                lines.append(f"SSID: {self.son_veri.get('ag_ssid', 'Yok')}")
                lines.append(f"Arayüz: {self.son_veri.get('ag_arayuz', 'Yok')}")
                lines.append(f"Harici IP: {k.get('ip', 'N/A')}")
                lines.append(f"Konum: {k.get('sehir', '-')}, {k.get('ulke', '-')}")
                lines.append(f"İndirilen: {self.son_veri.get('ag_alinan', '0 MB')}")
                lines.append(f"Yüklenen: {self.son_veri.get('ag_gonderilen', '0 MB')}")
                lines.append("")
                
                lines.append(f"[DEPOLAMA BİRİMLERİ]")
                for disk in self.son_veri.get('disk_bolumleri', []):
                    lines.append(f"Sürücü: {disk['aygit']} ({disk['model']})")
                    lines.append(f"  Bağlama: {disk['baglanti_noktasi']}")
                    lines.append(f"  Kullanım: {disk['kullanilan']} / {disk['toplam']} (%{disk['yuzde']})")
                    lines.append("-")
                
                with open(path, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
                
                QMessageBox.information(self, "Başarılı", "Rapor başarıyla kaydedildi.")
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Rapor kaydedilemedi: {e}")

    def guncelle(self, veri=None):
        if not veri: return
        self.son_veri = veri
        bat = veri.get('batarya', {})
        if bat.get("status_yok"):
            self.lbl_durum.setText("Kaynak: AC / Masaüstü");
            self.lbl_kalan.setText("Batarya: Bulunamadı");
            self.lbl_sure.setText("Süre: -")
        else:
            durum_txt = "Şarj Oluyor ⚡" if bat.get('plugged') else "Pilde 🔋"
            self.lbl_durum.setText(f"Durum: {durum_txt}");
            self.lbl_kalan.setText(f"Kalan: %{bat.get('percent', 0)}")
            secs = bat.get('secsleft', -1);
            sure_txt = f"{secs // 60} dk" if secs > 0 else "Hesaplanıyor...";
            self.lbl_sure.setText(f"Tahmini Süre: {sure_txt}")
        self.lbl_gpu.setText(f"<b>GPU:</b> {veri.get('ekran_karti_model', '-')}");
        self.lbl_cpu.setText(f"<b>CPU:</b> {veri.get('islemci_model', '-')}")
        self.lbl_ram.setText(f"<b>RAM:</b> {veri.get('ram_toplam', '-')}");
        self.lbl_distro.setText(f"<b>Dağıtım:</b> {veri.get('dagitim_detay', '-')}")
        self.lbl_kernel.setText(f"<b>Kernel:</b> {platform.release()}")

        # Tüm Diskler Güncelle
        self.lbl_tum_kullanim.setText(f"Kullanılan: {veri.get('tum_disk_kullanim', '0 GB')} {veri.get('tum_disk_yuzde', '%0')}")
        self.lbl_tum_toplam.setText(f"Toplam: {veri.get('tum_disk_toplam', '0 GB')}")

        # Fiziksel HDD Güncelle
        self.lbl_hdd_kullanim.setText(f"Kullanılan: {veri.get('fiziksel_hdd_kullanim', '0 GB')}")
        self.lbl_hdd_yuzde.setText(f"{veri.get('fiziksel_hdd_yuzde', '%0')}")
        self.lbl_hdd_toplam.setText(f"Toplam: {veri.get('fiziksel_hdd_toplam', '0 GB')}")

        while self.layout_disk.count(): item = self.layout_disk.takeAt(0);
        if item.widget(): item.widget().deleteLater()
        for d in veri.get("disk_bolumleri", []):
            row = QWidget();
            h = QHBoxLayout(row);
            h.setContentsMargins(0, 5, 0, 5)
            model_str = d.get("model", "Disk")
            lbl = QLabel(f"💾 {model_str} ({d['aygit']})");
            lbl.setFixedWidth(200);
            lbl.setStyleSheet("font-weight:bold; color:#33AADD")
            bar = QProgressBar();
            bar.setValue(int(d['yuzde']));
            bar.setFormat(f"%p% – {d['kullanilan']} / {d['toplam']}");
            bar.setTextVisible(True);
            bar.setAlignment(Qt.AlignmentFlag.AlignCenter);
            bar.setFixedHeight(18)
            h.addWidget(lbl);
            h.addWidget(bar);
            self.layout_disk.addWidget(row)