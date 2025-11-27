# gorsel_araclar.py

import platform
import psutil
import requests
import subprocess
import time
import os
import urllib3
import re
import json
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QRectF, QSize, QPointF
from PyQt6.QtGui import QFont, QColor, QPen, QPainter, QPixmap
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings


# --- AYARLAR YÖNETİCİSİ ---
class AyarlarYoneticisi:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/pardus-yardimci")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.ayarlar = self.yukle()

    def yukle(self):
        if not os.path.exists(self.config_file): return {"tema": "Otomatik"}
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except:
            return {"tema": "Otomatik"}

    def kaydet(self, anahtar, deger):
        self.ayarlar[anahtar] = deger
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_file, "w") as f: json.dump(self.ayarlar, f)

    @staticmethod
    def sistem_temasini_algila():
        try:
            out = subprocess.check_output(["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                                          text=True, stderr=subprocess.DEVNULL)
            if "dark" in out.lower(): return "Koyu"
            if "light" in out.lower(): return "Açık"
        except:
            pass
        return "Koyu"


# --- STANDART SAYFA BAŞLIĞI ---
class SayfaBasligi(QFrame):
    def __init__(self, baslik, icon_pixmap=None):
        super().__init__()
        self.setObjectName("SayfaBasligi")
        l = QHBoxLayout(self);
        l.setContentsMargins(20, 10, 20, 10)
        if icon_pixmap:
            icon_lbl = QLabel();
            icon_lbl.setPixmap(icon_pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation));
            l.addWidget(icon_lbl)
        lbl = QLabel(baslik);
        lbl.setObjectName("BaslikMetni");
        l.addWidget(lbl);
        l.addStretch()


# --- GÖRSEL BİLEŞENLER ---
class GostergeWidget(QWidget):
    def sizeHint(self): return QSize(150, 150)

    def __init__(self, parent=None, baslik="Kullanım"):
        super().__init__(parent);
        self.setMinimumSize(150, 150);
        self.deger = 0;
        self.max_deger = 100;
        self.baslik = baslik;
        self.tema_renk = "#33AADD"

    def degeri_ayarla(self, deger): self.deger = deger; self.update()
    def set_tema_rengi(self, renk): self.tema_renk = renk; self.update()

    def paintEvent(self, event):
        p = QPainter(self);
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect();
        mx, my = r.width() / 2, r.height() / 2;
        rad = min(r.width(), r.height()) / 2 - 10
        rect = QRectF(mx - rad, my - rad, rad * 2, rad * 2)
        p.setPen(QPen(QColor(100, 100, 100, 50), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap));
        p.drawArc(rect, int(45 * 16), int(-270 * 16))
        angle = int(270 * (self.deger / self.max_deger))
        p.setPen(QPen(QColor(self.tema_renk), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap));
        p.drawArc(rect, int(45 * 16), int(-angle * 16))
        p.setPen(QColor(self.tema_renk));
        p.setFont(QFont("Arial", 20, QFont.Weight.Bold));
        p.drawText(QRectF(mx - 50, my - 20, 100, 40), Qt.AlignmentFlag.AlignCenter, f"{int(self.deger)}%")
        p.setFont(QFont("Arial", 10));
        p.drawText(QRectF(mx - 50, my + rad - 25, 100, 20), Qt.AlignmentFlag.AlignCenter, self.baslik)


class HaritaWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent);
        self.layout = QVBoxLayout(self);
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.harita = QWebEngineView()
        s = self.harita.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, True)
        self.layout.addWidget(self.harita);
        self.setMinimumSize(300, 200)
        self.html_sablon = """<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" /><style>body {{ margin: 0; background: #222; }} #map {{ height: 100vh; width: 100%; }}</style></head><body><div id="map"></div><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script><script>window.onload = function() {{ if (typeof L === 'undefined') {{ document.body.innerHTML = "<h3 style='color:white;text-align:center;margin-top:50px;font-family:sans-serif'>Harita Yüklenemedi</h3>"; return; }} try {{ var map = L.map('map').setView([{lat}, {lon}], 13); L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{ maxZoom: 19, attribution: 'OSM' }}).addTo(map); L.marker([{lat}, {lon}]).addTo(map); }} catch(e) {{ console.log(e); }} }};</script></body></html>"""
        self.konumu_guncelle(39.9334, 32.8597)

    def konumu_guncelle(self, lat, lon): self.harita.setHtml(self.html_sablon.format(lat=lat, lon=lon))


# --- İKON OLUŞTURUCU ---
class SvgIkonOlusturucu:
    @staticmethod
    def svg_to_pixmap(svg_str, boyut=24):
        img = QPixmap(boyut, boyut);
        img.fill(Qt.GlobalColor.transparent)
        painter = QPainter(img);
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.end()
        return img

    @staticmethod
    def _draw_icon(draw_func, renk, boyut):
        p = QPixmap(boyut, boyut);
        p.fill(Qt.GlobalColor.transparent)
        pt = QPainter(p);
        pt.setRenderHint(QPainter.RenderHint.Antialiasing)
        pt.setPen(QPen(QColor(renk), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        pt.setBrush(Qt.BrushStyle.NoBrush)
        draw_func(pt, boyut);
        pt.end()
        return p

    @staticmethod
    def get_pixmap(svg_data, boyut=24): return SvgIkonOlusturucu.ayarlar_ikonu("#33AADD", boyut)
    
    # İkon Tanımları (Değişmedi)
    @staticmethod
    def termometre_getir(renk="#ff5555", s=24):
        def d(pt, s): pt.setBrush(QColor(renk)); pt.drawRoundedRect(int(s * 0.35), int(s * 0.1), int(s * 0.3), int(s * 0.6), 3, 3); pt.drawEllipse(int(s * 0.25), int(s * 0.6), int(s * 0.5), int(s * 0.5))
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    @staticmethod
    def indir_ikonu(renk="#33AADD", s=24):
        def d(pt, s): pt.setPen(QPen(QColor(renk), 3)); pt.drawLine(int(s / 2), int(s * 0.2), int(s / 2), int(s * 0.8)); pt.drawLine(int(s / 2), int(s * 0.8), int(s * 0.2), int(s * 0.5)); pt.drawLine(int(s / 2), int(s * 0.8), int(s * 0.8), int(s * 0.5))
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    @staticmethod
    def yukle_ikonu(renk="#e67e22", s=24):
        def d(pt, s): pt.setPen(QPen(QColor(renk), 3)); pt.drawLine(int(s / 2), int(s * 0.8), int(s / 2), int(s * 0.2)); pt.drawLine(int(s / 2), int(s * 0.2), int(s * 0.2), int(s * 0.5)); pt.drawLine(int(s / 2), int(s * 0.2), int(s * 0.8), int(s * 0.5))
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    @staticmethod
    def anahtar_ikonu(renk="#aaaaaa", s=20):
        def d(pt, s): pt.drawEllipse(int(s * 0.2), int(s * 0.2), int(s * 0.4), int(s * 0.4)); pt.drawLine(int(s * 0.5), int(s * 0.5), int(s * 0.8), int(s * 0.8))
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    @staticmethod
    def ayarlar_ikonu(renk="#E0E0E0", s=24):
        def d(pt, s): pt.drawEllipse(int(s * 0.25), int(s * 0.25), int(s * 0.5), int(s * 0.5)); pt.drawLine(int(s / 2), 0, int(s / 2), int(s * 0.2)); pt.drawLine(int(s / 2), int(s * 0.8), int(s / 2), s); pt.drawLine(0, int(s / 2), int(s * 0.2), int(s / 2)); pt.drawLine(int(s * 0.8), int(s / 2), s, int(s / 2))
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    @staticmethod
    def hud_ikonu(renk="#ffffff", s=24):
        def d(pt, s): pt.drawRoundedRect(int(s * 0.1), int(s * 0.1), int(s * 0.8), int(s * 0.8), 4, 4); pt.drawRect(int(s * 0.3), int(s * 0.3), int(s * 0.4), int(s * 0.4))
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    @staticmethod
    def dashboard_ikonu(renk="#33AADD", s=24):
        def d(pt, s): pt.drawRect(int(s * 0.1), int(s * 0.1), int(s * 0.35), int(s * 0.35)); pt.drawRect(int(s * 0.55), int(s * 0.1), int(s * 0.35), int(s * 0.35)); pt.drawRect(int(s * 0.1), int(s * 0.55), int(s * 0.35), int(s * 0.35)); pt.drawRect(int(s * 0.55), int(s * 0.55), int(s * 0.35), int(s * 0.35))
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    @staticmethod
    def hardware_ikonu(renk="#33AADD", s=24):
        def d(pt, s): pt.drawRoundedRect(int(s * 0.2), int(s * 0.2), int(s * 0.6), int(s * 0.6), 2, 2)
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    @staticmethod
    def process_ikonu(renk="#33AADD", s=24):
        def d(pt, s): path = [QPointF(0, s * 0.5), QPointF(s * 0.3, s * 0.5), QPointF(s * 0.45, s * 0.2), QPointF(s * 0.6, s * 0.8), QPointF(s * 0.75, s * 0.5), QPointF(s, s * 0.5)]; pt.drawPolyline(*path)
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    @staticmethod
    def network_ikonu(renk="#33AADD", s=24):
        def d(pt, s): pt.drawArc(int(s * 0.1), int(s * 0.1), int(s * 0.8), int(s * 0.8), 45 * 16, 90 * 16); pt.drawArc(int(s * 0.3), int(s * 0.3), int(s * 0.4), int(s * 0.4), 45 * 16, 90 * 16); pt.setBrush(QColor(renk)); pt.drawEllipse(QPointF(s * 0.5, s * 0.8), s * 0.08, s * 0.08)
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    @staticmethod
    def maintenance_ikonu(renk="#33AADD", s=24):
        def d(pt, s): pt.translate(s / 2, s / 2); pt.rotate(-45); pt.translate(-s / 2, -s / 2); pt.drawRoundedRect(int(s * 0.42), int(s * 0.4), int(s * 0.16), int(s * 0.55), 2, 2); pt.drawEllipse(int(s * 0.25), int(s * 0.05), int(s * 0.5), int(s * 0.5)); pt.setBrush(QColor("#252526")); pt.setPen(Qt.PenStyle.NoPen); pt.drawRect(int(s * 0.42), int(s * 0.05), int(s * 0.16), int(s * 0.2)); pt.resetTransform()
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    @staticmethod
    def info_ikonu(renk="#33AADD", s=24):
        def d(pt, s): pt.drawEllipse(1, 1, s - 2, s - 2); pt.drawLine(int(s * 0.5), int(s * 0.4), int(s * 0.5), int(s * 0.75)); pt.drawPoint(int(s * 0.5), int(s * 0.25))
        return SvgIkonOlusturucu._draw_icon(d, renk, s)
    
    @staticmethod
    def refresh_ikonu(renk, s=24): return SvgIkonOlusturucu.ayarlar_ikonu(renk, s)
    @staticmethod
    def clean_ikonu(renk, s=24): return SvgIkonOlusturucu.maintenance_ikonu(renk, s)
    @staticmethod
    def fix_ikonu(renk, s=24): return SvgIkonOlusturucu.ayarlar_ikonu(renk, s)
    @staticmethod
    def ram_ikonu(renk, s=24): return SvgIkonOlusturucu.hardware_ikonu(renk, s)
    @staticmethod
    def log_ikonu(renk, s=24): return SvgIkonOlusturucu.dashboard_ikonu(renk, s)
    @staticmethod
    def grub_ikonu(renk, s=24): return SvgIkonOlusturucu.dashboard_ikonu(renk, s)


# --- THREAD ---
class BilgiIsleyicisi(QThread):
    bilgi_guncelle_sinyal = pyqtSignal(dict)

    def __init__(self):
        super().__init__(); self.cached_konum = None

    def konum_bul(self):
        try:
            j = requests.get('http://ip-api.com/json', timeout=5).json(); return {"ip": j.get("query"),
                                                                              "lat": j.get("lat"),
                                                                              "lon": j.get("lon"),
                                                                              "org": j.get("isp"),
                                                                              "sehir": j.get("city"),
                                                                              "ulke": j.get("countryCode")}
        except:
            pass
        return {"ip": "N/A", "lat": 0, "lon": 0}

    def bayt_cevir(self, b):
        return f"{b / 1048576:.1f} MB"

    def get_gpu_model(self):
        try:
            out = subprocess.check_output("lspci | grep -i 'VGA\\|3D'", shell=True, text=True,
                                          stderr=subprocess.DEVNULL).strip()
            return out.split(':', 2)[-1].strip() if ':' in out else out
        except:
            return "Standart VGA / Bilinmiyor"

    def get_disk_models(self):
        """Disk modellerini eşleştiren güvenli bir sözlük döndürür."""
        models = {}
        try:
            # -d: no slaves, -n: no headings, -o: columns. 
            out = subprocess.check_output(["lsblk", "-d", "-n", "-o", "NAME,MODEL"], text=True,
                                          stderr=subprocess.DEVNULL)
            for line in out.splitlines():
                parts = line.strip().split(maxsplit=1)
                if len(parts) >= 2:
                    models[parts[0]] = parts[1]
                elif len(parts) == 1:
                    models[parts[0]] = "Disk Birimi"
        except:
            pass
        return models

    def get_battery(self):
        try:
            b = psutil.sensors_battery(); return {"percent": b.percent, "plugged": b.power_plugged,
                                                  "secsleft": b.secsleft} if b else {"status_yok": True}
        except:
            return {"status_yok": True}

    def get_temp(self):
        try:
            return int(open("/sys/class/thermal/thermal_zone0/temp").read().strip()) / 1000.0
        except:
            pass
        try:
            return psutil.sensors_temperatures()['coretemp'][0].current
        except:
            return 0

    def run(self):
        while not self.isInterruptionRequested():
            try:
                if not self.cached_konum or self.cached_konum.get("ip") == "N/A": self.cached_konum = self.konum_bul()
                
                c_pct = psutil.cpu_percent(percpu=True) or [0]
                ram = psutil.virtual_memory()
                net = psutil.net_io_counters()
                
                # --- USB VE HARİCİ DİSK DESTEĞİ İÇİN GÜNCELLENDİ ---
                disk_models = self.get_disk_models()
                disk_list = []
                
                # Sadece kesinlikle sistemle ilgili olmayan sanal FS'leri atlıyoruz.
                # 'fuseblk' eklenmedi çünkü NTFS/exFAT USB'ler genelde bu türde görünür.
                ignore_fs = ['squashfs', 'tmpfs', 'devtmpfs', 'proc', 'sysfs', 'debugfs', 'tracefs']
                
                partitions = psutil.disk_partitions(all=True)
                
                for p in partitions:
                    if p.fstype in ignore_fs:
                        continue
                    if not p.device:
                        continue
                    # Sadece loop (snap) ve sr (cdrom) hariç tutulur.
                    if "/dev/loop" in p.device or "/dev/sr" in p.device:
                        continue

                    try:
                        u = psutil.disk_usage(p.mountpoint)
                        if u.total == 0:
                            continue

                        dev_name = p.device.split('/')[-1]
                        raw_disk_name = re.sub(r'p?\d+$', '', dev_name)
                        
                        # Model ismini al, yoksa bağlama noktasına bakarak tahmin et
                        model = disk_models.get(raw_disk_name, disk_models.get(dev_name, ""))
                        
                        if not model:
                            # Model ismi yoksa, bağlama noktasından (örn: /media/kullanici/USB) çıkarım yap
                            if "/media/" in p.mountpoint or "/run/media/" in p.mountpoint:
                                model = "USB / Harici Disk"
                            else:
                                model = "Disk Birimi"

                        disk_list.append({
                            "aygit": p.device, 
                            "baglanti_noktasi": p.mountpoint, 
                            "yuzde": u.percent,
                            "kullanilan": f"{u.used / (1024 ** 3):.1f} GB",
                            "toplam": f"{u.total / (1024 ** 3):.1f} GB", 
                            "model": model
                        })
                    except Exception as e:
                        pass

                # Tüm diskler için toplamlar
                all_disks = disk_list
                toplam_kullanim_all = sum(float(d['kullanilan'].split()[0]) for d in all_disks)
                toplam_kapasite_all = sum(float(d['toplam'].split()[0]) for d in all_disks)
                yuzde_all = (toplam_kullanim_all / toplam_kapasite_all * 100) if toplam_kapasite_all > 0 else 0

                # Sadece Fiziksel HDD (/dev/sd*)
                fiziksel_hddler = [d for d in disk_list if re.search(r'/dev/sd[a-z]', d['aygit'])]
                toplam_kullanim = sum(float(d['kullanilan'].split()[0]) for d in fiziksel_hddler)
                toplam_kapasite = sum(float(d['toplam'].split()[0]) for d in fiziksel_hddler)
                yuzde_fiz = (toplam_kullanim / toplam_kapasite * 100) if toplam_kapasite > 0 else 0

                ssid = "Kablolu"
                try:
                    ssid = subprocess.check_output("nmcli -t -f NAME connection show --active", shell=True, text=True,
                                                   stderr=subprocess.DEVNULL).strip().split('\n')[0]
                except:
                    pass
                
                ni = "Eth"
                for i, d in psutil.net_if_stats().items():
                    if d.isup and i != 'lo': ni = i; break

                self.bilgi_guncelle_sinyal.emit(
                    {"cpu_yuzde": c_pct, "toplam_cpu_yuzde": sum(c_pct) / len(c_pct) if c_pct else 0,
                     "ram_yuzde": ram.percent, "ram_toplam": f"{ram.total >> 30} GB",
                     "ag_gonderilen": self.bayt_cevir(net.bytes_sent), "ag_alinan": self.bayt_cevir(net.bytes_recv),
                     "disk_bolumleri": disk_list, "konum_bilgisi": self.cached_konum, "ag_ssid": ssid, "ag_arayuz": ni,
                     "cpu_sicaklik": self.get_temp(), "dagitim_detay": self.get_distro(),
                     "islemci_model": self.get_cpu_name(), "ekran_karti_model": self.get_gpu_model(),
                     "batarya": self.get_battery(),
                     "fiziksel_hdd_kullanim": f"{toplam_kullanim:.1f} GB",
                     "fiziksel_hdd_toplam": f"{toplam_kapasite:.1f} GB",
                     "fiziksel_hdd_yuzde": f"{yuzde_fiz:.1f}%",
                     "tum_disk_kullanim": f"{toplam_kullanim_all:.1f} GB",
                     "tum_disk_toplam": f"{toplam_kapasite_all:.1f} GB",
                     "tum_disk_yuzde": f"{yuzde_all:.1f}%"})
            except Exception as e:
                pass
            self.msleep(1000)

    def get_distro(self):
        try:
            return subprocess.check_output(['lsb_release', '-ds'], text=True).strip()
        except:
            return platform.platform()

    def get_cpu_name(self):
        try:
            return [l.split(":")[1].strip() for l in open("/proc/cpuinfo") if "model name" in l][0]
        except:
            return "Bilinmiyor"